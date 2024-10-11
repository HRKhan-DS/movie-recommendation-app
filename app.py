import streamlit as st
import pickle
import pandas as pd
import requests
import gzip
import os

# Provide a link to download similarity.pkl.gz (uncomment and replace with actual link)
# st.markdown("### Download Similarity File")
# st.write("You can download the similarity file from [this link](your_new_link_here)")

# Function to fetch movie poster image URL from TMDb API
def fetch_poster(movie_id):
    # Construct the URL for the movie details using TMDb API
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=30da0cb097077501009ee8d9392ddcd6&language=en-US"

    # Send an HTTP GET request to fetch movie data
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract the poster_path from the response
        poster_path = data.get('poster_path')
        
        # Check if poster_path exists
        if poster_path:
            # Construct the full URL for the movie poster image
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
    return "https://via.placeholder.com/500x750?text=No+Poster+Available"  # Default image if no poster

# Function to recommend similar movies
def recommend(movie):
    # Find the index of the selected movie in the DataFrame
    movie_index = movies[movies['title'] == movie].index[0]

    # Get the similarity scores for the selected movie
    distances = similarity[movie_index]

    # Sort the movies by similarity in descending order and select the top 5 (excluding the selected one)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    # Fetch movie posters and names for the recommended movies
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, recommended_movie_posters

# Load movie data and similarity matrix from pickle files
try:
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)

    # Load the compressed similarity file
    with gzip.open('similarity.pkl.gz', 'rb') as f:
        similarity = pickle.load(f)
except FileNotFoundError:
    st.error("Movie data or similarity file not found. Please ensure the files are in the correct location.")
    st.stop()  # Stop execution if files are not found
except Exception as e:
    st.error(f"An error occurred while loading data: {e}")
    st.stop()  # Stop execution for other errors

# Set the title of the web application
st.title('Movie Recommendation App')

# Create a select box for users to choose a movie
selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values)

# Button to trigger the recommendation
if st.button('Show Recommendation'):
    # Call the recommend function to get recommendations
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    # Create five columns for displaying recommendations
    cols = st.columns(5)

    # Display recommended movie names and posters
    for i in range(len(recommended_movie_names)):
        with cols[i % 5]:  # Wrap around if there are more than 5 recommendations
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])

# Larger gap using multiple <br> tags
st.markdown("<br><br><br><br>", unsafe_allow_html=True)

# Instructions for Movie Recommendation App
st.write("Welcome to the Movie Recommendation App!")
st.write("Discover your next favorite movie with our recommendation engine.")
st.write("To get started, select your movie preferences from the dropdown.")
st.write("Click the 'Show Recommendation' button to see a list of recommended movies.")



