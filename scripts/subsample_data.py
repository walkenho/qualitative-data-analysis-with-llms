from pathlib import Path

import pandas as pd
import typer

app = typer.Typer(add_completion=False)

RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw" / "text_data.csv"
INTERIM_DATA_DIR = Path(__file__).parent.parent / "data" / "interim"


@app.command()
def main(
    n: int = typer.Argument(..., help="Number of rows to subsample."),
) -> None:
    """Subsample N rows from data/raw/text_data.csv and save to data/interim/."""
    df = pd.read_csv(RAW_DATA_PATH)
    sampled = df.sample(n, random_state=42)

    INTERIM_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = INTERIM_DATA_DIR / f"text_data_subsampled_{n}.csv"
    sampled.to_csv(output_path, index=True)

    typer.echo(f"Saved {len(sampled)} rows to {output_path}")


if __name__ == "__main__":
    app()
