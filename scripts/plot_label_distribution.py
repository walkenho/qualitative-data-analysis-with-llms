from pathlib import Path

import pandas as pd
import typer

from src.plotting import plot_label_distribution

app = typer.Typer(add_completion=False)

DEFAULT_DATA_PATH = Path(__file__).parent.parent / "data" / "raw" / "text_data.csv"
DEFAULT_TARGET_PNG = Path(__file__).parent.parent / "artifacts" / "taxonomy.png"


@app.command()
def main(
    data_path: Path = typer.Option(
        DEFAULT_DATA_PATH, "--data-path", help="CSV file to plot."
    ),
    target_path: Path = typer.Option(
        DEFAULT_TARGET_PNG, "--target-path", help="Path to save the resulting figure to."
    ),
) -> None:
    '''Load data, plot taxonomy, and save the figure to disk.'''

    df = pd.read_csv(data_path)
    fig = plot_label_distribution(df)

    target_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_image(
        target_path,
        width=1400,
        height=1600,
        scale=3,  # multiplies output pixel dimensions (~3x) for a crisp, high-DPI image
    )


if __name__ == '__main__':
    app()
