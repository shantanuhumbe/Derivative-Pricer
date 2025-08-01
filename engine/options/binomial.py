import math
from .common import payoff

def binomial_option_pricing(inputs):

    delta_t = inputs["T"] / inputs["steps"]
    u = math.exp(inputs["sigma"]* math.sqrt(delta_t))
    d = 1 / u

    inputs["p"] = (math.exp(inputs["r"] * delta_t) - d) / (u - d)
    inputs["q"] = 1 - inputs["p"]
    inputs["u"] = u
    inputs["d"] = d
    inputs["delta_t"] = delta_t

    cache = {}
    price = binomial_model(inputs, cache)

    inputs["price"] = price
    inputs["steps"]+= 1
    inputs["T"] = inputs["T"] * 252

    return inputs


def binomial_model(inputs, cache):

    key = (inputs["S"], inputs["steps"])

    if key in cache:
        return cache[key]

    if inputs["steps"] == 0:
        return payoff(inputs["S"], inputs["K"], inputs["option_type"])

    s_up = inputs["S"] * inputs["u"]
    s_down = inputs["S"] * inputs["d"]
    inputs["steps"] = inputs["steps"] - 1
    inputs_up = inputs.copy()
    inputs_down = inputs.copy()
    inputs_up["S"] = s_up
    inputs_down["S"] = s_down
    up = binomial_model(inputs_up, cache)
    down = binomial_model(inputs_down, cache)

    price =  (inputs["p"] * up + inputs["q"] * down) * math.exp(-inputs["r"] * inputs["delta_t"])
    cache[key] = price
    return price
