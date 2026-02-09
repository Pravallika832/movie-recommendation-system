🎬 Movie Recommender System

A Machine Learning web application that recommends similar movies based on content similarity and displays real movie posters using the TMDB API.

📌 Project Overview

This project is a content-based movie recommendation system.
When a user selects a movie, the system suggests 5 similar movies along with their posters.

The recommendations are generated using Natural Language Processing (NLP) and cosine similarity on movie metadata such as genres, keywords, cast, and overview.

🧠 How It Works

The movie dataset is cleaned and important features are combined into a single column called tags.

Text data is converted into vectors using CountVectorizer.

Cosine similarity is calculated between all movies.

When a user selects a movie, the top 5 most similar movies are returned.

Posters are fetched dynamically from the TMDB API and shown in the Streamlit web app.

🛠️ Technologies Used

Python

Pandas

NumPy

Scikit-learn

NLP (CountVectorizer)

Streamlit

TMDB API

Pickle

📂 Project Structure
movie-recommender/
│
├── app.py
├── movies_dict.pkl
├── similarity.pkl
├── requirements.txt
└── README.md
🚀 How to Run Locally

Clone the repository

git clone https://github.com/Pravallika832/movie-recommendation-system

Go into the project folder

cd movie-recommender-system

Install required libraries

pip install -r requirements.txt

Run the application

streamlit run app.py

Open in browser

http://localhost:8501
🎯 Features

Recommend similar movies

Displays real movie posters

Interactive UI using Streamlit

Fast recommendations using precomputed similarity matrix

📊 Dataset

TMDB 5000 Movies Dataset

The dataset includes:

title

genres

keywords

cast

crew

overview

🙋‍♀️ Author

Pravallika Chitturi
