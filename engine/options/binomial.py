import math
from .common import payoff

def binomial_option_pricing(inputs):

    delta_t = inputs["T"] / inputs["steps"]
    u = math.exp(inputs["sigma"]* math.sqrt(delta_t))
    d = 1 / u

    inputs["bi_p"] = (math.exp(inputs["r"] * delta_t) - d) / (u - d)
    inputs["bi_q"] = 1 - inputs["bi_p"]
    inputs["bi_u"] = u
    inputs["bi_d"] = d
    inputs["bi_delta_t"] = delta_t

    cache = {}
    price = binomial_model(inputs, cache)
    inputs["binomial_price"] = price

    return inputs


def binomial_model(inputs, cache):

    key = (inputs["S"], inputs["steps"])

    if key in cache:
        return cache[key]

    if inputs["steps"] == 0:
        return payoff(inputs["S"], inputs["K"], inputs["option_type"])

    s_up = inputs["S"] * inputs["bi_u"]
    s_down = inputs["S"] * inputs["bi_d"]
    inputs["steps"] = inputs["steps"] - 1
    inputs_up = inputs.copy()
    inputs_down = inputs.copy()
    inputs_up["S"] = s_up
    inputs_down["S"] = s_down
    up = binomial_model(inputs_up, cache)
    down = binomial_model(inputs_down, cache)

    price =  (inputs["bi_p"] * up + inputs["bi_q"] * down) * math.exp(-inputs["r"] * inputs["bi_delta_t"])
    cache[key] = price
    return price
