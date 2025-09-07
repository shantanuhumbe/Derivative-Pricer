import streamlit as st
# Inject CSS for full-width layout
st.markdown(
    '''
    <style>
    .block-container {
        padding-left: 100 !important;
        padding-right: 100 !important;
        width: 100vw !important;
        max-width: 90vw !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

from app.components import option_components
from engine.options import binomial, blackscholes, montecarlo
from engine.options.common import calc_payoffs

st.title("Derivative Pricer App")
with st.sidebar:
    product_type = st.radio("Select Product to Price",["Option", "Bonds"] )

if product_type == "Option":
    inputs = option_components.get_option_inputs()
    tab1, tab2 = st.tabs(["Option Price & Payoffs", "Option Greeks"])
    if inputs is not None:
        with tab1:
            inputs["payoff_data"] = calc_payoffs(inputs)
            inputs = binomial.binomial_option_pricing(inputs)
            inputs = blackscholes.blackscholes_option_pricing(inputs)
            inputs = montecarlo.monte_carlo_option_pricing(inputs)
            option_components.show_option_results(inputs)
    else:
        st.info("Please fill in the option parameters and click 'Run Pricing Model'.")
