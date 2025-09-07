import pandas as pd
import numpy as np
from scipy.stats import norm
from .common import payoff


def monte_carlo_option_pricing(inputs):
    """
    Calculate the option pricing using the Monte Carlo simulation method.

    Args:
        inputs (dict): Dictionary containing the option parameters.

    Returns:
        dict: Updated inputs with the calculated option price.
    """
    S = inputs["S"]
    K = inputs["K"]
    T = inputs["T"]
    sigma = inputs["sigma"]
    r = inputs["r"]
    option_type = inputs["option_type"]
    simulations = inputs["simulations"]
    steps = inputs["steps"]
    print(inputs)
    payoffs = []
    all_paths = []
    for _ in range(simulations):
        path = run_simulations(S, K, T, r, sigma, option_type, steps)
        payoffs.append(payoff(path[-1], K, option_type) * np.exp(-r * T))
        all_paths.append(path)
    price = np.mean(payoffs)
    inputs["mc_price"] = price
    inputs["mc_paths"] = all_paths  # Add all paths for frontend
    return inputs


def run_simulations(S, K, T, r, sigma, option_type, n):
    del_t = T / n
    st = S
    path = [S]
    for i in range(n):
        st *= np.exp((r - 0.5 * sigma ** 2) * del_t + sigma * np.sqrt(del_t) * norm.rvs(loc=0, scale=1))
        path.append(st)
    return path
