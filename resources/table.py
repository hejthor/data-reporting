import pandas as pd
import os
import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo

def _save_csv(df, item, path):
    file_name = os.path.basename(item['table'])
    save_path = os.path.join(path, file_name)
    df_str = df.astype(str)
    df_str.to_csv(save_path, index=False, sep=item['delimiter'])
    return save_path

def _save_excel(df, save_path):
    excel_save_path = os.path.splitext(save_path)[0] + '.xlsx'
    df.to_excel(excel_save_path, index=False)
    return excel_save_path

def _format_excel(excel_save_path):
    try:
        wb = openpyxl.load_workbook(excel_save_path)
        ws = wb.active
        min_col = ws.min_column
        max_col = ws.max_column
        min_row = ws.min_row
        max_row = ws.max_row
        table_ref = f"{ws.cell(row=min_row, column=min_col).coordinate}:{ws.cell(row=max_row, column=max_col).coordinate}"
        table = Table(displayName="DataTable", ref=table_ref)
        style = TableStyleInfo(name="TableStyleLight8", showFirstColumn=False,
                              showLastColumn=False, showRowStripes=True, showColumnStripes=False)
        table.tableStyleInfo = style
        ws.add_table(table)
        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                try:
                    cell_value = str(cell.value) if cell.value is not None else ""
                    if len(cell_value) > max_length:
                        max_length = len(cell_value)
                except Exception:
                    pass
            adjusted_width = max_length + 2
            ws.column_dimensions[col_letter].width = adjusted_width
        wb.save(excel_save_path)
    except ImportError:
        print("[PYTHON][generate_markdown.py] openpyxl is not installed. Excel formatting skipped.")
    except Exception as e:
        print(f"[PYTHON][generate_markdown.py] Error formatting Excel file: {e}")

def table_to_markdown(item, filter_column=None, filter_value=None):
    df = pd.read_csv(item['table'], delimiter=item['delimiter'], engine="python", on_bad_lines="skip")
    if filter_column and filter_value:
        if filter_column in df.columns and filter_value in df[filter_column].values:
            df = df[df[filter_column] == filter_value]
            df = df.drop(columns=[filter_column])
        else:
            return None
    return df.to_markdown(index=False, tablefmt="pipe", colalign=["left"] * len(df.columns))

def table(item, path, filter_column=None, filter_value=None):
    try:
        df = pd.read_csv(item['table'], delimiter=item['delimiter'], engine="python", on_bad_lines="skip")
        if filter_column and filter_value:
            if filter_column in df.columns and filter_value in df[filter_column].values:
                df = df[df[filter_column] == filter_value]
                df = df.drop(columns=[filter_column])
        save_path = _save_csv(df, item, path)
        excel_save_path = _save_excel(df, save_path)
        _format_excel(excel_save_path)
        return table_to_markdown(item, filter_column, filter_value)
    except pd.errors.ParserError as e:
        print(f"[PYTHON][table.py] Error reading table from {item['table']}: {e}")