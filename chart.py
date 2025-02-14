import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="HAI TIDE Expense Report", layout="wide")

# Add header and description
st.title("HAI TIDE")
st.subheader("Monthly Expense Analysis Dashboard")
st.markdown("""
    👋 **Welcome!** This dashboard helps you visualize expense data.
    
    📊 **How to use:**
    1. Select a month from the dropdown below
    2. Choose your preferred chart type
    3. Hover over the chart to see detailed information
""")

# Load the Excel file
file_path = "Expense_Report_Jul_Dec_2024.xlsx"
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names

# Add containers for better organization
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📅 Step 1: Choose the Month**")
        selected_month = st.selectbox(
            "Which month's data would you like to see?",
            sheet_names,
            help="Select a month to view its expense data"
        )
    
    with col2:
        st.markdown("**📈 Step 2: Select Chart Style**")
        chart_type = st.selectbox(
            "How would you like to view the data?",
            ["Bar", "Line", "Area", "Scatter"],
            help="""
            Bar: Shows individual expenses as columns
            Line: Shows trend of expenses
            Area: Shows filled area under the line
            Scatter: Shows individual expense points
            """
        )

def create_pivot_chart(sheet_name, df, chart_type):
    # Rename columns properly based on the second row
    df.columns = df.iloc[1]
    df = df[2:].reset_index(drop=True)

    # Convert Amount to numeric
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    
    # Filter out the "Total Amount" row
    df = df[df["Name"] != "Total Amount"]

    # Group by Name to get all transactions
    grouped_data = df.groupby('Name')['Amount'].apply(list).to_dict()
    
    # Prepare data for Plotly
    x_positions = []
    y_values = []
    hover_text = []
    
    for name, amounts in grouped_data.items():
        for amount in amounts:
            x_positions.append(name)
            y_values.append(amount)
            hover_text.append(f'{name}<br>RM {amount:,.2f}')  # Simplified hover text
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add traces based on chart type
    if chart_type == "Bar":
        fig.add_trace(go.Bar(
            x=x_positions,
            y=y_values,
            text=[f'RM {y:,.0f}' for y in y_values],
            textposition='outside',
            textfont=dict(size=10),
            hovertext=hover_text,
            hoverinfo='text',
            name='',  # Remove legend label
            marker_color='skyblue'
        ))
    elif chart_type == "Line":
        fig.add_trace(go.Scatter(
            x=x_positions,
            y=y_values,
            text=[f'RM {y:,.0f}' for y in y_values],
            mode='lines+markers+text',
            textposition='top center',
            textfont=dict(size=10),
            hovertext=hover_text,
            hoverinfo='text',
            line=dict(color='skyblue', width=2),
            marker=dict(size=8)
        ))
    elif chart_type == "Area":
        fig.add_trace(go.Scatter(
            x=x_positions,
            y=y_values,
            text=[f'RM {y:,.0f}' for y in y_values],
            mode='lines+markers+text',
            textposition='top center',
            textfont=dict(size=10),
            fill='tozeroy',
            hovertext=hover_text,
            hoverinfo='text',
            line=dict(color='skyblue', width=2),
            marker=dict(size=8)
        ))
    else:  # Scatter
        fig.add_trace(go.Scatter(
            x=x_positions,
            y=y_values,
            text=[f'RM {y:,.0f}' for y in y_values],
            mode='markers+text',
            textposition='top center',
            textfont=dict(size=10),
            hovertext=hover_text,
            hoverinfo='text',
            marker=dict(
                size=12,
                color='skyblue',
                line=dict(width=2)
            )
        ))

    # Update layout with more descriptive labels
    fig.update_layout(
        title={
            'text': f"HAI TIDE<br>Monthly Expense Analysis - {sheet_name}",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Name",  # Simplified axis label
        yaxis_title="Expense Amount (RM)",
        showlegend=False,
        xaxis_tickangle=-45,
        height=600,
        hovermode='closest',
        plot_bgcolor='white',
        margin=dict(t=100, r=50, b=100, l=50)  # Increased margins for labels
    )
    
    # Add grid
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    # Add note on the chart
    fig.add_annotation(
        text="💡 Tip: Hover over points to see details. Double-click to zoom out.",
        xref="paper", yref="paper",
        x=0, y=1.1,
        showarrow=False,
        font=dict(size=10, color="gray")
    )
    
    return fig

# Display the chart with a header
if selected_month:
    st.markdown("### 📊 Expense Visualization")
    df = pd.read_excel(xls, sheet_name=selected_month)
    fig = create_pivot_chart(selected_month, df, chart_type)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("👆 **Interactive Features:**\n"
            "* Click and drag to zoom into specific areas\n"
            "* Double-click to reset the view\n"
            "* Hover over data points to see detailed information")
