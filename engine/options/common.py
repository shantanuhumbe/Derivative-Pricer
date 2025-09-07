



def payoff(S, K, option_type):

    if option_type == 'call':
        return max(0, S - K)
    elif option_type == 'put':
        return max(0, K - S)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")


def calc_payoffs(inputs, steps = 5, stepsize = 50):
    S = inputs["S"]
    K = inputs["K"]
    option_type = inputs["option_type"]

    payoffs = {}
    for i in range(1,steps):
        S_adj = S + stepsize * i
        payoffs[S_adj] = payoff(S_adj, K, option_type)

    for i in range(1,steps):
        S_adj = S - stepsize * i
        if S_adj > 0:
            payoffs[S_adj] = payoff(S_adj, K, option_type)

    payoffs[S] = payoff(S, K, option_type)
    return payoffs
