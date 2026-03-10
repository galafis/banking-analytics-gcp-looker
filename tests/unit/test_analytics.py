"""
Tests for Banking Analytics Engine.

Author: Gabriel Demetrios Lafis
"""

import pytest
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.services.analytics_engine import BankingAnalytics
from backend.services.data_generator import BankingDataGenerator


# ── Fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def generator():
    return BankingDataGenerator(seed=42)


@pytest.fixture
def small_dataset(generator):
    customers = generator.generate_customers(100)
    transactions = generator.generate_transactions(customers, days_back=90)
    products = generator.generate_products(customers)
    return customers, transactions, products


@pytest.fixture
def analytics(small_dataset):
    customers, transactions, products = small_dataset
    return BankingAnalytics(customers, transactions, products)


# ── Data Generator Tests ─────────────────────────────────────────────

class TestBankingDataGenerator:
    def test_generate_customers(self, generator):
        df = generator.generate_customers(50)
        assert len(df) == 50
        assert 'customer_id' in df.columns
        assert 'segment' in df.columns
        assert 'credit_score' in df.columns
        assert 'income' in df.columns

    def test_customer_segments(self, generator):
        df = generator.generate_customers(500)
        segments = set(df['segment'].unique())
        assert segments.issubset({'Premium', 'Gold', 'Silver', 'Bronze'})

    def test_customer_credit_score_range(self, generator):
        df = generator.generate_customers(200)
        assert df['credit_score'].min() >= 300
        assert df['credit_score'].max() <= 850

    def test_customer_age_range(self, generator):
        df = generator.generate_customers(200)
        assert df['age'].min() >= 18
        assert df['age'].max() <= 80

    def test_generate_transactions(self, generator):
        customers = generator.generate_customers(20)
        txns = generator.generate_transactions(customers, days_back=30)
        assert len(txns) > 0
        assert 'transaction_id' in txns.columns
        assert 'amount' in txns.columns
        assert 'is_fraud' in txns.columns
        assert 'channel' in txns.columns

    def test_generate_products(self, generator):
        customers = generator.generate_customers(20)
        products = generator.generate_products(customers)
        assert len(products) > 0
        assert 'product_type' in products.columns
        assert 'balance' in products.columns

    def test_complete_dataset(self, generator):
        datasets = generator.generate_complete_dataset(50)
        assert 'customers' in datasets
        assert 'transactions' in datasets
        assert 'products' in datasets
        assert len(datasets['customers']) == 50

    def test_reproducibility(self):
        gen1 = BankingDataGenerator(seed=99)
        gen2 = BankingDataGenerator(seed=99)
        c1 = gen1.generate_customers(10)
        c2 = gen2.generate_customers(10)
        assert list(c1['customer_id']) == list(c2['customer_id'])


# ── Daily Transaction Volume Tests ───────────────────────────────────

class TestDailyTransactionVolume:
    def test_returns_dataframe(self, analytics):
        result = analytics.get_daily_transaction_volume()
        assert isinstance(result, pd.DataFrame)
        assert 'date' in result.columns
        assert 'volume' in result.columns

    def test_sorted_by_date(self, analytics):
        result = analytics.get_daily_transaction_volume()
        dates = result['date'].tolist()
        assert dates == sorted(dates)

    def test_positive_volume(self, analytics):
        result = analytics.get_daily_transaction_volume()
        assert (result['volume'] > 0).all()


# ── Transaction Type Distribution Tests ──────────────────────────────

class TestTransactionTypeDistribution:
    def test_returns_dataframe(self, analytics):
        result = analytics.get_transaction_type_distribution()
        assert isinstance(result, pd.DataFrame)
        assert 'transaction_type' in result.columns
        assert 'count' in result.columns

    def test_all_types_present(self, analytics):
        result = analytics.get_transaction_type_distribution()
        assert len(result) > 0


# ── Customer Segment Analysis Tests ──────────────────────────────────

class TestCustomerSegmentAnalysis:
    def test_returns_dataframe(self, analytics):
        result = analytics.get_customer_segment_analysis()
        assert isinstance(result, pd.DataFrame)
        assert 'segment' in result.columns

    def test_has_metrics(self, analytics):
        result = analytics.get_customer_segment_analysis()
        expected_cols = ['avg_balance', 'total_balance', 'customer_count',
                         'avg_income', 'avg_credit_score']
        for col in expected_cols:
            assert col in result.columns, f"Missing column: {col}"


# ── Fraud Statistics Tests ───────────────────────────────────────────

class TestFraudStatistics:
    def test_returns_dict(self, analytics):
        result = analytics.get_fraud_statistics()
        assert isinstance(result, dict)

    def test_has_required_keys(self, analytics):
        result = analytics.get_fraud_statistics()
        required = ['total_transactions', 'fraud_count', 'fraud_rate',
                     'fraud_amount', 'avg_fraud_amount', 'total_amount']
        for key in required:
            assert key in result, f"Missing key: {key}"

    def test_fraud_rate_range(self, analytics):
        result = analytics.get_fraud_statistics()
        assert 0 <= result['fraud_rate'] <= 1

    def test_fraud_count_lte_total(self, analytics):
        result = analytics.get_fraud_statistics()
        assert result['fraud_count'] <= result['total_transactions']


# ── Fraud Trend Tests ────────────────────────────────────────────────

class TestFraudTrend:
    def test_returns_dataframe(self, analytics):
        result = analytics.get_fraud_trend()
        assert isinstance(result, pd.DataFrame)
        assert 'date' in result.columns
        assert 'fraud_rate' in result.columns

    def test_fraud_rate_percentage(self, analytics):
        result = analytics.get_fraud_trend()
        assert (result['fraud_rate'] >= 0).all()
        assert (result['fraud_rate'] <= 100).all()


# ── Product Performance Tests ────────────────────────────────────────

class TestProductPerformance:
    def test_returns_dataframe(self, analytics):
        result = analytics.get_product_performance()
        assert isinstance(result, pd.DataFrame)
        assert 'product_type' in result.columns

    def test_has_metrics(self, analytics):
        result = analytics.get_product_performance()
        assert 'total_balance' in result.columns
        assert 'avg_balance' in result.columns
        assert 'account_count' in result.columns


# ── Channel Analysis Tests ───────────────────────────────────────────

class TestChannelAnalysis:
    def test_returns_dataframe(self, analytics):
        result = analytics.get_channel_analysis()
        assert isinstance(result, pd.DataFrame)
        assert 'channel' in result.columns

    def test_fraud_rate_column(self, analytics):
        result = analytics.get_channel_analysis()
        assert 'fraud_rate' in result.columns


# ── RFM Segmentation Tests ──────────────────────────────────────────

class TestRFMSegmentation:
    def test_returns_dataframe(self, analytics):
        result = analytics.rfm_segmentation()
        assert isinstance(result, pd.DataFrame)

    def test_has_rfm_columns(self, analytics):
        result = analytics.rfm_segmentation()
        for col in ['recency', 'frequency', 'monetary', 'rfm_score', 'segment']:
            assert col in result.columns, f"Missing column: {col}"

    def test_valid_segments(self, analytics):
        result = analytics.rfm_segmentation()
        valid = {'At Risk', 'Regular', 'Loyal', 'Champion'}
        actual = set(result['segment'].dropna().unique())
        assert actual.issubset(valid)

    def test_rfm_score_range(self, analytics):
        result = analytics.rfm_segmentation()
        assert result['rfm_score'].min() >= 3
        assert result['rfm_score'].max() <= 12


# ── Credit Risk Score Tests ──────────────────────────────────────────

class TestCreditRiskScore:
    def test_returns_dataframe(self, analytics):
        result = analytics.credit_risk_score()
        assert isinstance(result, pd.DataFrame)

    def test_has_risk_columns(self, analytics):
        result = analytics.credit_risk_score()
        assert 'risk_score' in result.columns
        assert 'risk_level' in result.columns

    def test_valid_risk_levels(self, analytics):
        result = analytics.credit_risk_score()
        valid = {'Low', 'Medium', 'High', 'Critical'}
        actual = set(result['risk_level'].dropna().unique())
        assert actual.issubset(valid)


# ── Insights Tests ───────────────────────────────────────────────────

class TestGenerateInsights:
    def test_returns_dict(self, analytics):
        result = analytics.generate_insights()
        assert isinstance(result, dict)

    def test_has_insight_keys(self, analytics):
        result = analytics.generate_insights()
        assert 'top_segment' in result
        assert 'top_transaction' in result
        assert 'fraud_rate' in result
        assert 'top_product' in result

    def test_insights_are_strings(self, analytics):
        result = analytics.generate_insights()
        for value in result.values():
            assert isinstance(value, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
