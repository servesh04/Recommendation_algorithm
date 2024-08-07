import pandas as pd
from itertools import combinations

# Sample product data
products = {
    101: 'Laptop',
    102: 'Smartphone',
    103: 'Headphones',
    104: 'Smartwatch',
    105: 'Tablet',
    106: 'E-reader',
    107: 'Wireless Mouse',
    108: 'Bluetooth Speaker',
    109: 'External Hard Drive',
    110: 'Wireless Keyboard'
}

# Sample purchase data (1 indicates purchase, 0 indicates no purchase)
data = {
    'customer_id': [1, 2, 3, 4, 5],
    101: [1, 1, 0, 1, 0],
    102: [1, 0, 1, 0, 1],
    103: [1, 1, 1, 0, 0],
    104: [0, 1, 0, 1, 1],
    105: [0, 0, 1, 1, 0],
    106: [1, 0, 0, 0, 1],
    107: [0, 1, 1, 0, 0],
    108: [1, 0, 0, 1, 1],
    109: [0, 1, 1, 0, 1],
    110: [1, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

def get_user_purchases():
    user_purchases = []
    print("Available products:")
    for pid, pname in products.items():
        print(f"{pid}: {pname}")
    
    while True:
        product_id = input("Enter a product ID you've purchased (or 'done' to finish): ")
        if product_id.lower() == 'done':
            break
        try:
            product_id = int(product_id)
            if product_id in products:
                user_purchases.append(product_id)
            else:
                print("Invalid product ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'done'.")
    
    return user_purchases

def candidate_elimination(user_purchases, all_products):
    S = set(user_purchases)
    G = set(combinations(all_products, len(user_purchases)))
    
    for _, row in df.iterrows():
        customer_purchases = set([prod for prod in all_products if row[prod] == 1])
        
        if customer_purchases.issuperset(S):  # Positive example
            G = {g for g in G if set(g).issubset(customer_purchases)}
        else:  # Negative example
            S = S.intersection(customer_purchases)
            G = {g for g in G if not set(g).issubset(customer_purchases)}
    
    return S, G

def get_recommendations(user_purchases):
    all_products = list(products.keys())
    S, G = candidate_elimination(user_purchases, all_products)
    
    recommendations = set()
    for g in G:
        recommendations.update(set(g) - S)
    
    recommendations = recommendations - set(user_purchases)
    
    if not recommendations:
        recommendations = set(all_products) - set(user_purchases)
    
    recommended_products = [products[pid] for pid in list(recommendations)[:5]]
    
    return recommended_products

# Main program
print("Welcome to the Product Recommender!")
user_purchases = get_user_purchases()

if user_purchases:
    print("\nBased on your purchase history, we recommend the following products:")
    recommendations = get_recommendations(user_purchases)
    for i, product in enumerate(recommendations, 1):
        print(f"{i}. {product}")
else:
    print("No purchases entered. Unable to provide personalized recommendations.")

print("\nThank you for using the Product Recommender!")
