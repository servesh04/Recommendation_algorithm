1. Data Setup:
   - We have a dictionary of `products` mapping product IDs to names.
   - There's sample `data` representing previous customer purchases.
   - This data is converted into a pandas DataFrame `df`.

2. User Input Function (`get_user_purchases()`):
   - This function displays all available products to the user.
   - It then prompts the user to enter product IDs they've purchased.
   - It continues to accept input until the user types 'done'.
   - It returns a list of product IDs the user has purchased.

3. Recommendation Function (`get_recommendations(user_purchases)`):
   - This is the core of the recommender system. Here's what it does:

   a. Data Preparation:
      - Adds the user's purchases to the existing DataFrame.
      - Uses LabelEncoder to convert customer and product IDs into numerical format.
      - Creates a user-item matrix using sparse matrix representation.

   b. K-Nearest Neighbors (KNN):
      - Fits a KNN model on the user-item matrix.
      - Finds the nearest neighbors (similar users) to the current user.

   c. Collaborative Filtering:
      - Collects products purchased by similar users (KNN recommendations).
      - Excludes products the user has already purchased.

   d. Popularity-based Recommendations:
      - Identifies the top N most frequently purchased products overall.
      - Excludes products the user has already purchased.

   e. Combining Recommendations:
      - Merges the KNN-based and popularity-based recommendations.
      - Ensures a diverse set of recommendations (up to 5 products).

   f. Product Mapping:
      - Converts product IDs back to product names for display.

4. Main Program Flow:
   - Welcomes the user and calls `get_user_purchases()` to get their purchase history.
   - If the user has made purchases, it calls `get_recommendations()` to get personalized recommendations.
   - Displays the recommended products to the user.

The key idea here is to combine two recommendation strategies:

1. Collaborative Filtering (via KNN): This recommends products based on what similar users have purchased.
2. Popularity-based: This recommends products that are generally popular among all users.

By combining these approaches, the system aims to provide recommendations that are both personalized and likely to be of general interest. The system also ensures it doesn't recommend products the user has already purchased, increasing the likelihood of suggesting new, relevant items.

This approach allows for a more interactive and personalized recommendation experience, as it bases its suggestions on the specific products each user inputs rather than predefined user profiles.

Algorithm :

Data Preparation
1.1. Load the product catalog and historical purchase data
1.2. Convert historical purchase data into a pandas DataFrame
1.3. Add the current user's purchases to the DataFrame
Data Encoding
2.1. Use LabelEncoder to convert customer IDs to numerical format
2.2. Use LabelEncoder to convert product IDs to numerical format
Create User-Item Matrix
3.1. Construct a sparse matrix where rows represent users and columns represent products
3.2. Set matrix values to 1 where a user has purchased a product, 0 otherwise
K-Nearest Neighbors (KNN) Model
4.1. Initialize a KNN model with cosine similarity as the distance metric
4.2. Fit the KNN model on the user-item matrix
Find Similar Users
5.1. Identify the K nearest neighbors (similar users) to the current user
5.2. K is the minimum of 5 and the total number of users
Collaborative Filtering Recommendations
6.1. Collect all products purchased by the similar users
6.2. Remove products already purchased by the current user
6.3. Remove duplicate products
Popularity-based Recommendations
7.1. Count the frequency of each product in the entire purchase history
7.2. Sort products by purchase frequency in descending order
7.3. Select the top N most popular products (e.g., N = 5)
7.4. Remove products already purchased by the current user
Combine Recommendations
8.1. Start with the popularity-based recommendations
8.2. Add collaborative filtering recommendations not already included
8.3. Limit the total number of recommendations to 5
Map Recommendations to Product Names
9.1. Convert the recommended product IDs to their corresponding names using the product catalog
Return Recommendations
10.1. Return the list of recommended product names
