import pandas as pd


class CSV:
    @staticmethod
    def load(fileName: str) -> pd.DataFrame:
        df = pd.read_csv(fileName)
        return df

    @staticmethod
    def save(df: pd.DataFrame, fileName: str):
        df.to_csv(fileName, index=False)
        pass

    