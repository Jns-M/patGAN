import numpy as np


def generate_noise(batch_size, latent_dim):
    noise = np.random.normal(0, 1, size=(batch_size, latent_dim))
    noise = noise.astype(np.float32)
    return noise
