import pandas as pd


class CSV:
    @staticmethod
    def load(fileName: str) -> pd.DataFrame:
        df = pd.read_csv(fileName)
        return df

    