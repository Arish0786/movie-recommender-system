import streamlit as st
import pickle
import gzip
import requests

st.set_page_config(page_title="Movie Recommender System", layout="wide")
st.markdown("""<style>
    .movie-card {
        background-color: #1E293B;
        color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    img {
        border-radius: 10px;
        width: 100%;
        height: auto;
    }
</style>""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US&api_key=f2e2bef701cc1ae76aedc8718cf3a720'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if not poster_path:
            return "https://via.placeholder.com/200?text=No+Image"
        return f"https://image.tmdb.org/t/p/original/{poster_path}"
    except (requests.RequestException, KeyError):
        return "https://via.placeholder.com/200?text=Error+Fetching+Image"

def load_compressed_file(file_path):
    print(f"Loading {file_path}...")
    try:
        with gzip.open(file_path, 'rb') as f:
            data = pickle.load(f)
        print(f"✅ Loaded {file_path} successfully!")
        return data
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies_names = []
        recommended_movies_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].id
            recommended_movies_names.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies_names, recommended_movies_posters
    except IndexError:
        st.error("Movie not found. Please try a different movie.")
        return [], []

st.title(':clapper: Movie Recommender System')

url = 'https://drive.google.com/file/d/1HA3hdXbTp9yqOl9Hh2inn9tO0EVTzDMS/view?usp=sharing'
response = requests.get(url)
with open('similarity.pkl', 'wb') as f:
    f.write(response.content)
# Load the compressed files
movies = load_compressed_file('movies_compressed.pkl.gz')
similarity = pickle.load(open('similarity.pkl', 'rb'))

if movies is None or similarity is None:
    st.error("Failed to load data. Please check your files.")
else:
    movie_list = movies['title'].values
    selected_movie_name = st.selectbox('🎬 Select a Movie', movie_list)

    if st.button('🚀 Show Recommendations'):
        with st.spinner('Fetching recommendations...'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

            if recommended_movie_names:
                st.subheader('You Might Like These Movies:')
                cols = st.columns(5)
                for i, col in enumerate(cols):
                    with col:
                        st.markdown(f"""<div class='movie-card'>
                        <img src='{recommended_movie_posters[i]}' alt='Movie Poster'>
                        <h4>{recommended_movie_names[i]}</h4>
                        </div>""", unsafe_allow_html=True)
            else:
                st.warning('No recommendations available. Please try another movie.')
