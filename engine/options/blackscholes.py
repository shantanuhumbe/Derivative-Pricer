import math
from scipy.stats import norm


def blackscholes_option_pricing(inputs):
    """
    Calculate the Black-Scholes option pricing.

    Args:
        inputs (dict): Dictionary containing the option parameters.

    Returns:
        dict: Updated inputs with the calculated option price.
    """
    d1 = (math.log(inputs["S"] / inputs["K"]) + (inputs["r"] + 0.5 * inputs["sigma"] ** 2) * inputs["T"]) / (inputs["sigma"] * math.sqrt(inputs["T"]))
    d2 = d1 - inputs["sigma"] * math.sqrt(inputs["T"])

    if inputs["option_type"] == "call":
        price = (inputs["S"] * norm.cdf(d1) - inputs["K"] * math.exp(-inputs["r"] * inputs["T"]) * norm.cdf(d2))
    else:
        price = (inputs["K"] * math.exp(-inputs["r"] * inputs["T"]) * norm.cdf(-d2) - inputs["S"] * norm.cdf(-d1))

    inputs["price"] = price
    return inputs