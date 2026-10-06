"""Pure transformations: data in, data out, no side effects."""
import pandas as pd


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase names, strip whitespace, spaces become underscores."""
    out = df.copy()
    out.columns = [c.strip().lower().replace(" ", "_") for c in out.columns]
    return out

