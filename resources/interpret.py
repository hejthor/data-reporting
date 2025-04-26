import os
import pandas

from table import table as _table
from graph import graph as _graph

def read_csv(source, delimiter, filter_column=None, filter_value=None):
    dataframe = pandas.read_csv(source, delimiter=delimiter, engine="python", on_bad_lines="skip")
    if filter_column and filter_value:
        if filter_column in dataframe.columns and filter_value in dataframe[filter_column].values:
            dataframe = dataframe[dataframe[filter_column] == filter_value]
            dataframe = dataframe.drop(columns=[filter_column])
    return dataframe

def interpret(item, path, filter_column=None, filter_value=None):

    if item.get("pagebreak"): 
        print(f"[PYTHON][interpret.py] Returning page break")
        return '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'

    if item.get("graph"):
        dataframe = read_csv(item["source"], item["delimiter"], filter_column, filter_value)
        print(f"[PYTHON][interpret.py] Running graph()")
        graph = _graph(dataframe, item, path, filter_column, filter_value)
        print(f"[PYTHON][interpret.py] Returning graph")
        return graph

    if item.get("table"):
        dataframe = read_csv(item["table"], item["delimiter"], filter_column, filter_value)
        print(f"[PYTHON][interpret.py] Running table()")
        table = _table(dataframe, item, path, filter_column, filter_value)
        print(f"[PYTHON][interpret.py] Returning table")
        return table

    if item.get("paragraph"):
        print(f"[PYTHON][interpret.py] Returning paragraph")
        return item["paragraph"] + "\n"

    for level in range(1, 7):
        if item.get(f"header{level}"):
            print(f"[PYTHON][interpret.py] Returning header {level}")
            return f'{"#" * level} {item.get(f"header{level}")}\n'