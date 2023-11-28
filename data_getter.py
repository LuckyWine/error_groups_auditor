import pandas as pd

class DataGetter:

    def get_error_groups(self) -> pd.DataFrame:
        df_error_groups = self.get_table_with_error_groups()
        return DataGetter._normalize_rules(df_error_groups)

    @staticmethod
    def _normalize_rules(df_error_groups: pd.DataFrame) -> pd.DataFrame:
        df_error_groups['Rules'] = df_error_groups['Rules'].apply(
            lambda x: x[1:-1].replace('"', '').replace("'", "").split(",")
        )
        return df_error_groups

    @staticmethod
    def get_tracebacks() -> pd.DataFrame:
        # запросы в БД
        return pd.read_excel("tab_tracebacks.xlsx")

    @staticmethod
    def get_table_with_error_groups() -> pd.DataFrame:
        # запросы в БД
        return pd.read_excel("tab_error_groups.xlsx")
