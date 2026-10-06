"""Reading and writing tabular data. I/O lives here and nowhere else."""
from pathlib import Path
import pandas as pd
def read_csv(path: Path) -> pd.DataFrame:

    """Read a CSV file into a DataFrame."""
    return pd.read_csv(path)


def write_csv(df: pd.DataFrame, path: Path) -> None:
    """Write a DataFrame to CSV, creating parent folders as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
