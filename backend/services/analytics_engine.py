"""
Banking Analytics Engine
Advanced analytics functions for banking data analysis.

Author: Gabriel Demetrios Lafis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class BankingAnalytics:
    """Advanced analytics engine for banking data."""

    def __init__(self, customers_df: pd.DataFrame,
                 transactions_df: pd.DataFrame,
                 products_df: pd.DataFrame):
        self.customers = customers_df.copy()
        self.transactions = transactions_df.copy()
        self.products = products_df.copy()

        if 'transaction_date' in self.transactions.columns:
            self.transactions['transaction_date'] = pd.to_datetime(self.transactions['transaction_date'])
        if 'account_opening_date' in self.customers.columns:
            self.customers['account_opening_date'] = pd.to_datetime(self.customers['account_opening_date'])
        if 'opening_date' in self.products.columns:
            self.products['opening_date'] = pd.to_datetime(self.products['opening_date'])

    def get_daily_transaction_volume(self, transactions_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        if transactions_df is None:
            transactions_df = self.transactions
        daily_volume = transactions_df.groupby(
            transactions_df['transaction_date'].dt.date
        )['amount'].sum().reset_index()
        daily_volume.columns = ['date', 'volume']
        daily_volume['date'] = pd.to_datetime(daily_volume['date'])
        return daily_volume.sort_values('date')

    def get_transaction_type_distribution(self, transactions_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        if transactions_df is None:
            transactions_df = self.transactions
        type_dist = transactions_df['transaction_type'].value_counts().reset_index()
        type_dist.columns = ['transaction_type', 'count']
        return type_dist

    def get_customer_segment_analysis(self, customers_df: Optional[pd.DataFrame] = None,
                                      products_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        if customers_df is None:
            customers_df = self.customers
        if products_df is None:
            products_df = self.products
        customer_products = customers_df.merge(products_df, on='customer_id', how='left')
        segment_analysis = customer_products.groupby('segment').agg({
            'balance': ['mean', 'sum', 'count'],
            'customer_id': 'nunique',
            'income': 'mean',
            'credit_score': 'mean'
        }).round(2)
        segment_analysis.columns = [
            'avg_balance', 'total_balance', 'product_count',
            'customer_count', 'avg_income', 'avg_credit_score'
        ]
        return segment_analysis.reset_index()

    def get_fraud_statistics(self, transactions_df: Optional[pd.DataFrame] = None) -> Dict:
        if transactions_df is None:
            transactions_df = self.transactions
        total_transactions = len(transactions_df)
        fraud_transactions = transactions_df[transactions_df['is_fraud'] == True]
        return {
            'total_transactions': total_transactions,
            'fraud_count': len(fraud_transactions),
            'fraud_rate': len(fraud_transactions) / total_transactions if total_transactions > 0 else 0,
            'fraud_amount': fraud_transactions['amount'].sum() if len(fraud_transactions) > 0 else 0,
            'avg_fraud_amount': fraud_transactions['amount'].mean() if len(fraud_transactions) > 0 else 0,
            'total_amount': transactions_df['amount'].sum()
        }

    def get_fraud_trend(self, transactions_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        if transactions_df is None:
            transactions_df = self.transactions
        daily_fraud = transactions_df.groupby(
            transactions_df['transaction_date'].dt.date
        ).agg({'is_fraud': ['sum', 'count']}).reset_index()
        daily_fraud.columns = ['date', 'fraud_count', 'total_count']
        daily_fraud['fraud_rate'] = (daily_fraud['fraud_count'] / daily_fraud['total_count'] * 100).round(2)
        daily_fraud['date'] = pd.to_datetime(daily_fraud['date'])
        return daily_fraud.sort_values('date')

    def get_product_performance(self, products_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        if products_df is None:
            products_df = self.products
        product_performance = products_df.groupby('product_type').agg({
            'balance': ['sum', 'mean', 'count'],
            'customer_id': 'nunique'
        }).round(2)
        product_performance.columns = [
            'total_balance', 'avg_balance', 'account_count', 'customer_count'
        ]
        return product_performance.reset_index()

    def get_channel_analysis(self, transactions_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        if transactions_df is None:
            transactions_df = self.transactions
        channel_analysis = transactions_df.groupby('channel').agg({
            'amount': ['sum', 'mean', 'count'],
            'is_fraud': 'sum'
        }).round(2)
        channel_analysis.columns = [
            'total_volume', 'avg_amount', 'transaction_count', 'fraud_count'
        ]
        channel_analysis['fraud_rate'] = (
            channel_analysis['fraud_count'] / channel_analysis['transaction_count'] * 100
        ).round(2)
        return channel_analysis.reset_index()

    def rfm_segmentation(self, transactions_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """RFM (Recency, Frequency, Monetary) customer segmentation."""
        if transactions_df is None:
            transactions_df = self.transactions
        reference_date = transactions_df['transaction_date'].max() + timedelta(days=1)
        rfm = transactions_df.groupby('customer_id').agg({
            'transaction_date': lambda x: (reference_date - x.max()).days,
            'amount': ['count', 'sum']
        }).reset_index()
        rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
        for col in ['recency', 'frequency', 'monetary']:
            rfm[f'{col}_score'] = pd.qcut(
                rfm[col].rank(method='first'),
                q=4, labels=[4, 3, 2, 1] if col == 'recency' else [1, 2, 3, 4]
            ).astype(int)
        rfm['rfm_score'] = rfm['recency_score'] + rfm['frequency_score'] + rfm['monetary_score']
        rfm['segment'] = pd.cut(
            rfm['rfm_score'],
            bins=[0, 4, 7, 10, 12],
            labels=['At Risk', 'Regular', 'Loyal', 'Champion']
        )
        return rfm

    def credit_risk_score(self, customers_df: Optional[pd.DataFrame] = None,
                          transactions_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Simple credit risk scoring model."""
        if customers_df is None:
            customers_df = self.customers
        if transactions_df is None:
            transactions_df = self.transactions
        customer_txn = transactions_df.groupby('customer_id').agg({
            'amount': ['sum', 'mean', 'std', 'count'],
            'is_fraud': 'sum'
        }).reset_index()
        customer_txn.columns = ['customer_id', 'total_amount', 'avg_amount', 'std_amount',
                                'txn_count', 'fraud_count']
        risk_df = customers_df.merge(customer_txn, on='customer_id', how='left').fillna(0)
        risk_df['risk_score'] = (
            (risk_df['fraud_count'] * 50) +
            (risk_df['std_amount'] / risk_df['avg_amount'].replace(0, 1) * 10) +
            ((850 - risk_df['credit_score']) / 10)
        ).round(2)
        risk_df['risk_level'] = pd.cut(
            risk_df['risk_score'],
            bins=[-float('inf'), 10, 25, 50, float('inf')],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
        return risk_df

    def generate_insights(self) -> Dict[str, str]:
        insights = {}
        top_segment = self.customers['segment'].value_counts().index[0]
        insights['top_segment'] = f"The largest customer segment is {top_segment}"
        top_type = self.transactions['transaction_type'].value_counts().index[0]
        insights['top_transaction'] = f"Most common transaction type is {top_type}"
        fraud_stats = self.get_fraud_statistics()
        insights['fraud_rate'] = f"Current fraud rate is {fraud_stats['fraud_rate']:.2%}"
        pp = self.get_product_performance()
        top_product = pp.loc[pp['total_balance'].idxmax(), 'product_type']
        insights['top_product'] = f"Highest balance product is {top_product}"
        return insights
