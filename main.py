import streamlit as st
from app.components import option_components
from engine.options import binomial

st.title("Derivative Pricer App")

with st.sidebar:
    product_type = st.radio("Select Product to Price",["Option", "Bonds"] )

if product_type == "Option":
    model = st.selectbox("Select Model", ["Black-Scholes", "Binomial", "Monte Carlo"])
    inputs = option_components.get_option_inputs(model)

    if model == "Binomial" and inputs is not None:

        result = binomial.binomial_option_pricing(inputs)
        option_components.show_binomial_result(result)
