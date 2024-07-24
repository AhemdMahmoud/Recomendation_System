import streamlit as st
import pandas as pd
import numpy as np
import difflib
import os

def main():
    st.title("Movie Recommendation System")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Streamlit Movie Recommendation System</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    # Check if files exist
    movies_path = '/content/movies.csv'
    similarity_path = '/content/similarity.npy'

    if not os.path.exists(movies_path):
        st.error(f"File not found: {movies_path}")
        return
    if not os.path.exists(similarity_path):
        st.error(f"File not found: {similarity_path}")
        return

    # Load movies data
    movies_data = pd.read_csv(movies_path)
    similarity = np.load(similarity_path)  # Load your similarity matrix

    # Select a movie from the dropdown
    selected_movie_name = st.selectbox('Select your favorite movie', movies_data['title'].values)

    # Find the closest match for the selected movie
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(selected_movie_name, list_of_all_titles)

    if find_close_match:
        close_match = find_close_match[0]
        index_of_the_movie = movies_data[movies_data.title == close_match].index.values[0]

        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

        st.write('Movies suggested for you:')
        i = 1
        for movie in sorted_similar_movies:
            index = movie[0]
            title_from_index = movies_data.iloc[index]['title']
            if i < 5:
                st.write(f"{i}. {title_from_index}")
                i += 1
    else:
        st.write("No close matches found for the selected movie.")

if __name__ == '__main__':
    main()

