import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def graph(item, path, filter_column=None, filter_value=None):
    results = []
    if item.get("graph"):
        df = pd.read_csv(item['source'], delimiter=item['delimiter'], engine="python", on_bad_lines="skip")
        # Apply filtering if specified
        if filter_column and filter_value:
            if filter_column in df.columns and filter_value in df[filter_column].values:
                df = df[df[filter_column] == filter_value]
            else:
                return results
        x = item.get('x')
        y = item.get('y')
        legend = item.get('legend')
        description = item.get('description', '')
        graph_type = item.get('graph', '').lower()
        img_name = os.path.splitext(os.path.basename(item['source']))[0] + '.png'
        img_path = os.path.join(path, img_name)

        scale = item.get("scale", 1)
        figsize = (10 * scale, 6 * scale)
        background = item.get("background", "white")
        fig = plt.figure(figsize=figsize, facecolor=background)
        fig.patch.set_edgecolor(item.get("border", 'black'))
        fig.patch.set_linewidth(1 * scale)
        if graph_type == 'linechart':
            if legend and legend in df.columns:
                for key, grp in df.groupby(legend):
                    plt.plot(grp[x], grp[y], label=key)
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
            else:
                plt.plot(df[x], df[y])
        elif graph_type == 'barchart':
            if legend and legend in df.columns:
                # Grouped bar chart
                unique_legends = df[legend].unique()
                x_vals = df[x].unique()
                x_indices = np.arange(len(x_vals))
                bar_width = 0.8 / len(unique_legends) if len(unique_legends) > 0 else 0.8
                for i, l_val in enumerate(unique_legends):
                    grp = df[df[legend] == l_val]
                    # Align y values with x_vals
                    y_vals = [grp[grp[x] == xv][y].values[0] if xv in grp[x].values else 0 for xv in x_vals]
                    plt.bar(x_indices + i * bar_width, y_vals, width=bar_width, label=str(l_val))
                plt.xticks(x_indices + bar_width * (len(unique_legends)-1)/2, x_vals)
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
            else:
                plt.bar(df[x], df[y])
        # You can extend with more graph types if needed
        plt.xlabel(x)
        plt.ylabel(y)
        padding_percent = 0.12  # 12% padding on all sides
        # Dynamically adjust right padding based on legend label length
        right_pad = 0.85
        if legend and legend in df.columns:
            labels = [str(l) for l in df[legend].unique()]
            max_label_len = max((len(label) for label in labels), default=0)
            right_pad = max(0.85 - 0.005 * max_label_len, 0.75)  # Do not go below 0.75
        plt.tight_layout(rect=[0, 0, right_pad, 1])
        plt.subplots_adjust(
            left=padding_percent/(3/2),
            right=right_pad,
            top=1 - padding_percent/2,
            bottom=padding_percent
        )
        plt.savefig(img_path)
        plt.close()