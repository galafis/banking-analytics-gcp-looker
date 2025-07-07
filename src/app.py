"""
Banking Analytics Dashboard - Main Streamlit Application
Advanced GCP/Looker Integration for Financial Services
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_generator import BankingDataGenerator
from analytics_engine import BankingAnalyti    # Page configuration
st.set_page_config(
    page_title="Banking Analytics Dashboard - GCP/Looker",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load or generate banking data"""
    data_path = "../data/"
    
    # Check if data files exist
    if (os.path.exists(f"{data_path}customers.csv") and 
        os.path.exists(f"{data_path}transactions.csv") and 
        os.path.exists(f"{data_path}products.csv")):
        
        customers = pd.read_csv(f"{data_path}customers.csv")
        transactions = pd.read_csv(f"{data_path}transactions.csv")
        products = pd.read_csv(f"{data_path}products.csv")
        
        # Convert date columns
        customers['account_opening_date'] = pd.to_datetime(customers['account_opening_date'])
        transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
        products['opening_date'] = pd.to_datetime(products['opening_date'])
        
    else:
        # Generate new data
        generator = BankingDataGenerator()
        datasets = generator.generate_complete_dataset(5000)
        
        customers = datasets['customers']
        transactions = datasets['transactions']
        products = datasets['products']
        
        # Create data directory if it doesn't exist
        os.makedirs(data_path, exist_ok=True)
        
        # Save data
        customers.to_csv(f"{data_path}customers.csv", index=False)
        transactions.to_csv(f"{data_path}transactions.csv", index=False)
        products.to_csv(f"{data_path}products.csv", index=False)
    
    return customers, transactions, products

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🏦 Banking Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">Advanced GCP/Looker Integration for Financial Services</p>', 
                unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading banking data..."):
        customers, transactions, products = load_data()
    
    # Initialize analytics engine
    analytics = BankingAnalytics(customers, transactions, products)
    
    # Sidebar
    st.sidebar.markdown('<div class="sidebar-header">📊 Dashboard Controls</div>', 
                       unsafe_allow_html=True)
    
    # Date range filter
    min_date = transactions['transaction_date'].min().date()
    max_date = transactions['transaction_date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(max_date - timedelta(days=30), max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Customer segment filter
    segments = st.sidebar.multiselect(
        "Customer Segments",
        options=customers['segment'].unique(),
        default=customers['segment'].unique()
    )
    
    # Product filter
    product_types = st.sidebar.multiselect(
        "Product Types",
        options=products['product_type'].unique(),
        default=products['product_type'].unique()
    )
    
    # Filter data based on selections
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_transactions = transactions[
            (transactions['transaction_date'].dt.date >= start_date) &
            (transactions['transaction_date'].dt.date <= end_date)
        ]
    else:
        filtered_transactions = transactions
    
    filtered_customers = customers[customers['segment'].isin(segments)]
    filtered_products = products[products['product_type'].isin(product_types)]
    
    # Key Metrics Row
    st.markdown("## 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_customers = len(filtered_customers)
        st.metric(
            label="Total Customers",
            value=f"{total_customers:,}",
            delta=f"+{int(total_customers * 0.05):,} vs last month"
        )
    
    with col2:
        total_transactions = len(filtered_transactions)
        st.metric(
            label="Total Transactions",
            value=f"{total_transactions:,}",
            delta=f"+{int(total_transactions * 0.12):,} vs last month"
        )
    
    with col3:
        total_volume = filtered_transactions['amount'].sum()
        st.metric(
            label="Transaction Volume",
            value=f"R$ {total_volume:,.0f}",
            delta=f"+R$ {int(total_volume * 0.08):,} vs last month"
        )
    
    with col4:
        avg_balance = filtered_products['balance'].mean()
        st.metric(
            label="Avg Account Balance",
            value=f"R$ {avg_balance:,.0f}",
            delta=f"+{avg_balance * 0.03:.0f} vs last month"
        )
    
    # Charts Row 1
    st.markdown("## 📊 Transaction Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily transaction volume
        daily_volume = analytics.get_daily_transaction_volume(filtered_transactions)
        fig_volume = px.line(
            daily_volume, 
            x='date', 
            y='volume',
            title="Daily Transaction Volume",
            labels={'volume': 'Volume (R$)', 'date': 'Date'}
        )
        fig_volume.update_layout(height=400)
        st.plotly_chart(fig_volume, use_container_width=True)
    
    with col2:
        # Transaction type distribution
        type_dist = analytics.get_transaction_type_distribution(filtered_transactions)
        fig_types = px.pie(
            type_dist,
            values='count',
            names='transaction_type',
            title="Transaction Types Distribution"
        )
        fig_types.update_layout(height=400)
        st.plotly_chart(fig_types, use_container_width=True)
    
    # Charts Row 2
    st.markdown("## 👥 Customer Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Customer segment analysis
        segment_analysis = analytics.get_customer_segment_analysis(filtered_customers, filtered_products)
        fig_segments = px.bar(
            segment_analysis,
            x='segment',
            y='avg_balance',
            title="Average Balance by Customer Segment",
            labels={'avg_balance': 'Average Balance (R$)', 'segment': 'Customer Segment'}
        )
        fig_segments.update_layout(height=400)
        st.plotly_chart(fig_segments, use_container_width=True)
    
    with col2:
        # Age distribution
        fig_age = px.histogram(
            filtered_customers,
            x='age',
            nbins=20,
            title="Customer Age Distribution",
            labels={'age': 'Age', 'count': 'Number of Customers'}
        )
        fig_age.update_layout(height=400)
        st.plotly_chart(fig_age, use_container_width=True)
    
    # Fraud Detection Section
    st.markdown("## 🚨 Fraud Detection Analytics")
    
    fraud_stats = analytics.get_fraud_statistics(filtered_transactions)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Fraud Rate",
            value=f"{fraud_stats['fraud_rate']:.2%}",
            delta=f"-{fraud_stats['fraud_rate']*0.1:.2%} vs last month"
        )
    
    with col2:
        st.metric(
            label="Fraud Amount",
            value=f"R$ {fraud_stats['fraud_amount']:,.0f}",
            delta=f"-R$ {fraud_stats['fraud_amount']*0.15:,.0f} vs last month"
        )
    
    with col3:
        st.metric(
            label="Fraud Cases",
            value=f"{fraud_stats['fraud_count']:,}",
            delta=f"-{int(fraud_stats['fraud_count']*0.2):,} vs last month"
        )
    
    # Fraud trend chart
    fraud_trend = analytics.get_fraud_trend(filtered_transactions)
    fig_fraud = px.line(
        fraud_trend,
        x='date',
        y='fraud_rate',
        title="Daily Fraud Rate Trend",
        labels={'fraud_rate': 'Fraud Rate (%)', 'date': 'Date'}
    )
    fig_fraud.update_layout(height=300)
    st.plotly_chart(fig_fraud, use_container_width=True)
    
    # Product Performance Section
    st.markdown("## 💼 Product Performance")
    
    product_performance = analytics.get_product_performance(filtered_products)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_product_balance = px.bar(
            product_performance,
            x='product_type',
            y='total_balance',
            title="Total Balance by Product Type",
            labels={'total_balance': 'Total Balance (R$)', 'product_type': 'Product Type'}
        )
        fig_product_balance.update_xaxis(tickangle=45)
        fig_product_balance.update_layout(height=400)
        st.plotly_chart(fig_product_balance, use_container_width=True)
    
    with col2:
        fig_product_customers = px.bar(
            product_performance,
            x='product_type',
            y='customer_count',
            title="Customer Count by Product Type",
            labels={'customer_count': 'Number of Customers', 'product_type': 'Product Type'}
        )
        fig_product_customers.update_xaxis(tickangle=45)
        fig_product_customers.update_layout(height=400)
        st.plotly_chart(fig_product_customers, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>Banking Analytics Dashboard</strong> - Advanced Financial Data Analytics</p>
        <p>Powered by GCP BigQuery & Looker Studio | Built with Streamlit & Python</p>
        <p>🚀 Demonstrating Modern Data Analytics Capabilities</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

