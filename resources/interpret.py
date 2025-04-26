import os

from table import table
from graph import graph

def interpret(item, path, filter_column=None, filter_value=None):

    # pagebreak
    if item.get("pagebreak"):
        return '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'

    # graph
    if item.get("graph"):
        graph(item, path, filter_column, filter_value)
        return f'![{item.get("description", "")}]({os.path.abspath(os.path.join(path, os.path.splitext(os.path.basename(item['source']))[0] + '.png'))}){{width=110%}}\n'

    # table
    if item.get("table"):
        return table(item, path, filter_column, filter_value)

    # paragraph
    if item.get("paragraph"):
        return item["paragraph"] + "\n"

    # header (1-6)
    for level in range(1, 7):
        if item.get(f"header{level}"):
            return f'{"#" * level} {item.get(f"header{level}")}\n'