import streamlit as st
import pickle
import pandas as pd
import requests


# ---------- TMDB POSTER FUNCTION ----------
def fetch_poster(movie_id):

    api_key = "b7760be1c771c05e2a66229c87313855"

    # API to get movie details
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    response = requests.get(url)

    # if request fails
    if response.status_code != 200:
        return "https://via.placeholder.com/300x450?text=No+Image"

    data = response.json()

    poster_path = data.get("poster_path")

    # some movies don't have posters
    if poster_path is None:
        return "https://via.placeholder.com/300x450?text=No+Poster"

    # convert to full image URL
    full_url = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_url


# ---------- RECOMMENDATION FUNCTION ----------
def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id   #IMPORTANT LINE
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ---------- LOAD DATA ----------
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))


# ---------- STREAMLIT UI ----------
st.title("🎬 Movie Recommender System")
st.write("Get similar movie recommendations with posters!")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)


# ---------- BUTTON ----------
if st.button("Recommend"):

    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
