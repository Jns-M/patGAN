# patGAN

patGAN is a Python tool that allows you to generate synthetic clinical study data in the form of individual synthetic patients. The data is generated using a **GAN** (Generative Adversarial Network) that was trained on a subset of the **Framingham Heart Study** data. The individual patients consist of *continuous* and *binary* demographic and clinical features, including vital parameter measurements, lifestyle choices, and medical history. The generated data is exported to a CSV file.

## Requirements

Before using patGAN, make sure your environment meets the following requirements:

- `Python 3.x` (The tool was tested with Python 3.11)
- Required dependencies (See installation guide below)

## Installation

1. Clone or download this repository to your local machine.

2. Navigate to the root directory of the project.

3. Install the required dependencies from the `requirements.txt` file:

    `pip install -r requirements.txt`

## How to Use

To use patGAN, follow these steps:

1. Make sure you have the required dependencies installed.

2. Open a terminal or command prompt in the root directory of your project.

3. Run the CLI by executing the following command:
    `python patgan.py [OPTIONS]`

4. You can get an overview of all available options by displaying the help section:
    `python patgan.py -h`



## CLI Options

The patGAN CLI supports the following options:

- `-n` or `--n_patients`: Specifies the number of patients to generate. The default value is 100.
- `-o` or `--output`: Specifies the name of the output CSV file. The default name is `generated_patients.csv`

## Examples

Here are some example usages of the patGAN CLI:

1. Generate the default amount of patients (100):
    ```
    python patGAN.py
    ```

2. Generate a specific amount of patients (e.g. 1000):
    ```
    python patGAN.py -n 1000
    ```
        
3. Generate the default amount of patients (100) and specify the output CSV name:
    ```
    python patGAN.py -o custom_name
    ```

4. Generate a specific amount of patients (e.g. 5000) and specify the output CSV name:
    ```
    python patGAN.py -n 5000 -o my_patients
    ```

## Citation

If you find the toolkit useful for your work, please consider citing it.

[![DOI](https://zenodo.org/badge/801514563.svg)](https://zenodo.org/doi/10.5281/zenodo.11259941)