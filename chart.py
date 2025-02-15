import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="HAI TIDE Expense Report", layout="wide")
st.title("HAI TIDE")
st.subheader("Monthly Expense Analysis Dashboard")
st.markdown("👋 **Welcome!** Use the filters below to explore your expenses.")

# Load Data
file_path = "Expense_Report_Jul_Dec_2024.xlsx"
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names

# Sidebar Filters with Improved UI
with st.sidebar:
    selected_month = st.selectbox("📅 Choose Month:", sheet_names)
    df = pd.read_excel(xls, sheet_name=selected_month)
    df.columns = df.iloc[1]
    df = df[2:].reset_index(drop=True)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    payment_modes = df['Payment Mode'].dropna().unique().tolist()
    selected_modes = st.multiselect("💳 Payment Modes:", payment_modes, default=payment_modes)

    expense_types = df['Name'].dropna().unique().tolist()
    selected_types = st.multiselect("💰 Expense Types:", expense_types, default=expense_types)

    chart_type = st.radio("📈 Chart Style:", ["Bar", "Line", "Area", "Scatter"])

# Filter Data
def filter_data(df, modes, types):
    return df[df['Payment Mode'].isin(modes) & df['Name'].isin(types)]

filtered_df = filter_data(df, selected_modes, selected_types)

# Visualization
def create_chart(df, chart_type):
    fig = go.Figure()
    if chart_type == "Bar":
        fig.add_trace(go.Bar(x=df['Name'], y=df['Amount']))
    elif chart_type == "Line":
        fig.add_trace(go.Scatter(x=df['Name'], y=df['Amount'], mode='lines+markers'))
    elif chart_type == "Area":
        fig.add_trace(go.Scatter(x=df['Name'], y=df['Amount'], fill='tozeroy'))
    elif chart_type == "Scatter":
        fig.add_trace(go.Scatter(x=df['Name'], y=df['Amount'], mode='markers'))
    fig.update_layout(title=f"Expenses for {selected_month}", xaxis_title="Expense Type", yaxis_title="Amount")
    return fig

st.plotly_chart(create_chart(filtered_df, chart_type), use_container_width=True)

st.info("👆 Use the sidebar to filter data and explore expense trends interactively.")
