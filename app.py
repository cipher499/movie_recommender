"""
Streamlit app for the movie recommender system
author: @cipher499
date: 25/08/23
"""

import streamlit as st
import pickle 
import pandas as pd
import requests

# open the pickle objects
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies_df = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# function for fetching poster from the tmdb image api
def fetch_poster(movie_id):
    response = requests.get(
                "https://api.themoviedb.org/3/movie/{}?api_key=a312e3808b9a48d8bc6782e80c15f02a".format(movie_id))
    data = response.json()
    
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

# recommender function
def recommend(movie):
    """
    input: title of the movie
    output: returns titles of the 5 most similar movies
    """
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    rec_list = sorted(list(enumerate(distances)), 
                      key=lambda x: x[1], 
                      reverse=True)[1:6]
    
    rec_movies = []
    rec_movie_posters = []

    for i in rec_list:        
        # fetch movie names from the df
        rec_movies.append(movies_df.iloc[i[0]].title)

        # fetch posters from the api
        rec_movie_posters.append(fetch_poster(movies_df.iloc[i[0]].id))
    
    return rec_movies, rec_movie_posters

# set the display title
st.title("Movie Recommender System")

# add a selectbox
selected_movie_name = st.selectbox(
    'Select the movies you want the recommendations for',
    (movies_df["title"].values))

# add a button
if st.button("Recommend"):
    try:
        names, posters = recommend(selected_movie_name)
        
        if names:
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

        else:
            st.write("No recommendations found for the given movie.")
    
    except Exception as e:
        st.error(f"An error occured: {e}")
