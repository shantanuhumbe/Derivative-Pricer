import streamlit as st
from app.components import option_components
from engine.options import binomial, blackscholes

st.title("Derivative Pricer App")

with st.sidebar:
    product_type = st.radio("Select Product to Price",["Option", "Bonds"] )

if product_type == "Option":
    model = st.selectbox("Select Model", ["Black-Scholes", "Binomial", "Monte Carlo"])
    inputs = option_components.get_option_inputs(model)

    if model == "Binomial" and inputs is not None:

        result = binomial.binomial_option_pricing(inputs)
        option_components.show_binomial_result(result)
    elif model == "Black-Scholes" and inputs is not None:
        result = blackscholes.blackscholes_option_pricing(inputs)
        option_components.show_blackscholes_result(result)
    elif model == "Monte Carlo":
        st.warning("Monte Carlo pricing is not yet implemented.")

