import configparser


class ConfigParser:
    def __init__(self, config_path):
        self.__config = configparser.ConfigParser()
        self.__config.read(config_path)
        self.__continuous_cols = self.__config.get("COLUMNS", "continuous_columns").split(",")
        self.__discrete_count_cols = self.__config.get("COLUMNS", "discrete_count_columns").split(
            ","
        )
        self.__binary_cols = self.__config.get("COLUMNS", "binary_columns").split(",")
        self.__integer_cols = self.__config.get("POSTPROCESSING", "integer_columns").split(",")
        self.__two_dec_cols = self.__config.get("POSTPROCESSING", "two_decimal_columns").split(",")
        self.__ptfive_cols = self.__config.get("POSTPROCESSING", "ptfive_round_columns").split(",")
        self.__smoker_col = self.__config.get("POSTPROCESSING", "smoker_column")
        self.__cigs_per_day_col = self.__config.get("POSTPROCESSING", "cigs_per_day_column")
        self.__sys_bp_col = self.__config.get("POSTPROCESSING", "sys_bp_column")
        self.__dia_bp_col = self.__config.get("POSTPROCESSING", "dia_bp_column")
        self.__latent_dim = self.__config.getint("MODEL", "latent_dim")
        self.__min_samples = self.__config.getint("MODEL", "min_samples")
        self.__max_samples = self.__config.getint("MODEL", "max_samples")

    def get_continuous_cols(self):
        return self.__continuous_cols

    def get_discrete_count_cols(self):
        return self.__discrete_count_cols

    def get_binary_cols(self):
        return self.__binary_cols

    def get_integer_cols(self):
        return self.__integer_cols

    def get_two_dec_cols(self):
        return self.__two_dec_cols

    def get_ptfive_cols(self):
        return self.__ptfive_cols

    def get_smoker_col(self):
        return self.__smoker_col

    def get_cigs_per_day_col(self):
        return self.__cigs_per_day_col

    def get_sys_bp_col(self):
        return self.__sys_bp_col

    def get_dia_bp_col(self):
        return self.__dia_bp_col

    def get_latent_dim(self):
        return self.__latent_dim

    def get_min_samples(self):
        return self.__min_samples

    def get_max_samples(self):
        return self.__max_samples
