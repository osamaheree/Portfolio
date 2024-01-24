from flask import Flask, render_template, request, jsonify
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Initialize Flask app
app = Flask(__name__)

# Load your DataFrame here
# Example: df = pd.read_csv("your_data_file.csv")
df = pd.read_csv('SET_DATA.csv')  # Replace with your actual data file
products = df

# Initialize NLTK tools (Ensure you have downloaded the necessary NLTK datasets)
stop_words = set(stopwords.words('english'))
porter = PorterStemmer()
lemmatizer = WordNetLemmatizer()
# Function 
# Function to find the product with the highest price
def product_with_highest_price(df):
    highest_price = df['Price'].max()
    highest_price_product = df[df['Price'] == highest_price]['Product Title'].values[0]
    return highest_price_product,highest_price

# Function to find the product with the lowest price
def product_with_lowest_price(df):
    lowest_price = df['Price'].min()
    lowest_price_product = df[df['Price'] == lowest_price]['Product Title'].values[0]
    return lowest_price_product,lowest_price

# Function to calculate the average price of products
def average_product_price(df):
    average_price = df['Price'].mean()
    return average_price

# Function to find the product with the lowest rating
def product_with_lowest_rating(df):
    lowest_Rating = df['Rating'].min()
    lowest_Rating_product = df[df['Rating'] == lowest_Rating]['Product Title'].values[0]
    return lowest_Rating_product,lowest_Rating

# Function to find the product with the highest rating
def product_with_highest_rating(df):
    highest_Rating = df['Rating'].max()
    highest_Rating_product = df[df['Rating'] == highest_Rating]['Product Title'].values[0]
    return highest_Rating_product,highest_Rating



def best_phones_above_price(df, min_price):
    high_priced_phones = df[df['Price'] >= min_price]
    highest_rated_phones = high_priced_phones[high_priced_phones['Rating'] == high_priced_phones['Rating'].max()]
    recommended_phones = highest_rated_phones[['Product Title', 'Price']].copy()
    return recommended_phones

def best_phones_under_price(df, max_price):
    affordable_phones = df[df['Price'] <= max_price]
    highest_rated_phones = affordable_phones[affordable_phones['Rating'] == affordable_phones['Rating'].max()]
    recommended_phones = highest_rated_phones[['Product Title', 'Price']].copy()
    return recommended_phones
 

def products_with_free_shipping(df):
    free_shipping_df = df[df['Free Shipping Status'] == True]
    free_shipping_products = free_shipping_df['Product Title'].tolist()
    return free_shipping_products

def products_in_daraz_mall(df):
    daraz_mall_df = df[df['Daraz Mall Status'] == True]
    daraz_mall_products = daraz_mall_df['Product Title'].tolist()
    return daraz_mall_products

def sellers_with_best_rating(df):
    best_seller_rating = df['Seller Rating'].max()
    best_sellers = df[df['Seller Rating'] == best_seller_rating]['Product Title'].tolist()
    return best_sellers

def sellers_who_ship_on_time(df):
    on_time_shippers = df[df['Ship on Time Score'] >= 90]  # Assuming the score is out of 100
    on_time_shipping_products = on_time_shippers['Product Title'].tolist()
    return on_time_shipping_products

def get_product_specifications(df, product_title):
    product_specs = df[df['Product Title'].str.contains(product_title, case=False)]
    if not product_specs.empty:
        return product_specs.iloc[0]['Specifications']
    else:
        return "Product not found."

def find_phone_with_feature(df, feature):
    phones_with_feature = df[df['Specifications'].str.contains(feature, case=False)]
    products = phones_with_feature['Product Title'].tolist()
    return products
# +++++++++++++++++++++++++++++

def product_with_most_questions(df):
    most_questions = df['No.of Questions'].max()
    most_questions_product = df[df['No.of Questions'] == most_questions]['Product Title'].values[0]
    return most_questions_product, most_questions

def brand_of_best_selling(df):
    # Filter the products with the highest price first
    highest_price = df['Price'].max()
    highest_price_products = df[df['Price'] == highest_price]
    highest_rated = highest_price_products['Rating'].max()
    best_selling_product = highest_price_products[highest_price_products['Rating'] == highest_rated]
    best_selling_brand = best_selling_product['Brand'].values[0]
    return best_selling_brand, (highest_price, highest_rated)

def brand_of_highest_price_mobile(df):
    highest_price = df['Price'].max()
    highest_price_brand = df[df['Price'] == highest_price]['Brand'].values[0]
    return highest_price_brand, highest_price

def brand_of_lowest_price_mobile(df):
    lowest_price = df['Price'].min()
    lowest_price_brand = df[df['Price'] == lowest_price]['Brand'].values[0]
    return lowest_price_brand, lowest_price

##
# Sample data in the form of a DataFrame with product information
# Replace this with the actual DataFrame you are using

# Define your functions here (e.g., product_with_highest_price, product_with_lowest_price, etc.)

bot_responses = {
    "hi": ["Hi there!", "Hello!"],
    "hello": ["Hi there!", "Hello!"],
    "how are you": ["I'm good, thanks for asking.", "I'm doing well, thank you!"],
    "what's up": ["Not much, just here to help.", "I'm here to assist you!"],
    "goodbye": ["Goodbye!", "See you later!", "Bye!"],
    "thanks": ["myPleasure!", ":}", ":} :}"],
}

# Function to generate a random bot response
def get_bot_response(user_input):
    if user_input.lower() in bot_responses:
        return random.choice(bot_responses[user_input.lower()])
    else:
        return "Sorry, I don't understand that."

# Updated analyze_input function
def analyze_input(user_input, df):
    tokens = word_tokenize(user_input.lower())
    filtered_tokens = [word for word in tokens if word not in stop_words]
    stemmed_tokens = [porter.stem(word) for word in filtered_tokens]
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in stemmed_tokens]
    pos_tags = nltk.pos_tag(lemmatized_tokens)
    matching_columns = {token: column for token in lemmatized_tokens for column in df.columns if token in column.lower()}


#     # Example for 'price' related queries
 # Logic for 'price' related queries
    if 'price' in matching_columns or 'price' in user_input:
        if 'max' in lemmatized_tokens or 'highest' in lemmatized_tokens or 'max' in user_input or 'highest' in user_input:
            return product_with_highest_price(df)
        elif 'min' in lemmatized_tokens or 'lowest' in lemmatized_tokens or 'minimum' in user_input or 'lowest' in user_input:
            return product_with_lowest_price(df)
        elif 'averag' in lemmatized_tokens or 'average' in user_input:
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

    # Logic for queries related to specific features or specifications
    if 'feature' in lemmatized_tokens or 'specification' in matching_columns or 'feature' in user_input or 'specification' in user_input:
        feature = " ".join(tokens[tokens.index('with') + 1:]) if 'with' in tokens else ""
        return find_phone_with_feature(df, feature)

    # Logic for finding best phones under a certain price
  # if 'best' in lemmatized_tokens and 'phone' in lemmatized_tokens or 'under' in lemmatized_tokens or 'best' in user_input and 'phone' in user_input or 'under' in user_input:
    if 'best' in lemmatized_tokens and 'phone' in lemmatized_tokens or 'under' in lemmatized_tokens or 'best' in user_input and 'phone' in user_input or 'under' in user_input:
        try:
            max_price = [int(t) for t in tokens if t.isdigit()]
            if max_price:
                return best_phones_under_price(df, max_price[0])  # Assuming you only need the first number found
            else:
                return "Please provide a valid price limit."
        except ValueError:
            return "Please provide a valid price limit."

 ##0000000000000000000000
    if 'phone' in lemmatized_tokens and 'above' in lemmatized_tokens or 'greater' in lemmatized_tokens or 'phone' in user_input and 'above' in user_input or 'above' in user_input:
          try:
              max_price = [int(t) for t in tokens if t.isdigit()]
              if max_price:
                  return best_phones_above_price(df, max_price[0])  # Assuming you only need the first number found
              else:
                  return "Please provide a valid price limit."
          except ValueError:
              return "Please provide a valid price limit."


   # Logic for queries about the product with most questions++++++++
    if 'most' in lemmatized_tokens and 'question' in lemmatized_tokens or 'most' in user_input and 'question' in user_input:
        return product_with_most_questions(df)

    # Logic for queries about the best selling brand
    if 'best' in lemmatized_tokens and 'selling' in lemmatized_tokens and 'brand' in lemmatized_tokens or 'best' in user_input and 'selling' in user_input and 'brand' in user_input:
        return brand_of_best_selling(df)

    # Logic for queries about the brand of the highest price mobile
    if 'highest' in lemmatized_tokens and 'price' in lemmatized_tokens and 'brand' in lemmatized_tokens or  'highest' in user_input and 'price' in user_input and 'brand' in user_input:
        return brand_of_highest_price_mobile(df)

    # Logic for queries about the brand of the lowest price mobile
    if 'lowest' in lemmatized_tokens and 'price' in lemmatized_tokens and 'brand' in lemmatized_tokens or  'lowest' in user_input and 'price' in user_input and 'brand' in user_input:
        return brand_of_lowest_price_mobile(df)
    else:
        return get_bot_response(user_input)


@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['userInput']
    response = analyze_input(user_input, df)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
