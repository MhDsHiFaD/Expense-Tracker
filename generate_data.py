import csv
import random
from datetime import datetime, timedelta

def generate_transaction_data(n=500):
    random.seed(42)
    
    # Categories and potential descriptions
    # Note: I'm keeping 'Subsciptions' misspelled as 'Subsciptions' to give the user something to clean!
    categories = {
        'Food & Drink': ['Starbucks', 'McDonaldsn', 'Whole Foods', 'Taco Bell', 'Local Cafe', 'Pizza Hut', 'UberEats'],
        'Transport': ['Uber', 'Lyft', 'Gas Station', 'Metro Ticket', 'Parking Gar'],
        'Subsciptions': ['Netflix', 'Spotify', 'Amazon Prime', 'Gym Membership', 'Cloud Storage'],
        'Shopping': ['Amazon', 'Walmart', 'Target', 'Apparel Store', 'Electronic Mart', 'Home Depot'],
        'Utilities': ['Electric Bill', 'Water Bill', 'Internet Provider', 'Phone Bill'],
        'Rent': ['Monthly Rent']
    }
    
    start_date = datetime(2025, 1, 1)
    data = []
    
    for _ in range(n):
        cat_key = random.choice(list(categories.keys()))
        desc = random.choice(categories[cat_key])
        
        # Add some "messiness" (Transaction IDs, Locations)
        if random.random() > 0.5:
            desc = f"{desc} #{random.randint(1000, 9999)} NY"
        
        date = start_date + timedelta(days=random.randint(0, 365))
        
        if cat_key == 'Rent':
            amount = 25000.00
            date = date.replace(day=1)
        elif cat_key == 'Utilities':
            amount = random.uniform(50, 150)
        elif cat_key == 'Subsciptions':
            amount = random.uniform(10, 30)
        else:
            amount = random.uniform(5, 200)
            
        # Introduce some nulls for amount
        if random.random() < 0.02: # 2% chance of missing value
            amount = ""
        else:
            amount = round(amount, 2)

        data.append([date.strftime('%Y-%m-%d'), desc, amount, 'INR'])

    # Sort data by date
    data.sort(key=lambda x: x[0])
    
    return data

if __name__ == "__main__":
    headers = ['date', 'description', 'amount', 'currency']
    rows = generate_transaction_data(500)
    
    with open('transactions.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
        
    print("Successfully generated transactions.csv using standard Python libraries.")
