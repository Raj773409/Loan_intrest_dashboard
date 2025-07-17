
# Streamlit-based web dashboard for daily loan and interest tracking
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data (you'll upload the Excel file)
@st.cache_data
def load_data(file):
    df = pd.read_excel(file, sheet_name="Transactions")
    freq_df = pd.read_excel(file, sheet_name="Customer Frequency")
    return df, freq_df

st.title("📊 Loan & Interest Dashboard")

uploaded_file = st.file_uploader("Upload Your Excel File", type=["xlsx"])

if uploaded_file:
    df, freq_df = load_data(uploaded_file)

    df['Date'] = pd.to_datetime(df['Date'])
    selected_date = st.date_input("Select Date to View", df['Date'].min())
    day_data = df[df['Date'] == pd.to_datetime(selected_date)]

    st.subheader(f"📅 Summary for {selected_date.strftime('%B %d, %Y')}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Debit", f"₹{day_data['Debit'].sum():,.0f}")
    col2.metric("Total Collection", f"₹{day_data['Collection'].sum():,.0f}")
    col3.metric("Interest Paid", f"₹{day_data['Interest Paid'].sum():,.0f}")

    st.markdown("---")
    st.subheader("🚨 Overdue Customers")
    overdue = day_data[day_data['Overdue Flag'] == 'Overdue']
    if not overdue.empty:
        st.dataframe(overdue[['Name of Customer', 'Frequency', 'Debit', 'Collection', 'Overdue Flag']])
    else:
        st.success("No overdue customers today!")

    st.markdown("---")
    st.subheader("📊 Interest Summary by Frequency")
    summary = (
        df.groupby("Frequency")
        .agg(Customers=('Name of Customer', 'nunique'),
             Total_Interest_Paid=('Interest Paid', 'sum'))
        .reset_index()
    )
    st.dataframe(summary)

    st.markdown("---")
    st.subheader("📈 Daily Collection Trend")
    trend = df.groupby("Date")["Collection"].sum().reset_index()
    fig = px.line(trend, x="Date", y="Collection", title="Daily Collection")
    st.plotly_chart(fig)

    st.markdown("---")
    st.subheader("🔍 Full Transaction Table")
    st.dataframe(df)
else:
    st.info("Upload an Excel file with 'Transactions' and 'Customer Frequency' sheets to begin.")
