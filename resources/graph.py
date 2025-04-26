import matplotlib.pyplot as plt
import os
import numpy as np

def graph(dataframe, item, path, filter_column=None, filter_value=None):
    
    print(f"[PYTHON][graph.py] Get graph parameters")
    x = item.get('x')
    y = item.get('y')
    legend = item.get('legend')
    graph_type = item.get('graph', '').lower()
    img_name = os.path.splitext(os.path.basename(item['source']))[0] + '.png'
    graphs_path = os.path.join(path, "PNG")
    os.makedirs(graphs_path, exist_ok=True)
    img_path = os.path.join(graphs_path, img_name)
    scale = item.get("scale", 1)

    print(f"[PYTHON][graph.py] Create figure")
    fig = plt.figure(
        figsize=(10 * scale, 6 * scale),
        facecolor=item.get("background", "white")
    )
    fig.patch.set_edgecolor(item.get("border", 'black'))
    fig.patch.set_linewidth(1 * scale)

    print(f"[PYTHON][graph.py] Plot graph")
    if graph_type == 'linechart':

        if legend and legend in dataframe.columns:
            for key, grp in dataframe.groupby(legend):
                plt.plot(grp[x], grp[y], label=key)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        else:
            plt.plot(dataframe[x], dataframe[y])

    elif graph_type == 'barchart':

        if legend and legend in dataframe.columns:
            print(f"[PYTHON][graph.py] Grouped bar chart")
            unique_legends = dataframe[legend].unique()
            x_vals = dataframe[x].unique()
            x_indices = np.arange(len(x_vals))
            bar_width = 0.8 / len(unique_legends) if len(unique_legends) > 0 else 0.8
            for i, l_val in enumerate(unique_legends):
                grp = dataframe[dataframe[legend] == l_val]
                y_vals = [grp[grp[x] == xv][y].values[0] if xv in grp[x].values else 0 for xv in x_vals]
                plt.bar(x_indices + i * bar_width, y_vals, width=bar_width, label=str(l_val))
            plt.xticks(x_indices + bar_width * (len(unique_legends)-1)/2, x_vals)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        else:
            plt.bar(dataframe[x], dataframe[y])

    print(f"[PYTHON][graph.py] Add labels")
    plt.xlabel(x)
    plt.ylabel(y)
    padding_percent = 0.12
    right_pad = 0.85
    if legend and legend in dataframe.columns:
        labels = [str(l) for l in dataframe[legend].unique()]
        max_label_len = max((len(label) for label in labels), default=0)
        right_pad = max(0.85 - 0.005 * max_label_len, 0.75)
    plt.tight_layout(rect=[0, 0, right_pad, 1])
    plt.subplots_adjust(
        left=padding_percent/(3/2),
        right=right_pad,
        top=1 - padding_percent/2,
        bottom=padding_percent
    )

    print(f"[PYTHON][graph.py] Save image")
    plt.savefig(img_path)
    plt.close()

    print(f"[PYTHON][graph.py] Return markdown")
    return f'![]({os.path.abspath(img_path)}){{width=110%}}'