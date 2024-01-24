from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
import random
import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK datasets
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


# Initialize NLTK tools
stop_words = set(stopwords.words('english'))
porter = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Load your data frame here
df = pd.read_csv('DATA_SET1.csv')  # Replace with your actual data file
products = df

#-----------------  Function --------------
# Function to find the product with the Highest price 
def product_with_highest_price(df):
    highest_price = df['Price'].max()
    highest_price_products = df[df['Price'] == highest_price]
    return highest_price_products

# Function to find the product with the Lowest price 
def product_with_lowest_price(df):
    lowest_price = df['Price'].min()
    lowest_price_products = df[df['Price'] == lowest_price]
    return lowest_price_products

# Function to calculate the average price of products
def average_product_price(df):
    average_price = df['Price'].mean()
    return average_price

# Function to calculate the avg price of specific phone brand
def phones_avg_price_brand(df, brand):
    # Filter the dataframe for the specified brand
    brand_df = df[df['Brand'].str.lower() == brand.lower()]  # Assuming 'Brand' is the column name
    if not brand_df.empty:
        # Calculate the average price
        average_price = brand_df['Price'].mean()  # Assuming 'Price' is the column name
        return average_price

# Function to find the product with the Lowest Rating 
def product_with_lowest_rating(df):
    lowest_rating = df['Rating'].min()
    lowest_rating_products = df[df['Rating'] == lowest_rating]
    return lowest_rating_products.head(5)

# Function to find the product with the Highest Rating 
def product_with_highest_rating(df):
    highest_rating = df['Rating'].max()
    highest_rating_products = df[df['Rating'] == highest_rating]
    return highest_rating_products.head(5)

# Function to Filter the DataFrame to include only products with prices equal to or above the specified minimum price
def best_phones_above_price(df, min_price):
    df_filtered = df[df['Price'] >= min_price]
    num_items_filtered = len(df_filtered)
    sorted_phones = df_filtered.sort_values(by='Rating', ascending=False)
    top_5_phones = sorted_phones.head(5)
    average_price = df_filtered['Price'].mean()
    average_rating = df_filtered['Rating'].mean()
    total_questions = df_filtered['No.of Questions'].sum()
    return num_items_filtered, top_5_phones, average_price, average_rating, total_questions


# Function to Filter the DataFrame to include only products with prices equal to or below the specified minimum price
def best_phones_under_price(df, max_price):
    df_filtered = df[df['Price'] <= max_price]
    num_items_filtered = len(df_filtered)
    sorted_phones = df_filtered.sort_values(by='Rating', ascending=False)
    top_5_phones = sorted_phones.head(5)
    average_price = df_filtered['Price'].mean()
    average_rating = df_filtered['Rating'].mean()
    total_questions = df_filtered['No.of Questions'].sum()
    return num_items_filtered, top_5_phones, average_price, average_rating, total_questions

# Filter the DataFrame to include only products with prices within the specified range
def best_phones_between_price(df, min_price, max_price):
    df_filtered = df[(df['Price'] >= min_price) & (df['Price'] <= max_price)]
    num_items_filtered = len(df_filtered)
    sorted_phones = df_filtered.sort_values(by='Rating', ascending=False)
    top_5_phones = sorted_phones.head(5)
    average_price = df_filtered['Price'].mean()
    average_rating = df_filtered['Rating'].mean()
    total_questions = df_filtered['No.of Questions'].sum()
    return num_items_filtered, top_5_phones, average_price, average_rating, total_questions

# Filter the DataFrame to include only products with free shipping
def products_with_free_shipping(df):
    free_shipping_df = df[df['Free Shipping Status'] == True]
    return free_shipping_df

# Filter the DataFrame to include only products available in Daraz Mall
def products_in_daraz_mall(df):
    daraz_mall_df = df[df['Daraz Mall Status'] == True]
    return daraz_mall_df

# Find sellers with the highest rating
def sellers_with_best_rating(df):
    best_seller_rating = df['Seller Rating'].max()
    best_sellers = df[df['Seller Rating'] == best_seller_rating]
    return best_sellers
    
# Filter the DataFrame to include only sellers with a ship-on-time score of 90 or higher
def sellers_who_ship_on_time(df):
    on_time_shippers = df[df['Ship on Time Score'] >= 90]  # Assuming the score is out of 100
    return on_time_shippers

def filter_phone_specifications(df, specs, model_specs=[]):
    """
    Filter a DataFrame of phone products based on specified specifications.

    Parameters:
    - df (pd.DataFrame): DataFrame containing phone products.
    - specs (list): List of general specifications to filter by.
    - model_specs (list): List of model-specific specifications to filter by.

    Returns:
    - pd.DataFrame: Filtered DataFrame containing rows matching the specified specifications.
    """
    filtered_rows = []

    # Convert specifications and model_specs to lowercase for case-insensitive matching
    specs = [spec.lower() for spec in specs]
    model_specs = [model_spec.lower() for model_spec in model_specs]

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        title = row['Product Title'].lower()
        specifications = row['Specifications'].lower()

        # Check if any general specification matches the title or specifications
        if any(spec in title or spec in specifications for spec in specs):
            # Check if all model-specific specifications are present in the title or specifications
            if all(model_spec in title or model_spec in specifications for model_spec in model_specs):
                filtered_rows.append(row)

    # Create a new DataFrame with the filtered rows
    filtered_df = pd.DataFrame(filtered_rows, columns=df.columns)
    
    # Select the top 5 rows from the filtered DataFrame
    dff = filtered_df.head(5)
    
    return dff



# Filter phones based on whether the specified feature is present in their title
def find_phone_with_feature(df, feature):
    return df[df['Product Title'].str.contains(feature, case=False)]

# Find the product with the highest number of questions
def product_with_most_questions(df):
    most_questions = df['No.of Questions'].max()
    most_questions_product = df[df['No.of Questions'] == most_questions]
    return most_questions_product

# Find the brand of the best-selling product based on the highest price and rating
def brand_of_best_selling(df):
    highest_price = df['Price'].max()
    highest_price_products = df[df['Price'] == highest_price]
    highest_rated = highest_price_products['Rating'].max()
    best_selling_product = highest_price_products[highest_price_products['Rating'] == highest_rated]
    best_selling_brand = best_selling_product['Brand'].values[0]
    return best_selling_brand, (highest_price, highest_rated)

# Find the brand of the mobile with the highest price
def brand_of_highest_price_mobile(df):
    highest_price = df['Price'].max()
    highest_price_brand = df[df['Price'] == highest_price]['Brand'].values[0]
    return highest_price_brand, highest_price

# Find the brand of the mobile with the lowest price
def brand_of_lowest_price_mobile(df):
    lowest_price = df['Price'].min()
    lowest_price_brand = df[df['Price'] == lowest_price]['Brand'].values[0]
    return lowest_price_brand, lowest_price

# Filter the products based on the given minimum rating and maximum price
def filter_products_rating_price(df, min_rating, max_price):
    filtered_df = df[(df['Rating'] >= min_rating) & (df['Price'] <= max_price)]
    return filtered_df


def filter_products_range_price_brand(df, min_price, max_price, brands):
    # Convert single brand string to a list
    if isinstance(brands, str):
        brands_lower = [brands.lower()]
    else:
        # Convert list of brands to lowercase
        brands_lower = [brand.lower() for brand in brands]

    # Filter the DataFrame based on the specified criteria
    filtered_df = df[(df['Price'] >= min_price) & (df['Price'] <= max_price) & (df['Brand'].str.lower().isin(brands_lower))]

    # Create a new DataFrame for the filtered results
    df_filtered = filtered_df

    # Calculate additional statistics
    num_items_filtered = len(df_filtered)
    sorted_phones = df_filtered.sort_values(by='Rating', ascending=False)
    top_5_phones = sorted_phones.head(5)
    average_price = df_filtered['Price'].mean()
    average_rating = df_filtered['Rating'].mean()
    total_questions = df_filtered['No.of Questions'].sum()

    return num_items_filtered, top_5_phones, average_price, average_rating, total_questions


def extract_prices(tokens):
    prices = []
    for token in tokens:
        if 'k' in token.lower():
            try:
                price = int(float(token.lower().replace('k', '')) * 1000)
                prices.append(price)
            except ValueError:
                continue
        elif token.isdigit():
            prices.append(int(token))
    return prices


#-------------- Functions for bot responses ------------

bot_responses = {
    "hi": ["Hi there! How can I assist you today?","Hello! Ready to help. What do you need?"],
    "Hey":["Hi there!", "Hello!"],
    "hello": ["Hi there!", "Hello!"],
    "how are you": ["I'm good, thanks for asking.", "I'm doing well, thank you!"],
    "what's up": ["Not much, just here to help.", "I'm here to assist you!"],
    "goodbye": ["Goodbye! Feel free to return if you have more queries.", "See you later! If you need anything else, I'm here."],
    "thanks": ["You're welcome! If you have more questions, feel free to ask.","My pleasure! Anything else I can help you with?","myPleasure!", ":}", ":} :}"],
    "what can you do": ["I can help you with a wide range of tasks.","I'm here to assist you with your queries."],
    
}

# Function to generate a random bot response
def get_bot_response(user_input):
    if user_input.lower() in bot_responses:
        return random.choice(bot_responses[user_input.lower()])
    else:
        return "Sorry, I don't understand that."
    

#-------------- Functions for bot responses ------------


# Updated analyze_input function
def analyze_input(user_input, df):
    tokens = word_tokenize(user_input.lower())
    filtered_tokens = [word for word in tokens if word not in stop_words]
    stemmed_tokens = [porter.stem(word) for word in filtered_tokens]
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in stemmed_tokens]
    pos_tags = nltk.pos_tag(lemmatized_tokens)
    matching_columns = {token: column for token in lemmatized_tokens for column in df.columns if token in column.lower()}
    
 
 # Logic for mobile phone-related queries
    if 'mobile' in matching_columns or 'phone' in matching_columns:
        # Logic for 'price' related queries
        if 'price' in matching_columns or 'price' in user_input:
            if any(keyword in lemmatized_tokens for keyword in ['max', 'highest']):
                return product_with_highest_price(df)
            elif any(keyword in lemmatized_tokens for keyword in ['min', 'lowest', 'minimum']):
                return product_with_lowest_price(df)
            elif any(keyword in lemmatized_tokens for keyword in ['average', 'averag']):
                return average_product_price(df)

    # Logic for 'rating' related queries
    if 'rating' in matching_columns or 'rating' in user_input:
        if 'max' in lemmatized_tokens or 'highest' in lemmatized_tokens or 'max' in user_input or 'highest' in user_input:
            return product_with_highest_rating(df)
        elif 'min' in lemmatized_tokens or 'lowest' in lemmatized_tokens or 'minimum' in user_input or 'lowest' in user_input:
            return product_with_lowest_rating(df)

    # Logic for 'shipping' related queries
    if 'ship' in lemmatized_tokens or 'shipping' in matching_columns or 'ship' in user_input or 'shipping' in user_input:
        if 'free' in lemmatized_tokens or 'free' in user_input:
            return products_with_free_shipping(df)
        elif 'time' in lemmatized_tokens or 'time' in user_input:
            return sellers_who_ship_on_time(df)

    # Logic for 'Daraz Mall' related queries
    if 'daraz' in lemmatized_tokens and 'mall' in lemmatized_tokens or 'daraz' in user_input and 'mall' in user_input:
        return products_in_daraz_mall(df)

    # Logic for 'seller' related queries
    if 'seller' in matching_columns or 'seller' in user_input:
        if 'best' in lemmatized_tokens or 'top' in lemmatized_tokens or 'best' in user_input or 'top' in user_input:
            return sellers_with_best_rating(df)


    # Logic for 'feature' or 'specification' related queries
    if 'feature' in lemmatized_tokens or 'specification' in lemmatized_tokens or 'specs' in lemmatized_tokens or 'RAM' in lemmatized_tokens or 'feature' in user_input or 'RAM' in user_input or 'specification' in user_input or 'specs' in user_input:
        if 'with' in tokens:
            try:
                # Extract features after 'with'
                feature = " ".join(tokens[tokens.index('with') + 1:])
                
                # Check if the query specifies a numeric value (e.g., 64 GB RAM and 48 MP camera)
                numeric_values = [int(word) for word in lemmatized_tokens if word.isdigit()]
                
                if len(numeric_values) >= 2:
                    ram_value, camera_value = sorted(numeric_values[:2])
                    
                    # Filter products based on RAM and camera specifications
                    filtered_products = filter_phone_specifications(products, [f"{ram_value} GB RAM", f"{camera_value} MP camera"])
                    
                    if not filtered_products.empty:
                        return filtered_products.head(5)
                    else:
                        return "No phones found with the specified specifications."

                else:
                    return "Please provide numeric values for RAM and camera specifications."

            except IndexError:
                return "Please provide a specific feature after 'with'."
        else:
            return "Please specify the feature you are looking for using 'with.'"


    # Logic for filtering products by price and rating
    if 'price' in lemmatized_tokens and 'above' in lemmatized_tokens and 'rating' in lemmatized_tokens or 'price' in user_input and 'above' in user_input and 'rating' in user_input:
        try:
            prices = extract_prices(tokens)
            if len(prices) >= 2:
                min_rating, max_price = sorted(prices[:2])
                return filter_products_rating_price(df, min_rating, max_price)
        except IndexError:
            return "Please Re-enter."

    # Logic for filtering products by price range and brand
    if 'price' in lemmatized_tokens and 'brand' in lemmatized_tokens and 'range' in lemmatized_tokens or 'price' in user_input and 'range' in user_input and 'brand' in user_input:
        try:
            prices = extract_prices(lemmatized_tokens)
            if len(prices) >= 2:
                min_price, max_price = sorted(prices[:2])
                b=['Xiaomi','Tecno', 'Redmi', 'Honor', 'Samsung','Infinix', 'itel', 'Infinix__','Shoptech', 'OPPO','LG ReEn', 'Sparx', 'Motorola', 'VGOTEL', 'Realme','Vivo', 'Nokia', 'ZTE', 'SONY']
                matching_brands = []
                # Check for matches between words in 'b' and the input string
                for brand in b:
                    brand_lower = brand.lower()
                    if brand_lower in tokens:
                        matching_brands.append(brand)
                return filter_products_range_price_brand(df, min_price, max_price, matching_brands[0])
        except IndexError:
            return "Please Re-enter."

    # Logic for finding best phones between a certain price range
    if 'best' in lemmatized_tokens and 'phone' in lemmatized_tokens or 'between' in lemmatized_tokens or 'range' in lemmatized_tokens or 'best' in user_input and 'phone' in user_input or 'between' in user_input or 'range' in user_input:
        try:
            prices = extract_prices(lemmatized_tokens)
            if len(prices) >= 2:
                min_price, max_price = sorted(prices[:2])
                return best_phones_between_price(df, min_price, max_price)
            else:
                return "Please provide both a minimum and a maximum price limit."
        except ValueError:
            return "Please provide valid price limits."

    # Logic for finding average product price by brand
    if 'average' in lemmatized_tokens and 'price' in lemmatized_tokens and 'with' in lemmatized_tokens and 'brand' in lemmatized_tokens or 'average' in user_input and 'price' in user_input and 'with' in user_input and 'brand' in user_input:
        try:
            b=['Xiaomi','Tecno', 'Redmi', 'Honor', 'Samsung','Infinix', 'itel', 'Infinix__','Shoptech', 'OPPO','LG ReEn', 'Sparx', 'Motorola', 'VGOTEL', 'Realme','Vivo', 'Nokia', 'ZTE', 'SONY']
            matching_brands = []
            # Check for matches between words in 'b' and the input string
            for brand in b:
                brand_lower = brand.lower()
                if brand_lower in tokens:
                    matching_brands.append(brand)
            return phones_avg_price_brand(df, matching_brands[0])  # Assuming you only need the first number found
        except ValueError:
            return "ERROR: Brand name?"

    # Logic for finding best phones under a certain price
    if 'phone' in lemmatized_tokens and 'under' in lemmatized_tokens or 'phone' in user_input and 'under' in user_input:
        try:
            max_price = extract_prices(tokens)
            if max_price:
                return best_phones_under_price(df, max_price[0])  # Assuming you only need the first number found
            else:
                return "Please provide a valid price limit."
        except ValueError:
            return "Please provide a valid price limit."

    # Logic for finding best phones above a certain price
    if 'phone' in lemmatized_tokens and 'above' in lemmatized_tokens or 'greater' in lemmatized_tokens or 'phone' in user_input and 'above' in user_input or 'above' in user_input:
        try:
            max_price = extract_prices(tokens)
            if max_price:
                return best_phones_above_price(df, max_price[0])  # Assuming you only need the first number found
            else:
                return "Please provide a valid price limit."
        except ValueError:
            return "Please provide a valid price limit."

    # Logic for queries about the product with most questions
    if 'most' in lemmatized_tokens and 'question' in lemmatized_tokens or 'most' in user_input and 'question' in user_input:
        return product_with_most_questions(df)

    # Logic for queries about the best selling brand
    if 'best' in lemmatized_tokens and 'selling' in lemmatized_tokens and 'brand' in lemmatized_tokens or 'best' in user_input and 'selling' in user_input and 'brand' in user_input:
        return brand_of_best_selling(df)

    # Logic for queries about the brand of the highest price mobile
    if 'highest' in lemmatized_tokens and 'price' in lemmatized_tokens and 'brand' in lemmatized_tokens or 'highest' in user_input and 'price' in user_input and 'brand' in user_input:
        return brand_of_highest_price_mobile(df)

    # Logic for queries about the brand of the lowest price mobile
    if 'lowest' in lemmatized_tokens and 'price' in lemmatized_tokens and 'brand' in lemmatized_tokens or 'lowest' in user_input and 'price' in user_input and 'brand' in user_input:
        return brand_of_lowest_price_mobile(df)
    else:
        return get_bot_response(user_input)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/processSeller', methods=['POST'])
def get_processSeller():
    user_input = request.json['message']
    response = analyze_input(user_input, products)
    result_data = {}  # Create a new dictionary for each request

    if response is not None:
        if isinstance(response, tuple):
            if isinstance(response[1], pd.DataFrame):
                # Handling response from functions like best_phones_under_price
                num_items_filtered, top_5_phones, avg_price, avg_rating, total_questions = response

                result_data["message"] = f"There are {num_items_filtered} phones matching your criteria."
                result_data["product_list"] = top_5_phones.to_dict(orient='records')
                result_data["statistics"] = {
                    "average_price": round(avg_price, 2),
                    "average_rating": round(avg_rating, 2),
                    "total_questions": str(round(total_questions, 2))
                }

            else:
                result_data["message"] = f"{response[0]} with a value of {response[1]}"

        else:
            if isinstance(response, pd.DataFrame):
                result_data["product_list"] = response.to_dict(orient='records')
            else:
                result_data["message"] = f"{response}"

    return jsonify({'response': result_data})

# ...