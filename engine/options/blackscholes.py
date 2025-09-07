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

    inputs["bs_price"] = price
    return inputs


def blackscholes_greeks(inputs):
    """
    Calculate the Greeks for the Black-Scholes option pricing.

    Args:
        inputs (dict): Dictionary containing the option parameters.

    Returns:
        dict: Updated inputs with the calculated Greeks.
    """
    d1 = (math.log(inputs["S"] / inputs["K"]) + (inputs["r"] + 0.5 * inputs["sigma"] ** 2) * inputs["T"]) / (inputs["sigma"] * math.sqrt(inputs["T"]))
    d2 = d1 - inputs["sigma"] * math.sqrt(inputs["T"])

    delta = norm.cdf(d1) if inputs["option_type"] == "call" else norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (inputs["S"] * inputs["sigma"] * math.sqrt(inputs["T"]))
    theta = (- (inputs["S"] * norm.pdf(d1) * inputs["sigma"]) / (2 * math.sqrt(inputs["T"])) -
             inputs["r"] * inputs["K"] * math.exp(-inputs["r"] * inputs["T"]) * norm.cdf(d2 if inputs["option_type"] == "call" else -d2))
    rho = inputs["K"] * inputs["T"] * math.exp(-inputs["r"] * inputs["T"]) * norm.cdf(d2 if inputs["option_type"] == "call" else -d2)

    inputs["delta"] = delta
    inputs["gamma"] = gamma
    inputs["theta"] = theta
    inputs["rho"] = rho

    vega = inputs["S"] * norm.pdf(d1) * math.sqrt(inputs["T"])
    inputs["vega"] = vega

    return inputs