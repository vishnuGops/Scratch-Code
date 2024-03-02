import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, uniform, expon, poisson, lognorm, chi2, gamma, beta


def number_from_normal_curve(min_value, max_value, mu, sigma):
    while True:
        number = random.normalvariate(mu, sigma)
        if min_value <= number <= max_value:
            return number


def number_from_random(min_value, max_value):
    return random.randint(min_value, max_value)


# Parameters
min_value = 0
max_value = 20
mu = 10  # Mean of the normal distribution
sigma = 2  # Standard deviation of the normal distribution
num_samples = 100000

# Generate 100 numbers from the normal curve
numbers_normal = [number_from_normal_curve(
    min_value, max_value, mu, sigma) for _ in range(num_samples)]
# Generate 100 numbers from a random distribution
numbers_random = [number_from_random(
    min_value, max_value) for _ in range(num_samples)]

# Generate 100 numbers from uniform distribution
numbers_uniform = uniform.rvs(
    size=num_samples, loc=min_value, scale=max_value-min_value)

# Generate 100 numbers from exponential distribution
numbers_exponential = expon.rvs(
    size=num_samples, scale=(max_value-min_value)/mu)

# Generate 100 numbers from Poisson distribution
lambda_poisson = (max_value-min_value)/mu
numbers_poisson = poisson.rvs(mu=lambda_poisson, size=num_samples)

# Generate 100 numbers from log-normal distribution
numbers_lognormal = lognorm.rvs(
    s=sigma, loc=min_value, scale=mu, size=num_samples)

# Generate 100 numbers from chi-square distribution
df_chi2 = 2*mu/sigma**2
numbers_chi2 = chi2.rvs(df=df_chi2, size=num_samples)

# Generate 100 numbers from gamma distribution
a_gamma = (mu**2) / sigma**2
scale_gamma = (sigma**2) / mu
numbers_gamma = gamma.rvs(a=a_gamma, scale=scale_gamma, size=num_samples)

# Generate 100 numbers from beta distribution
alpha_beta = 2
beta_beta = 2
numbers_beta = beta.rvs(a=alpha_beta, b=beta_beta, size=num_samples)

# Plotting
fig, axs = plt.subplots(3, 3, figsize=(20, 10))

# Normal Distribution
axs[0, 0].hist(numbers_normal, bins=50, density=True, alpha=0.6,
               color='g', label='Normal Distribution')
xmin, xmax = axs[0, 0].get_xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, sigma)
axs[0, 0].plot(x, p, 'k', linewidth=2)
axs[0, 0].set_title('Normal Distribution')
axs[0, 0].set_xlabel('Value')
axs[0, 0].set_ylabel('Frequency')
axs[0, 0].grid(True)
axs[0, 0].legend()

# Random Distribution
axs[0, 1].hist(numbers_random, bins=50, density=True, alpha=0.6,
               color='b', label='Random Distribution')
axs[0, 1].set_title('Random Distribution')
axs[0, 1].set_xlabel('Value')
axs[0, 1].set_ylabel('Frequency')
axs[0, 1].grid(True)
axs[0, 1].legend()

# Uniform Distribution
axs[0, 2].hist(numbers_uniform, bins=50, density=True,
               alpha=0.6, color='r', label='Uniform Distribution')
axs[0, 2].set_title('Uniform Distribution')
axs[0, 2].set_xlabel('Value')
axs[0, 2].set_ylabel('Frequency')
axs[0, 2].grid(True)
axs[0, 2].legend()

# Exponential Distribution
axs[1, 0].hist(numbers_exponential, bins=50, density=True,
               alpha=0.6, color='m', label='Exponential Distribution')
axs[1, 0].set_title('Exponential Distribution')
axs[1, 0].set_xlabel('Value')
axs[1, 0].set_ylabel('Frequency')
axs[1, 0].grid(True)
axs[1, 0].legend()

# Poisson Distribution
axs[1, 1].hist(numbers_poisson, bins=50, density=True,
               alpha=0.6, color='c', label='Poisson Distribution')
axs[1, 1].set_title('Poisson Distribution')
axs[1, 1].set_xlabel('Value')
axs[1, 1].set_ylabel('Frequency')
axs[1, 1].grid(True)
axs[1, 1].legend()

# Log-Normal Distribution
axs[1, 2].hist(numbers_lognormal, bins=50, density=True,
               alpha=0.6, color='y', label='Log-Normal Distribution')
axs[1, 2].set_title('Log-Normal Distribution')
axs[1, 2].set_xlabel('Value')
axs[1, 2].set_ylabel('Frequency')
axs[1, 2].grid(True)
axs[1, 2].legend()

# Chi-Square Distribution
axs[2, 0].hist(numbers_chi2, bins=50, density=True, alpha=0.6,
               color='k', label='Chi-Square Distribution')
axs[2, 0].set_title('Chi-Square Distribution')
axs[2, 0].set_xlabel('Value')
axs[2, 0].set_ylabel('Frequency')
axs[2, 0].grid(True)
axs[2, 0].legend()

# Gamma Distribution
axs[2, 1].hist(numbers_gamma, bins=50, density=True, alpha=0.6,
               color='orange', label='Gamma Distribution')
axs[2, 1].set_title('Gamma Distribution')
axs[2, 1].set_xlabel('Value')
axs[2, 1].set_ylabel('Frequency')
axs[2, 1].grid(True)
axs[2, 1].legend()

# Beta Distribution
axs[2, 2].hist(numbers_beta, bins=50, density=True, alpha=0.6,
               color='orange', label='Beta Distribution')
axs[2, 2].set_title('Beta Distribution')
axs[2, 2].set_xlabel('Value')
axs[2, 2].set_ylabel('Frequency')
axs[2, 2].grid(True)
axs[2, 2].legend()

plt.tight_layout()
plt.show()
