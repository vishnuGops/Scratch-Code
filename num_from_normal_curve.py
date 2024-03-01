import random


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


# Example usage
min_value = 0
max_value = 12
mu = 6  # Mean of the normal distribution
sigma = 2  # Standard deviation of the normal distribution

random_number = number_from_normal_curve(min_value, max_value, mu, sigma)
print("Random number from normal curve:", random_number)
