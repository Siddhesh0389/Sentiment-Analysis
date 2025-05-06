import praw
import pandas as pd
from textblob import TextBlob
import random
from datetime import datetime

# Step 1: Authenticate with Reddit API
reddit = praw.Reddit(
    client_id='XLIGqvgfRPLi_Gt9hRFD8w',          # Replace with your Client ID
    client_secret='xPybd1wMpJen1v4xqA4uOsyYvhbG-w', # Replace with your Client Secret
    user_agent='ZomatoReviewApp/1.0',   
    username='Siddhu_0389'   # Your Reddit username   
)

# Step 2: Define parameters
subreddit_name = 'India'
query = 'Zomato'
post_limit = 1000  # Number of posts to fetch 
max_entries = 10000  # Limit to 10000 final rows

# Categories for mocking purposes
categories = ["Delivery Speed", "Food Quality", "Customer Service", "Pricing", "Overall Experience"]
locations = ["Mumbai, India", "Delhi, India", "Bangalore, India", "Hyderabad, India", "Chennai, India", " Pune, India"]

# Step 3: Collect posts and comments
reviews = []
subreddit = reddit.subreddit(subreddit_name)

for submission in subreddit.search(query, limit=post_limit):
    submission.comments.replace_more(limit=0)  # Expand all comments
    for comment in submission.comments.list():
        # Only take short reviews (under 200 characters) for concise data
        if len(comment.body) > 200:
            continue
        
        review_text = comment.body
        reviewer_id = comment.author.name if comment.author else 'Anonymous'
        date = pd.to_datetime(comment.created_utc, unit='s')  # Convert timestamp to date

        # Sentiment Analysis
        analysis = TextBlob(review_text)
        polarity = "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

        # Generate Mock Rating based on Sentiment
        rating = 5 if polarity == "Positive" else 2 if polarity == "Negative" else 3

        # Randomly assign a location and category
        location = random.choice(locations)
        category = random.choice(categories)

        # Append to the list
        reviews.append({
            "Review Text": review_text,
            "Rating": rating,
            "Date": date.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as required
            "Location": location,
            "Reviewer ID": reviewer_id,
            "Sentiment Polarity": polarity,
            "Category": category
        })

        # Break if 500 entries are collected
        if len(reviews) >= max_entries:
            break
    if len(reviews) >= max_entries:
        break

# Step 4: Create a DataFrame and Save to CSV
df = pd.DataFrame(reviews)
df.to_csv('zomato_reviews.csv', index=False)
print("Data saved to zomato_reviews.csv")
