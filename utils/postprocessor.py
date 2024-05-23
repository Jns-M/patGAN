import pandas as pd
from joblib import load
from sklearn.preprocessing import StandardScaler

from utils.configparser import ConfigParser


class PostProcessor:
    def __init__(self, config_parser):
        self.__config_parser: ConfigParser = config_parser

        self.__continuous_scaler = StandardScaler(with_mean=True, with_std=True)
        self.__discrete_count_scaler = StandardScaler(with_mean=False, with_std=True)

        self.__continuous_cols = self.__config_parser.get_continuous_cols()
        self.__discrete_count_cols = self.__config_parser.get_discrete_count_cols()
        self.__binary_cols = self.__config_parser.get_binary_cols()

        self.__integer_cols = self.__config_parser.get_integer_cols()
        self.__two_dec_cols = self.__config_parser.get_two_dec_cols()
        self.__ptfive_cols = self.__config_parser.get_ptfive_cols()

        self.__smoker_col = self.__config_parser.get_smoker_col()
        self.__cigs_per_day_col = self.__config_parser.get_cigs_per_day_col()
        self.__sys_bp_col = self.__config_parser.get_sys_bp_col()
        self.__dia_bp_col = self.__config_parser.get_dia_bp_col()

    def fit_transform(self, data: pd.DataFrame):
        data_postprocessed = data.copy()

        data_postprocessed = self.round_cols(data_postprocessed, self.__integer_cols, 1)
        data_postprocessed = self.round_cols(data_postprocessed, self.__ptfive_cols, 0.5)
        data_postprocessed = self.round_cols(data_postprocessed, self.__two_dec_cols, 0.01)

        for col in data_postprocessed.columns:
            data_postprocessed[col] = data_postprocessed[col].apply(lambda x: max(0, x))

        if self.__binary_cols is not None:
            for col in self.__binary_cols:
                data_postprocessed[col] = data_postprocessed[col].apply(
                    lambda x: 0 if x < 0.5 else 1
                )

        return data_postprocessed

    def round_cols(self, data, cols, round_to):
        if cols is not None:
            for col in cols:
                data[col] = data[col].apply(lambda x: round(x / round_to) * round_to)
        return data

    def reverse_scaling(self, data: pd.DataFrame, scale_binary=True):
        data_restored = data.copy()
        if self.__continuous_scaler is not None:
            data_restored[self.__continuous_cols] = self.__continuous_scaler.inverse_transform(
                data_restored[self.__continuous_cols]
            )
        if self.__discrete_count_scaler is not None:
            data_restored[self.__discrete_count_cols] = (
                self.__discrete_count_scaler.inverse_transform(
                    data_restored[self.__discrete_count_cols]
                )
            )
        if scale_binary and self.__binary_cols is not None:
            for col in self.__binary_cols:
                data_restored[col] = data_restored[col].apply(lambda x: 0 if x < 0.5 else 1)

        return data_restored

    def filter(self, data: pd.DataFrame, n_samples):
        cond_1 = (data[self.__smoker_col] == 0) & (data[self.__cigs_per_day_col] > 0)
        cond_2 = (data[self.__smoker_col] == 1) & (data[self.__cigs_per_day_col] == 0)
        cond_3 = data[self.__sys_bp_col] < data[self.__dia_bp_col]
        conditions = cond_1 | cond_2 | cond_3
        data = data[~conditions]

        try:
            data = data.sample(n_samples)
            data.reset_index(drop=True, inplace=True)
            return data
        except ValueError:
            print("\nERROR: Not enough samples to filter, please try again.")

    def load_scalers(self, continuous_scaler_path, discrete_count_scaler_path):
        self.__continuous_scaler = load(continuous_scaler_path)
        self.__discrete_count_scaler = load(discrete_count_scaler_path)
