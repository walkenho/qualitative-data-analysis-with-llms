from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw" / "text_data.csv"
TARGET_PNG = Path(__file__).parent.parent / "artifacts" / "taxonomy.png"


def plot_raw_data_distribution() -> None:
    '''Plot taxonomy of raw data file.'''

    df = (pd.read_csv(RAW_DATA_PATH)
            .drop(columns=['code', 'criticality', 'organization', 'question', 'row_index']))

    counts = (
        df.groupby(["label", "subcategory"], sort=False)
        .size()
        .reset_index(name="count")
    )

    # labels ordered by total responses, most to fewest
    label_totals = counts.groupby("label")["count"].sum()
    label_order = label_totals.sort_values(ascending=False).index.tolist()

    counts["label"] = pd.Categorical(counts["label"], categories=label_order, ordered=True)
    counts = counts.sort_values(["label", "count"], ascending=[True, False]).reset_index(drop=True)

    counts["y_pos"] = counts.index[::-1]

    PALETTE = px.colors.qualitative.Safe
    FONT_FAMILY = "Arial, sans-serif"

    fig = go.Figure()
    for i, label in enumerate(label_order):
        sub = counts[counts["label"] == label]
        color = PALETTE[i % len(PALETTE)]
        _ = fig.add_trace(
            go.Bar(
                x=sub["count"],
                y=sub["y_pos"],
                orientation="h",
                marker_color=color,
                name=label,
                width=0.8,
            )
        )

    LABEL_COL_X = 0.00
    PLOT_START_X = 0.42

    for label in label_order:
        sub = counts[counts["label"] == label]
        _ = fig.add_annotation(
            x=LABEL_COL_X, xref="paper", xanchor="left",
            y=sub["y_pos"].max(), yref="y", yanchor="middle",
            text=f"<b>{label}</b>",
            showarrow=False,
            font={"family": FONT_FAMILY, "size": 12},
            align="left",
        )

    for _, row in counts.iterrows():
        _ = fig.add_annotation(
            x=PLOT_START_X, xref="paper", xanchor="right",
            y=row["y_pos"], yref="y", yanchor="middle",
            text=row["subcategory"],
            showarrow=False,
            font={"family": FONT_FAMILY, "size": 11},
            align="right",
            xshift=-6,
        )

    # divider between each label group — limited to the text columns, not the bars
    boundaries = [
        counts.loc[counts["label"] == label, "y_pos"].max() + 0.5
        for label in label_order[1:]
    ]
    for y in boundaries:
        _ = fig.add_shape(
            type="line",
            xref="paper", x0=LABEL_COL_X, x1=PLOT_START_X,
            yref="y", y0=y, y1=y,
            line={"color": "lightgrey", "width": 1},
        )

    _ = fig.update_xaxes(domain=[PLOT_START_X, 1], title="Number of Mentions")
    _ = fig.update_yaxes(showticklabels=False, range=[-1, len(counts)])
    _ = fig.update_layout(
        height=1500,
        margin={"l": 10, "r": 20, "t": 60, "b": 40},
        title="What were survey respondents concerned with?",
        font={"family": FONT_FAMILY, "size": 12},
        showlegend=False,
    )

    fig.write_image(
        TARGET_PNG,
        width=1400,
        height=1600,
        scale=3,  # multiplies output pixel dimensions (~3x) for a crisp, high-DPI image
    ) 

if __name__ == '__main__':
    plot_raw_data_distribution()