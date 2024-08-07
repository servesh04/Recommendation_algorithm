import pandas as pd
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

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
    110: 'Wireless Keyboard',
    111: 'Fitness Tracker',
    112: 'Gaming Console',
    113: 'Webcam',
    114: 'Printer',
    115: 'Power Bank'
}

# Sample purchase data
data = {
    'customer_id': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
    'product_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    'purchase_date': ['2023-01-01', '2023-01-05', '2023-02-01', '2023-02-10', '2023-03-01', '2023-03-05', '2023-04-01', '2023-04-10', '2023-05-01', '2023-05-10']
}

df = pd.DataFrame(data)
df['purchase_date'] = pd.to_datetime(df['purchase_date'])

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

def get_recommendations(user_purchases):
    # Add user purchases to the dataframe
    user_id = max(df['customer_id']) + 1
    for product_id in user_purchases:
        df.loc[len(df)] = [user_id, product_id, pd.Timestamp.now()]

    # Encode customer_id and product_id
    customer_encoder = LabelEncoder()
    product_encoder = LabelEncoder()
    df['customer_encoded'] = customer_encoder.fit_transform(df['customer_id'])
    df['product_encoded'] = product_encoder.fit_transform(df['product_id'])

    # Create the user-item matrix
    user_item_matrix = csr_matrix((df['purchase_date'].notnull().astype(int), 
                                   (df['customer_encoded'], df['product_encoded'])))

    # Fit the KNN model
    knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=min(5, user_item_matrix.shape[0]))
    knn.fit(user_item_matrix)

    # Get recommendations
    user_encoded = customer_encoder.transform([user_id])[0]
    distances, indices = knn.kneighbors(user_item_matrix[user_encoded].reshape(1, -1))

    # Collect products recommended by KNN
    recommended_products_knn = []
    for i in indices.flatten():
        if i != user_encoded:  # Exclude the user's own purchases
            recommended_products_knn.extend(df[df['customer_encoded'] == i]['product_id'].values)
    recommended_products_knn = list(set(recommended_products_knn) - set(user_purchases))  # Remove user's purchases

    # Get top N most frequently bought products
    N = 5
    product_counts = df['product_id'].value_counts().reset_index()
    product_counts.columns = ['product_id', 'count']
    top_n_products = product_counts[~product_counts['product_id'].isin(user_purchases)].sort_values(by='count', ascending=False).head(N)

    # Combine KNN and top N recommendations
    combined_recommendations = top_n_products['product_id'].tolist()
    combined_recommendations.extend([pid for pid in recommended_products_knn if pid not in combined_recommendations][:5 - len(combined_recommendations)])

    # Map product IDs to product names
    recommended_product_names = [products[pid] for pid in combined_recommendations]

    return recommended_product_names

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