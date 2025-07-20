import streamlit as st
import pickle
import pandas as pd
import requests

# Fetch poster from TMDB with fallback to OMDb
def fetch_poster(movie_id, movie_title=None):
    try:
        # Primary - TMDB
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            raise ValueError("No poster in TMDB")
    except:
        # Fallback - OMDb
        try:
            omdb_api_key = 'c4b6ef6e'  # 🔑 Replace this with your OMDb API key
            omdb_url = f"http://www.omdbapi.com/?t={movie_title}&apikey={omdb_api_key}"
            omdb_response = requests.get(omdb_url)
            omdb_data = omdb_response.json()
            if omdb_data['Response'] == 'True' and omdb_data.get('Poster') != 'N/A':
                return omdb_data['Poster']
        except:
            pass
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movie_title)
        recommended_movies_posters.append(fetch_poster(movie_id, movie_title))  # ✅ pass both

    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
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
