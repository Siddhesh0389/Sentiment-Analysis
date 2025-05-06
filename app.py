from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load the processed data
data = pd.read_csv("processed_reviews.csv")  # Update with your CSV file path

# Load the vectorizer and model
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
model = pickle.load(open("sentiment_model.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html', reviews=None, selected_city=None, message=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the city from form input
    city = request.form['city']
    
    # Filter data by city
    filtered_data = data[data['Location'].str.contains(city, case=False, na=False)].copy()

    # Check if the city exists in the dataset
    if filtered_data.empty:
        return render_template(
            'index.html', 
            reviews=None, 
            selected_city=city, 
            message=f"Data for {city} is not available."
        )

    # Handle missing values in 'Cleaned Review'
    filtered_data['Cleaned Review'] = filtered_data['Cleaned Review'].fillna("No review available")

    # Vectorize the cleaned review text
    transformed_reviews = vectorizer.transform(filtered_data['Cleaned Review'])

    # Predict sentiment
    filtered_data['Sentiment Prediction'] = model.predict(transformed_reviews)

    # Map sentiment predictions to labels
    filtered_data['Sentiment Polarity'] = filtered_data['Sentiment Prediction'].map({
        1: 'Positive', 
        0: 'Neutral', 
        -1: 'Negative'
    })

    # Convert the filtered data to a list of dictionaries for the template
    reviews = filtered_data[['Cleaned Review', 'Sentiment Polarity', 'Date', 'Location', 'Extracted Emojis', 'Rating', 'Reviewer ID']].to_dict(orient='records')
    return render_template(
        'index.html', 
        reviews=reviews, 
        selected_city=city, 
        message=None
    )

if __name__ == '__main__':
    app.run(debug=True)
