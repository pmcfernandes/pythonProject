import pandas as pd


class CSV:
    @staticmethod
    def load(fileName):
        df = pd.read_csv(fileName)
        return df

    