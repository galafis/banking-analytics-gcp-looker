"""
Banking Analytics Engine
Advanced analytics functions for banking data analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class BankingAnalytics:
    """Advanced analytics engine for banking data"""
    
    def __init__(self, customers_df: pd.DataFrame, 
                 transactions_df: pd.DataFrame, 
                 products_df: pd.DataFrame):
        """Initialize analytics engine with data"""
        self.customers = customers_df.copy()
        self.transactions = transactions_df.copy()
        self.products = products_df.copy()
        
        # Ensure datetime columns
        if 'transaction_date' in self.transactions.columns:
            self.transactions['transaction_date'] = pd.to_datetime(self.transactions['transaction_date'])
        if 'account_opening_date' in self.customers.columns:
            self.customers['account_opening_date'] = pd.to_datetime(self.customers['account_opening_date'])
        if 'opening_date' in self.products.columns:
            self.products['opening_date'] = pd.to_datetime(self.products['opening_date'])
    
    def get_daily_transaction_volume(self, transactions_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Calculate daily transaction volume"""
        if transactions_df is None:
            transactions_df = self.transactions
            
        daily_volume = transactions_df.groupby(
            transactions_df['transaction_date'].dt.date
        )['amount'].sum().reset_index()
        
        daily_volume.columns = ['date', 'volume']
        daily_volume['date'] = pd.to_datetime(daily_volume['date'])
        
        return daily_volume.sort_values('date')
    
    def get_transaction_type_distribution(self, transactions_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Get distribution of transaction types"""
        if transactions_df is None:
            transactions_df = self.transactions
            
        type_dist = transactions_df['transaction_type'].value_counts().reset_index()
        type_dist.columns = ['transaction_type', 'count']
        
        return type_dist
    
    def get_customer_segment_analysis(self, customers_df: Optional[pd.DataFrame] = None,
                                    products_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Analyze customer segments"""
        if customers_df is None:
            customers_df = self.customers
        if products_df is None:
            products_df = self.products
            
        # Merge customer and product data
        customer_products = customers_df.merge(products_df, on='customer_id', how='left')
        
        # Calculate segment metrics
        segment_analysis = customer_products.groupby('segment').agg({
            'balance': ['mean', 'sum', 'count'],
            'customer_id': 'nunique',
            'income': 'mean',
            'credit_score': 'mean'
        }).round(2)
        
        # Flatten column names
        segment_analysis.columns = [
            'avg_balance', 'total_balance', 'product_count',
            'customer_count', 'avg_income', 'avg_credit_score'
        ]
        
        return segment_analysis.reset_index()
    
    def get_fraud_statistics(self, transactions_df: Optional[pd.DataFrame] = None) -> Dict:
        """Calculate fraud detection statistics"""
        if transactions_df is None:
            transactions_df = self.transactions
            
        total_transactions = len(transactions_df)
        fraud_transactions = transactions_df[transactions_df['is_fraud'] == True]
        
        fraud_stats = {
            'total_transactions': total_transactions,
            'fraud_count': len(fraud_transactions),
            'fraud_rate': len(fraud_transactions) / total_transactions if total_transactions > 0 else 0,
            'fraud_amount': fraud_transactions['amount'].sum(),
            'avg_fraud_amount': fraud_transactions['amount'].mean() if len(fraud_transactions) > 0 else 0,
            'total_amount': transactions_df['amount'].sum()
        }
        
        return fraud_stats
    
    def get_fraud_trend(self, transactions_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Get daily fraud rate trend"""
        if transactions_df is None:
            transactions_df = self.transactions
            
        daily_fraud = transactions_df.groupby(
            transactions_df['transaction_date'].dt.date
        ).agg({
            'is_fraud': ['sum', 'count']
        }).reset_index()
        
        daily_fraud.columns = ['date', 'fraud_count', 'total_count']
        daily_fraud['fraud_rate'] = (daily_fraud['fraud_count'] / daily_fraud['total_count'] * 100).round(2)
        daily_fraud['date'] = pd.to_datetime(daily_fraud['date'])
        
        return daily_fraud.sort_values('date')
    
    def get_product_performance(self, products_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Analyze product performance"""
        if products_df is None:
            products_df = self.products
            
        product_performance = products_df.groupby('product_type').agg({
            'balance': ['sum', 'mean', 'count'],
            'customer_id': 'nunique'
        }).round(2)
        
        # Flatten column names
        product_performance.columns = [
            'total_balance', 'avg_balance', 'account_count', 'customer_count'
        ]
        
        return product_performance.reset_index()
    
    def get_channel_analysis(self, transactions_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Analyze transaction channels"""
        if transactions_df is None:
            transactions_df = self.transactions
            
        channel_analysis = transactions_df.groupby('channel').agg({
            'amount': ['sum', 'mean', 'count'],
            'is_fraud': 'sum'
        }).round(2)
        
        # Flatten column names
        channel_analysis.columns = [
            'total_volume', 'avg_amount', 'transaction_count', 'fraud_count'
        ]
        
        # Calculate fraud rate by channel
        channel_analysis['fraud_rate'] = (
            channel_analysis['fraud_count'] / channel_analysis['transaction_count'] * 100
        ).round(2)
        
        return channel_analysis.reset_index()
    
    def get_customer_lifetime_value(self, customers_df: Optional[pd.DataFrame] = None,
                                  products_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Calculate customer lifetime value"""
        if customers_df is None:
            customers_df = self.customers
        if products_df is None:
            products_df = self.products
            
        # Merge customer and product data
        customer_products = customers_df.merge(products_df, on='customer_id', how='left')
        
        # Calculate CLV metrics
        clv_analysis = customer_products.groupby('customer_id').agg({
            'balance': 'sum',
            'product_type': 'count',
            'income': 'first',
            'segment': 'first',
            'credit_score': 'first',
            'account_opening_date': 'first'
        }).reset_index()
        
        # Calculate account age in days
        clv_analysis['account_age_days'] = (
            datetime.now() - clv_analysis['account_opening_date']
        ).dt.days
        
        # Simple CLV calculation (balance * products * tenure factor)
        clv_analysis['estimated_clv'] = (
            clv_analysis['balance'] * 
            clv_analysis['product_type'] * 
            (clv_analysis['account_age_days'] / 365 + 1)
        ).round(2)
        
        return clv_analysis
    
    def get_risk_analysis(self, customers_df: Optional[pd.DataFrame] = None,
                         transactions_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Perform risk analysis on customers"""
        if customers_df is None:
            customers_df = self.customers
        if transactions_df is None:
            transactions_df = self.transactions
            
        # Calculate transaction metrics per customer
        customer_transactions = transactions_df.groupby('customer_id').agg({
            'amount': ['sum', 'mean', 'std', 'count'],
            'is_fraud': 'sum'
        }).reset_index()
        
        # Flatten column names
        customer_transactions.columns = [
            'customer_id', 'total_amount', 'avg_amount', 'std_amount', 
            'transaction_count', 'fraud_count'
        ]
        
        # Merge with customer data
        risk_analysis = customers_df.merge(customer_transactions, on='customer_id', how='left')
        
        # Fill NaN values
        risk_analysis = risk_analysis.fillna(0)
        
        # Calculate risk score (simple model)
        risk_analysis['risk_score'] = (
            (risk_analysis['fraud_count'] * 50) +
            (risk_analysis['std_amount'] / risk_analysis['avg_amount'].replace(0, 1) * 10) +
            ((850 - risk_analysis['credit_score']) / 10)
        ).round(2)
        
        # Categorize risk levels
        risk_analysis['risk_level'] = pd.cut(
            risk_analysis['risk_score'],
            bins=[0, 10, 25, 50, 100],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
        
        return risk_analysis
    
    def get_monthly_trends(self, transactions_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Get monthly transaction trends"""
        if transactions_df is None:
            transactions_df = self.transactions
            
        # Create month-year column
        transactions_df['month_year'] = transactions_df['transaction_date'].dt.to_period('M')
        
        monthly_trends = transactions_df.groupby('month_year').agg({
            'amount': ['sum', 'mean', 'count'],
            'is_fraud': 'sum',
            'customer_id': 'nunique'
        }).reset_index()
        
        # Flatten column names
        monthly_trends.columns = [
            'month_year', 'total_volume', 'avg_amount', 'transaction_count',
            'fraud_count', 'active_customers'
        ]
        
        # Convert period back to datetime for plotting
        monthly_trends['date'] = monthly_trends['month_year'].dt.to_timestamp()
        
        # Calculate growth rates
        monthly_trends['volume_growth'] = monthly_trends['total_volume'].pct_change() * 100
        monthly_trends['customer_growth'] = monthly_trends['active_customers'].pct_change() * 100
        
        return monthly_trends.round(2)
    
    def generate_insights(self) -> Dict[str, str]:
        """Generate automated insights from the data"""
        insights = {}
        
        # Customer insights
        top_segment = self.customers['segment'].value_counts().index[0]
        insights['top_segment'] = f"The largest customer segment is {top_segment}"
        
        # Transaction insights
        top_transaction_type = self.transactions['transaction_type'].value_counts().index[0]
        insights['top_transaction'] = f"Most common transaction type is {top_transaction_type}"
        
        # Fraud insights
        fraud_stats = self.get_fraud_statistics()
        insights['fraud_rate'] = f"Current fraud rate is {fraud_stats['fraud_rate']:.2%}"
        
        # Product insights
        product_performance = self.get_product_performance()
        top_product = product_performance.loc[product_performance['total_balance'].idxmax(), 'product_type']
        insights['top_product'] = f"Highest balance product is {top_product}"
        
        return insights

