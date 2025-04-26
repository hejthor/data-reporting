import os
import pandas

from interpret import interpret
from pandoc import pandoc

def document(document, output_path):
    if document.get('split'):

        print(f"[PYTHON][document.py] Get unique values")
        uniques = set()
        for item in document['contents']:
            if item.get("table"):
                try:
                    dataframe = pandas.read_csv(item['table'], delimiter=item['delimiter'], engine="python", on_bad_lines="skip")
                    if document['split'] in dataframe.columns:
                        uniques.update(dataframe[document['split']].unique())
                except pandas.errors.ParserError as e:
                    print(f"[PYTHON][document.py] Error parsing {item['table']}: {e}")
            if item.get("graph"):
                try:
                    dataframe = pandas.read_csv(item['source'], delimiter=item['delimiter'], engine="python", on_bad_lines="skip")
                    if document['split'] in dataframe.columns:
                        uniques.update(dataframe[document['split']].unique())
                except pandas.errors.ParserError as e:
                    print(f"[PYTHON][document.py] Error parsing {item['source']}: {e}")
        
        print(f"[PYTHON][document.py] Create unique output directories")
        for unique_value in uniques:
            unique_output_path = os.path.join(output_path, str(unique_value), document['title'])
            os.makedirs(unique_output_path, exist_ok=True)
            print(f"[PYTHON][document.py] Running pandoc() for {unique_output_path}")
            pandoc(
                "\n".join([interpret(item, unique_output_path, document['split'], unique_value) for item in document['contents']]),
                document,
                unique_output_path
            )

    else:
        output_path = os.path.join(output_path, document['title'])
        os.makedirs(output_path, exist_ok=True)
        print(f"[PYTHON][document.py] Running pandoc() for {output_path}")
        pandoc(
            "\n".join([interpret(item, output_path) for item in document['contents']]),
            document,
            output_path
        )