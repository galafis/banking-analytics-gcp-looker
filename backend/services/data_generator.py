"""
Banking Data Generator for Analytics Dashboard
Generates realistic banking data for demonstration purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple
import json

class BankingDataGenerator:
    """Generate realistic banking data for analytics dashboard"""
    
    def __init__(self, seed: int = 42):
        """Initialize the data generator with a random seed"""
        np.random.seed(seed)
        random.seed(seed)
        
        # Customer segments
        self.customer_segments = ['Premium', 'Gold', 'Silver', 'Bronze']
        self.segment_weights = [0.1, 0.2, 0.4, 0.3]
        
        # Product types
        self.products = [
            'Conta Corrente', 'Poupança', 'Cartão de Crédito', 
            'Empréstimo Pessoal', 'Financiamento Imobiliário', 
            'Investimentos', 'Seguros', 'Previdência'
        ]
        
        # Transaction types
        self.transaction_types = [
            'PIX', 'TED', 'DOC', 'Débito Automático', 
            'Cartão Débito', 'Cartão Crédito', 'Saque', 'Depósito'
        ]
        
        # Brazilian cities for realistic data
        self.cities = [
            'São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador',
            'Fortaleza', 'Belo Horizonte', 'Manaus', 'Curitiba',
            'Recife', 'Porto Alegre', 'Goiânia', 'Belém'
        ]
    
    def generate_customers(self, num_customers: int = 10000) -> pd.DataFrame:
        """Generate customer data"""
        customers = []
        
        for i in range(num_customers):
            customer = {
                'customer_id': f'CUST_{i+1:06d}',
                'age': np.random.normal(45, 15),
                'income': np.random.lognormal(10, 0.8),
                'segment': np.random.choice(self.customer_segments, p=self.segment_weights),
                'city': np.random.choice(self.cities),
                'account_opening_date': datetime.now() - timedelta(days=np.random.randint(30, 3650)),
                'is_active': np.random.choice([True, False], p=[0.85, 0.15]),
                'credit_score': np.random.normal(650, 100),
                'num_products': np.random.poisson(2.5) + 1
            }
            
            # Adjust income based on segment
            if customer['segment'] == 'Premium':
                customer['income'] *= 3
            elif customer['segment'] == 'Gold':
                customer['income'] *= 2
            elif customer['segment'] == 'Silver':
                customer['income'] *= 1.2
                
            # Ensure realistic ranges
            customer['age'] = max(18, min(80, customer['age']))
            customer['income'] = max(1000, min(500000, customer['income']))
            customer['credit_score'] = max(300, min(850, customer['credit_score']))
            customer['num_products'] = max(1, min(8, customer['num_products']))
            
            customers.append(customer)
        
        return pd.DataFrame(customers)
    
    def generate_transactions(self, customers_df: pd.DataFrame, 
                            days_back: int = 365) -> pd.DataFrame:
        """Generate transaction data for customers"""
        transactions = []
        
        for _, customer in customers_df.iterrows():
            if not customer['is_active']:
                continue
                
            # Number of transactions based on segment
            segment_multiplier = {
                'Premium': 3.0, 'Gold': 2.0, 'Silver': 1.5, 'Bronze': 1.0
            }
            
            num_transactions = int(np.random.poisson(30) * 
                                 segment_multiplier[customer['segment']])
            
            for _ in range(num_transactions):
                transaction_date = datetime.now() - timedelta(
                    days=np.random.randint(0, days_back)
                )
                
                transaction_type = np.random.choice(self.transaction_types)
                
                # Amount based on transaction type and customer segment
                if transaction_type in ['PIX', 'TED', 'DOC']:
                    amount = np.random.lognormal(6, 1.5)
                elif transaction_type in ['Cartão Débito', 'Cartão Crédito']:
                    amount = np.random.lognormal(4, 1)
                elif transaction_type == 'Saque':
                    amount = np.random.choice([50, 100, 200, 500])
                else:
                    amount = np.random.lognormal(5, 1.2)
                
                # Adjust amount based on customer income
                amount *= (customer['income'] / 5000)
                amount = max(1, min(50000, amount))
                
                # Fraud detection (1% of transactions)
                is_fraud = np.random.choice([True, False], p=[0.01, 0.99])
                
                transaction = {
                    'transaction_id': f'TXN_{len(transactions)+1:08d}',
                    'customer_id': customer['customer_id'],
                    'transaction_date': transaction_date,
                    'transaction_type': transaction_type,
                    'amount': round(amount, 2),
                    'is_fraud': is_fraud,
                    'channel': np.random.choice(['Mobile', 'Internet', 'ATM', 'Branch'], 
                                              p=[0.5, 0.3, 0.15, 0.05])
                }
                
                transactions.append(transaction)
        
        return pd.DataFrame(transactions)
    
    def generate_products(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """Generate product holdings for customers"""
        products_data = []
        
        for _, customer in customers_df.iterrows():
            num_products = customer['num_products']
            customer_products = np.random.choice(
                self.products, size=num_products, replace=False
            )
            
            for product in customer_products:
                # Product balance based on type and customer segment
                if product == 'Conta Corrente':
                    balance = np.random.lognormal(8, 1) * (customer['income'] / 10000)
                elif product == 'Poupança':
                    balance = np.random.lognormal(9, 1.2) * (customer['income'] / 8000)
                elif product == 'Investimentos':
                    balance = np.random.lognormal(10, 1.5) * (customer['income'] / 5000)
                else:
                    balance = np.random.lognormal(7, 1) * (customer['income'] / 15000)
                
                balance = max(0, balance)
                
                product_data = {
                    'customer_id': customer['customer_id'],
                    'product_type': product,
                    'balance': round(balance, 2),
                    'opening_date': customer['account_opening_date'] + 
                                  timedelta(days=np.random.randint(0, 365)),
                    'is_active': np.random.choice([True, False], p=[0.9, 0.1])
                }
                
                products_data.append(product_data)
        
        return pd.DataFrame(products_data)
    
    def generate_complete_dataset(self, num_customers: int = 10000) -> Dict[str, pd.DataFrame]:
        """Generate complete banking dataset"""
        print(f"Generating {num_customers} customers...")
        customers_df = self.generate_customers(num_customers)
        
        print("Generating transactions...")
        transactions_df = self.generate_transactions(customers_df)
        
        print("Generating product holdings...")
        products_df = self.generate_products(customers_df)
        
        return {
            'customers': customers_df,
            'transactions': transactions_df,
            'products': products_df
        }

if __name__ == "__main__":
    # Generate sample data
    generator = BankingDataGenerator()
    datasets = generator.generate_complete_dataset(1000)  # Smaller sample for testing
    
    # Save to CSV files
    for name, df in datasets.items():
        df.to_csv(f'../data/{name}.csv', index=False)
        print(f"Saved {name}.csv with {len(df)} records")
    
    # Print summary statistics
    print("\n=== Dataset Summary ===")
    for name, df in datasets.items():
        print(f"\n{name.upper()}:")
        print(f"  Records: {len(df)}")
        print(f"  Columns: {list(df.columns)}")

