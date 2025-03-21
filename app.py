import pickle
import streamlit as st
import requests

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: #000000;
            color: white;
            font-family: Arial, sans-serif;
        }
        .stButton>button {
            background-color: #1DB954;
            color: white;
            border-radius: 25px;
            padding: 10px 20px;
            font-size: 18px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #1ed760;
        }
        img {
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.8);
        }
        .stSelectbox>div>div {
            background-color: #333333;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


st.header('🎬 Movie Recommender System')
st.write('Discover movies tailored to your taste!')
import pickle
import lzma

def load_compressed_pickle(file_path):
    with lzma.open(file_path, 'rb') as file:
        return pickle.load(file)

similarity = load_compressed_pickle('similarity.pkl.xz')
movies = pickle.load(open('movies.pkl', 'rb'))


movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)

    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.image(poster, caption=name, use_container_width=True)

