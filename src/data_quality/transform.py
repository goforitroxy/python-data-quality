"""Pure transformations: data in, data out, no side effects."""
import pandas as pd


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase names, strip whitespace, spaces become underscores."""
    out = df.copy()
    out.columns = [c.strip().lower().replace(" ", "_") for c in out.columns]
    return out



def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from all text columns."""
    out = df.copy()
    text_cols = out.select_dtypes(include=["object", "string"]).columns
    out[text_cols] = out[text_cols].apply(lambda s: s.str.strip())
    return out
