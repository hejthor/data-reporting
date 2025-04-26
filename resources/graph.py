import matplotlib.pyplot as plt
import os
import numpy as np

def wrap_label(label, width=20):
    # Insert newlines every `width` characters
    import textwrap
    return '\n'.join(textwrap.wrap(str(label), width=width))

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

    # Determine max legend label length (no dynamic sizing)
    legend_labels = []
    if legend and legend in dataframe.columns:
        legend_labels = [str(l) for l in dataframe[legend].unique()]

    print(f"[PYTHON][graph.py] Create figure")
    fig = plt.figure(
        figsize=(10 * scale, 5 * scale),
        facecolor=item.get("background", "white")
    )
    fig.patch.set_edgecolor(item.get("border", 'black'))
    fig.patch.set_linewidth(1 * scale)

    print(f"[PYTHON][graph.py] Plot graph")
    if graph_type == 'linechart':

        if legend and legend in dataframe.columns:
            for key, grp in dataframe.groupby(legend):
                wrapped_label = wrap_label(key)
                plt.plot(grp[x], grp[y], label=wrapped_label)
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
                wrapped_label = wrap_label(l_val)
                plt.bar(x_indices + i * bar_width, y_vals, width=bar_width, label=wrapped_label)
            plt.xticks(x_indices + bar_width * (len(unique_legends)-1)/2, x_vals)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        else:
            plt.bar(dataframe[x], dataframe[y])

    print(f"[PYTHON][graph.py] Add labels")
    plt.xlabel(x)
    plt.ylabel(y)
    padding_percent = 0.12
    # Draw the canvas to populate tick labels
    fig = plt.gcf()
    fig.canvas.draw()
    ax = plt.gca()
    renderer = fig.canvas.get_renderer()
    y_ticklabels = ax.get_yticklabels()
    label_widths = [label.get_window_extent(renderer=renderer).width for label in y_ticklabels if label.get_text()]
    # Base paddings
    left_pad = 0.11
    right_pad = 0.95
    top_pad = 0.92
    bottom_pad = 0.14
    # Dynamically increase left pad for wide y-tick labels
    if label_widths:
        max_label_width = max(label_widths)
        # For every 50px above 40px, add 0.01 to left_pad
        left_pad += max(0, (max_label_width - 40) / 50 * 0.005)
    if legend and legend in dataframe.columns:
        labels = [str(l) for l in dataframe[legend].unique()]
        max_label_len = max((len(label) for label in labels), default=0)
        right_pad = max(0.85 - 0.005 * max_label_len, 0.75)
    plt.subplots_adjust(left=left_pad, right=right_pad, top=top_pad, bottom=bottom_pad)


    print(f"[PYTHON][graph.py] Save image")
    plt.savefig(img_path, bbox_inches=None)
    plt.close()
    print(f"[PYTHON][graph.py] Return markdown")
    return f'![{item.get("title", "")}]({os.path.abspath(img_path)}){{width=110%}}'