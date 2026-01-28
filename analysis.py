import pandas as pd
import numpy as np
import json

def process_data():
    print("--- Loading and Cleaning Data ---")
    df = pd.read_csv('transactions.csv')
    
    # 1. Cleaning: Convert date and handle missing amounts
    df['date'] = pd.to_datetime(df['date'])
    df = df.dropna(subset=['amount'])
    
    # 2. Cleaning: Fix the "Subsciptions" typo in the description (if any) or just the logic
    # The original generator used 'Subsciptions' as a key and in descriptions sometimes
    df['description'] = df['description'].str.replace('Subsciptions', 'Subscriptions', case=False)
    
    # 3. Categorization
    def categorize(desc):
        desc = desc.lower()
        if any(word in desc for word in ['starbucks', 'mcdonalds', 'pizza', 'cafe', 'eats', 'taco', 'food']):
            return 'Dining'
        if any(word in desc for word in ['uber', 'lyft', 'gas', 'metro', 'parking']):
            return 'Transport'
        if any(word in desc for word in ['netflix', 'spotify', 'amazon prime', 'gym', 'cloud', 'subscription']):
            return 'Subscriptions'
        if 'rent' in desc:
            return 'Rent'
        if any(word in desc for word in ['amazon', 'walmart', 'target', 'apparel', 'electronic', 'depot']):
            return 'Shopping'
        if any(word in desc for word in ['bill', 'electric', 'water', 'internet', 'phone']):
            return 'Utilities'
        return 'Other'

    df['category'] = df['description'].apply(categorize)
    
    # 4. Feature Engineering
    df['month'] = df['date'].dt.strftime('%b')
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    df['is_weekend'] = df['date'].dt.dayofweek >= 5
    
    # --- ANALYSIS TASKS ---
    
    # Task 1: Subscription Audit
    sub_df = df[df['category'] == 'Subscriptions']
    avg_sub_monthly = sub_df.groupby(df['date'].dt.to_period('M'))['amount'].sum().mean()
    
    # Task 2: Weekend Effect
    weekend_avg = df[df['is_weekend']]['amount'].mean()
    weekday_avg = df[~df['is_weekend']]['amount'].mean()
    
    # Task 3: Aggregates for Dashboard
    
    # Monthly Total Spending (Sorted by month)
    monthly_trend = df.groupby(['month_num', 'month'])['amount'].sum().reset_index()
    monthly_trend = monthly_trend.sort_values('month_num')
    
    # Category Breakdown
    category_dist = df.groupby('category')['amount'].sum().reset_index()
    
    # Weekend vs Weekday Total
    weekend_dist = df.groupby('is_weekend')['amount'].sum().reset_index()
    weekend_dist['type'] = weekend_dist['is_weekend'].map({True: 'Weekend', False: 'Weekday'})

    # Recent Transactions
    recent_transactions = df.sort_values('date', ascending=False).head(10)
    
    # Prepare JSON data for website
    output_data = {
        "summary": {
            "total_spent": round(float(df['amount'].sum()), 2),
            "avg_monthly_sub": round(float(avg_sub_monthly), 2),
            "weekend_avg": round(float(weekend_avg), 2),
            "weekday_avg": round(float(weekday_avg), 2),
            "saving_hint": "Your weekend spending is higher!" if weekend_avg > weekday_avg else "Your spending is consistent."
        },
        "monthly_trend": monthly_trend[['month', 'amount']].to_dict(orient='records'),
        "category_distribution": category_dist.to_dict(orient='records'),
        "weekend_vs_weekday": weekend_dist[['type', 'amount']].to_dict(orient='records'),
        "recent_transactions": recent_transactions[['date', 'description', 'category', 'amount']].astype(str).to_dict(orient='records')
    }
    
    with open('dashboard_data.json', 'w') as f:
        json.dump(output_data, f, indent=4)
        
    print("Analysis complete. dashboard_data.json created.")

if __name__ == "__main__":
    process_data()
