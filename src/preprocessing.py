import pandas as pd


def preprocess_raw_data(raw_data_file: str) -> pd.DataFrame:
    df_raw = pd.read_csv(raw_data_file)
    df_proc = df_raw.assign(
        date=lambda df: (
            pd.to_datetime(df["date"], format="%d %b %Y").dt.strftime("%Y-%m-%d")
        ),
        amount=lambda df: (
            df.amount.str.extract("([-\d,]+)")
            .replace(",", ".", regex=True)
            .astype(float)
        ),
        savings=lambda df: (
            df.savings.str.extract("([-\d,]+)")
            .replace(",", ".", regex=True)
            .astype(float)
        ),
    )
    return df_proc
