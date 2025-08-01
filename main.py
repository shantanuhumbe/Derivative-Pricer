import streamlit as st
from app.components import option_components
from engine.options.binomial import binomial_option_pricing

st.title("Welcome to Derivative Pricer App")

with st.sidebar:
    product_type = st.radio("Select Product to Price",["Option", "Bonds"] )

if product_type == "Option":
    model = st.selectbox("Select Model", ["Black-Scholes", "Binomial", "Monte Carlo"])
    inputs = option_components.get_option_inputs(model)

    if model == "Binomial":
        binomial = binomial.binomial_option_pricing(inputs)
        print("Binomial Option Pricing Result:", binomial)
