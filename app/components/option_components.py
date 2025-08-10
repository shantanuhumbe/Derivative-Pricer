import streamlit as st

def get_option_inputs(model):
    """
    Function to get user inputs for option pricing based on the selected model.
    """
    st.markdown("## Option Pricing Inputs")
    st.markdown("Customize the parameters below to price your option using the selected engine.")


    with st.container():

        col1, col2 = st.columns(2)
        with col1:
            S = st.number_input(" Spot Price (S)", value=100.0, min_value=0.0, step=0.5)
        with col2:
            K = st.number_input(" Strike Price (K)", value=100.0, min_value=0.0, step=0.5)


        col3, col4 = st.columns(2)
        with col3:
            T = st.number_input(" Time to Maturity (T in days)", value=1.0, min_value=0.0, step=0.05)
        with col4:
            sigma = st.number_input(" Annualized Volatility (σ)", value=0.2, min_value=0.0, max_value=100.0, step=0.01)


        col5, col6 = st.columns(2)
        with col5:
            r = st.number_input(" Risk-Free Rate (r)", value=0.05, min_value=0.0, max_value=1.0, step=0.005)
        with col6:
            option_type = st.radio(" Option Type", ["Call", "Put"], horizontal=True)


        if model == 'Binomial':
            st.markdown("###  Binomial Model Settings")
            steps = st.slider(" Number of Steps", min_value=10, max_value=500, value=100, step=10)
        elif model == 'Monte Carlo':
            st.markdown("###  Monte Carlo Model Settings")
            simulations = st.number_input(" Simulations", value=10000, step=1000, min_value=1000)
        else:
            steps = simulations = None


    st.markdown("---")
    submit = st.button(" Run Pricing Model")

    if submit:
        return {
            "S": S,
            "K": K,
            "T": T/252, # Convert days to years
            "sigma": sigma,
            "r": r,
            "option_type": option_type.lower(),
            "steps": steps if model == 'Binomial' else None,
            "simulations": simulations if model == 'Monte Carlo' else None
        }
    return None

def show_binomial_result(result: dict):
    with st.container():
        st.markdown("## Option Pricing Result (Binomial Model)")
        st.markdown("---")

        # Top level summary
        st.markdown(f"### **Option Price: `{result['price']:.4f}`**")

        st.markdown("#### Input Parameters")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Spot Price (S):** `{result['S']}`")
            st.markdown(f"**Strike Price (K):** `{result['K']}`")
            st.markdown(f"**Time to Maturity (T):** `{result['T']}` days")
            st.markdown(f"**Volatility (σ):** `{result['sigma']}`")
        with col2:
            st.markdown(f"**Risk-Free Rate (r):** `{result['r']}`")
            st.markdown(f"**Option Type:** `{result['option_type'].capitalize()}`")
            st.markdown(f"**Steps (n):** `{result['steps']}`")
            st.markdown(f"**Δt (delta_t):** `{result['delta_t']:.6f}`")

        st.markdown("#### Model Coefficients")
        coef1, coef2 = st.columns(2)
        with coef1:
            st.markdown(f"**Up Factor (u):** `{result['u']:.4f}`")
            st.markdown(f"**Down Factor (d):** `{result['d']:.4f}`")
        with coef2:
            st.markdown(f"**Probability Up (p):** `{result['p']:.4f}`")
            st.markdown(f"**Probability Down (q):** `{result['q']:.4f}`")

        st.markdown("---")

def show_blackscholes_result(result: dict):
    with st.container():
        st.markdown("## Option Pricing Result (Black-Scholes Model)")
        st.markdown("---")

        # Top level summary
        st.markdown(f"### **Option Price: `{result['price']:.4f}`**")

        st.markdown("#### Input Parameters")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Spot Price (S):** `{result['S']}`")
            st.markdown(f"**Strike Price (K):** `{result['K']}`")
            st.markdown(f"**Time to Maturity (T):** `{result['T']}` years")
            st.markdown(f"**Volatility (σ):** `{result['sigma']}`")
        with col2:
            st.markdown(f"**Risk-Free Rate (r):** `{result['r']}`")
            st.markdown(f"**Option Type:** `{result['option_type'].capitalize()}`")

        st.markdown("---")
