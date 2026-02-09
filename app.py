import streamlit as st
import pickle
import pandas as pd
import requests
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- AUTO DATA CREATION ----------
def create_similarity():
    import ast

    movies = pd.read_csv('tmdb_5000_movies.csv')
    credits = pd.read_csv('tmdb_5000_credits.csv')

    movies = movies.merge(credits, on='title')

    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    movies.dropna(inplace=True)

    def convert(obj):
        L = []
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert)

    def fetch_director(obj):
        L = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
        return L

    movies['crew'] = movies['crew'].apply(fetch_director)
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    new_df = movies[['movie_id','title','tags']]
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()

    similarity = cosine_similarity(vectors)

    # Save
    pickle.dump(new_df, open('movies_dict.pkl', 'wb'))
    pickle.dump(similarity, open('similarity.pkl', 'wb'))

    return new_df, similarity


# ---------- LOAD OR CREATE ----------
if not os.path.exists('similarity.pkl'):
    movies, similarity = create_similarity()
else:
    movies_dict = pickle.load(open('movies_dict.pkl','rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl','rb'))


# ---------- TMDB POSTER ----------
def fetch_poster(movie_id):
    api_key = "b7760be1c771c05e2a66229c87313855"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)

    if response.status_code != 200:
        return "https://via.placeholder.com/300x450?text=No+Image"

    data = response.json()
    poster_path = data.get("poster_path")

    if poster_path is None:
        return "https://via.placeholder.com/300x450?text=No+Poster"

    return "https://image.tmdb.org/t/p/w500/" + poster_path


# ---------- RECOMMEND FUNCTION ----------
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
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ---------- UI ----------
st.title("🎬 Movie Recommender System")
st.write("Get similar movie recommendations with posters!")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)

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
