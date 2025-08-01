



def payoff(S, K, option_type):

    if option_type == 'call':
        return max(0, S - K)
    elif option_type == 'put':
        return max(0, K - S)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
