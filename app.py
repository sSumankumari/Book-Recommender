import streamlit as st
import pickle
import numpy as np

# Load pickled data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

def recommend_books(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    recommended_books = []
    for i in similar_items:
        item = {}
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item['title'] = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
        item['author'] = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
        item['image'] = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]
        recommended_books.append(item)
    return recommended_books

st.title("Book Recommender System")

st.sidebar.header("Popular Books")
for i in range(len(popular_df)):
    st.sidebar.image(popular_df.iloc[i]['Image-URL-M'], width=100)
    st.sidebar.write(popular_df.iloc[i]['Book-Title'])
    st.sidebar.write(f"Author: {popular_df.iloc[i]['Book-Author']}")
    st.sidebar.write(f"Votes: {popular_df.iloc[i]['num_ratings']}")
    st.sidebar.write(f"Rating: {popular_df.iloc[i]['avg_rating']}")

st.header("Recommend Books")

book_name = st.text_input("Enter a book name")
if st.button("Recommend"):
    try:
        recommendations = recommend_books(book_name)
        for book in recommendations:
            st.image(book['image'], width=100)
            st.write(book['title'])
            st.write(f"Author: {book['author']}")
    except IndexError:
        st.write("Book not found in the dataset.")

st.write("Powered by Streamlit")
