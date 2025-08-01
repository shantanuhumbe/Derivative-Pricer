import streamlit as st

def get_option_inputs(model):
    """
    Function to get user inputs for option pricing based on the selected model.
    """
    st.markdown("## Option Pricing Inputs")
    st.markdown("Customize the parameters below to price your option using the selected engine.")

    # Nice container card style
    with st.container():
        # Row 1
        col1, col2 = st.columns(2)
        with col1:
            S = st.number_input(" Spot Price (S)", value=100.0, min_value=0.0, step=0.5)
        with col2:
            K = st.number_input(" Strike Price (K)", value=100.0, min_value=0.0, step=0.5)

        # Row 2
        col3, col4 = st.columns(2)
        with col3:
            T = st.number_input(" Time to Maturity (T in days)", value=1.0, min_value=0.0, step=0.05)
        with col4:
            sigma = st.number_input(" Volatility (σ)", value=0.2, min_value=0.0, max_value=1.0, step=0.01)

        # Row 3
        col5, col6 = st.columns(2)
        with col5:
            r = st.number_input(" Risk-Free Rate (r)", value=0.05, min_value=0.0, max_value=1.0, step=0.005)
        with col6:
            option_type = st.radio(" Option Type", ["Call", "Put"], horizontal=True)

        # Engine-specific inputs
        if model == 'Binomial':
            st.markdown("###  Binomial Model Settings")
            steps = st.slider(" Number of Steps", min_value=10, max_value=500, value=100, step=10)
        elif model == 'Monte Carlo':
            st.markdown("###  Monte Carlo Model Settings")
            simulations = st.number_input(" Simulations", value=10000, step=1000, min_value=1000)
        else:
            steps = simulations = None

    # Submit
    st.markdown("---")
    submit = st.button(" Run Pricing Model")

    if submit:
        return {
            "S": S,
            "K": K,
            "T": T,
            "sigma": sigma,
            "r": r,
            "option_type": option_type.lower(),
            "steps": steps if model == 'Binomial' else None,
            "simulations": simulations if model == 'Monte Carlo' else None
        }
    return None
