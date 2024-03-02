import random
import matplotlib.pyplot as plt


def number_from_normal_curve(min_value, max_value, mu, sigma):
    """
    Generate a random number from a normal distribution within a specified range.

    Parameters:
        min_value (float): Minimum value of the range.
        max_value (float): Maximum value of the range.
        mu (float): Mean of the normal distribution.
        sigma (float): Standard deviation of the normal distribution.

    Returns:
        float: Random number from the normal distribution within the specified range.
    """
    while True:
        number = random.normalvariate(mu, sigma)
        if min_value <= number <= max_value:
            return round(number)


# Parameters
min_value = 2
max_value = 14
mu = 8  # Mean of the normal distribution
sigma = 2  # Standard deviation of the normal distribution
num_samples = 100000

# Generate 100 numbers from the normal curve
numbers = [number_from_normal_curve(
    min_value, max_value, mu, sigma) for _ in range(num_samples)]

# Plotting
plt.hist(numbers, bins=50, density=True, alpha=0.6, color='g')
plt.title('Histogram of Numbers from Normal Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
