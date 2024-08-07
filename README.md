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

Display Available Products:

Loop through the products dictionary and print each product's ID and name.

Get User Purchases:

Initialize an empty list user_purchases to store products purchased by the user.
Prompt the user to input product IDs of purchased items until the user enters 'done'.
If a valid product ID is entered, append it to user_purchases.
If the input is invalid (not a number or not a valid product ID), prompt the user to try again.
Return the list of user_purchases.

Candidate Elimination Algorithm:

Initialize Sets:
Let S be the set of user's purchased product IDs.
Let G be the set of all possible combinations of products of size equal to the length of S.
Iterate Over Customer Purchase Data:
For each row in the DataFrame df:
Determine customer_purchases, the set of products purchased by the current customer.
Positive Example (Customer Purchases Superset of S):
Update G to contain only those combinations in G that are subsets of customer_purchases.
Negative Example (Customer Purchases Not Superset of S):
Update S by intersecting it with customer_purchases.
Remove any combinations in G that are subsets of customer_purchases.
Return Final Hypothesis:
Return the sets S and G.

Generate Recommendations:

Call candidate_elimination with user_purchases and the list of all product IDs.
Initialize an empty set recommendations.
Loop through each combination g in G:
Add the difference between g and S to the recommendations set.
Remove any products from recommendations that the user has already purchased.
If recommendations is empty, consider recommending all products not in user_purchases.
Convert the final product IDs in recommendations to product names and return the top 5 recommendations.
