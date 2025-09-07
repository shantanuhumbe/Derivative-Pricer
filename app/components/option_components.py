import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def get_option_inputs():
    """
    Function to get user inputs for option pricing in a single styled box with custom background.
    """
    st.markdown("Customize the parameters below to price your option.")

    row1_col1, row1_col2, row1_col3, row1_col4, row_col5 = st.columns(5)
    with row1_col1:
        S = st.number_input("Spot Price (S)", value=100.0, min_value=0.0, step=50.0)
    with row1_col2:
        K = st.number_input("Strike Price (K)", value=100.0, min_value=0.0, step=50.0)
    with row1_col3:
        T = st.number_input("Time to Maturity (T in days)", value=1.0, min_value=0.0, step=0.05)
    with row1_col4:
        sigma = st.number_input("Annualized Volatility (σ)", value=0.2, min_value=0.0, max_value=100.0, step=0.01)
    with row_col5:
        r = st.number_input("Risk-Free Rate (r)", value=0.05, min_value=0.0, max_value=1.0, step=0.01)

    # Second row: Option type, steps, simulations
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1:
        option_type = st.radio("Option Type", ["Call", "Put"], horizontal=True)
    with row2_col2:
        steps = st.slider("Number of Steps", min_value=10, max_value=500, value=100, step=10)
    with row2_col3:
        simulations = st.number_input("Simulations", value=10000, step=1, min_value=10)

    st.markdown("---")
    submit = st.button("Run Pricing Model")

    if submit:
        return {
            "S": S,
            "K": K,
            "T": T/252, # Convert days to years
            "sigma": sigma,
            "r": r,
            "option_type": option_type.lower(),
            "steps": steps,
            "simulations": simulations
        }
    return None

def show_option_results(result: dict):
    # Create 2x2 layout using Streamlit columns
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    # Block 1 (row1_col1): Model and Price (two columns)
    with row1_col1:
            model_results = {"Black-Scholes": result.get("bs_price", None),
                             "Binomial": result.get("binomial_price", None),
                             "Monte Carlo": result.get("mc_price", None)}
            model_df = pd.DataFrame(model_results.items(), columns=["Model", "Price"])
            model_df["Price"] = model_df["Price"].apply(lambda x: f"{x
            :.4f}" if x is not None else "-")
            st.markdown("**Model Prices:**")
            st.table(model_df.set_index("Model"))

    # Block 2 (row1_col2): Reserved for one graph (placeholder)
    with row1_col2:
        payoff_data = result.get("payoff_data", None)
        payoff_df = pd.DataFrame(payoff_data.items(), columns=["Spot","Payoff"])
        payoff_df = payoff_df.sort_values(by="Spot")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=payoff_df["Spot"],
            y=payoff_df["Payoff"],
            mode='lines',
            line=dict(color='cyan', width=2),
            name='Payoff'
        ))
        fig.update_layout(
            template='plotly_dark',
            title='Option Payoff at Maturity',
            xaxis_title='Spot Price at Maturity',
            yaxis_title='Payoff',
            legend=dict(font=dict(color='white')),
            margin=dict(l=10, r=10, t=40, b=10),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

        # You can add a graph here in the future

    # Block 3 (row2_col1): Monte Carlo paths graph
    with row2_col1:
        print(result.keys())
        if "mc_paths" in result and result["mc_paths"]:
            n_show = min(50, len(result["mc_paths"]))
            fig = go.Figure()
            for i, path in enumerate(result["mc_paths"][:n_show]):
                fig.add_trace(go.Scatter(
                    y=path,
                    mode='lines',
                    line=dict(width=1),
                    opacity=0.6,
                    name=f'Path {i+1}',
                    showlegend=False
                ))
            fig.add_trace(go.Scatter(
                x=list(range(len(result["mc_paths"][0]))),
                y=[result["K"]]*len(result["mc_paths"][0]),
                mode='lines',
                line=dict(color='red', dash='dash', width=2),
                name='Strike Price',
                showlegend=True
            ))
            fig.update_layout(
                template='plotly_dark',
                title='Monte Carlo Simulation Paths',
                xaxis_title='Time Step',
                yaxis_title='Asset Price',
                legend=dict(font=dict(color='white')),
                margin=dict(l=10, r=10, t=40, b=10),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No simulation paths available for chart.")

    # Block 4 (row2_col2): Empty for now
    with row2_col2:
        if "mc_paths" in result and result["mc_paths"]:
            final_prices = [path[-1] for path in result["mc_paths"]]
            hist_fig = go.Figure()
            hist_fig.add_trace(go.Histogram(
                x=final_prices,
                nbinsx=30,
                marker_color='cyan',
                opacity=0.75,
                name='Final Prices'
            ))
            hist_fig.update_layout(
                template='plotly_dark',
                title='Distribution of Stock Prices at Maturity',
                xaxis_title='Stock Price at Maturity',
                yaxis_title='Frequency',
                legend=dict(font=dict(color='white')),
                margin=dict(l=10, r=10, t=40, b=10),
                height=300
            )
            st.plotly_chart(hist_fig, use_container_width=True)
