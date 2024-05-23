import argparse

import onnxruntime
import pandas as pd

import utils.helpers as helpers
from utils.configparser import ConfigParser
from utils.postprocessor import PostProcessor

MODEL_PATH = "model/model.onnx"
CONFIG_PATH = "config/config.ini"
CONT_SCALER_PATH = "config/continuous_scaler.bin"
DC_SCALER_PATH = "config/discrete_count_scaler.bin"


class PatGAN:
    def __init__(self, config_parser: ConfigParser) -> None:
        self.__model = self.load_model()
        self.__config_parser = config_parser
        self.__postprocessor = PostProcessor(self.__config_parser)
        self.__postprocessor.load_scalers(CONT_SCALER_PATH, DC_SCALER_PATH)

    def load_model(self):
        return onnxruntime.InferenceSession(MODEL_PATH)

    def generate_samples(self, n_samples):
        noise = helpers.generate_noise(n_samples * 3, self.__config_parser.get_latent_dim())
        generated_samples = self.__model.run(None, {"args_0": noise})[0]
        generated_samples = pd.DataFrame(
            generated_samples,
            columns=self.__config_parser.get_continuous_cols()
            + self.__config_parser.get_discrete_count_cols()
            + self.__config_parser.get_binary_cols(),
        )
        generated_samples = self.__postprocessor.reverse_scaling(generated_samples)
        generated_samples = self.__postprocessor.fit_transform(generated_samples)
        generated_samples = self.__postprocessor.filter(generated_samples, n_samples)
        return generated_samples

    def export_samples(self, samples, output):
        samples.to_csv(output, index=False)

    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description="patGAN - Generate synthetic clinical study data in the form of individual patients (CSV file)."
        )
        parser.add_argument(
            "-n",
            "--n_patients",
            metavar="\b",
            type=int,
            default=100,
            help="The number of patients to generate. Default is 100.",
        )
        parser.add_argument("-o", "--output", metavar="\b", help="The name of the output CSV file.")
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    config_parser = ConfigParser(CONFIG_PATH)
    gan = PatGAN(config_parser)
    min_samples, max_samples = config_parser.get_min_samples(), config_parser.get_max_samples()
    args = gan.parse_arguments()

    args.output = args.output or "generated_patients"
    if not args.output.endswith(".csv"):
        args.output += ".csv"
    if args.n_patients < min_samples or args.n_patients > max_samples:
        print(f"\nERROR: The number of patients must be between {min_samples} and {max_samples}.")
    else:
        print(f"\nGenerating {args.n_patients} patients...")
        generated_samples = gan.generate_samples(args.n_patients)
        if generated_samples is None:
            exit(1)
        gan.export_samples(generated_samples, args.output)
        print(f"Generated patients saved to {args.output}")
        print()
        print(generated_samples)
