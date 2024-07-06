import streamlit as st
import pickle
import numpy as np

# Load pickled data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))


def recommend(book_name):
    # Returns the numerical index for the book_name
    index = np.where(pt.index == book_name)[0][0]

    # Sorts the similarities for the book_name in descending order
    similar_books = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    # To return result in list format
    data = []

    for idx, similarity in similar_books:
        item = {}
        # Get the book details by index
        temp_df = books[books['Book-Title'] == pt.index[idx]]

        # Add all relevant details to the result item
        item['title'] = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
        item['author'] = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
        item['publisher'] = temp_df.drop_duplicates('Book-Title')['Publisher'].values[0]
        item['publication_year'] = temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values[0]
        item['image'] = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]

        data.append(item)

    return data


st.title("Book Recommender System")

st.sidebar.header("Popular Books")
for i in range(len(popular_df)):
    st.sidebar.image(popular_df.iloc[i]['Image-URL-M'], width=100)
    st.sidebar.write(popular_df.iloc[i]['Book-Title'])
    st.sidebar.write(f"Author: {popular_df.iloc[i]['Book-Author']}")
    st.sidebar.write(f"Votes: {popular_df.iloc[i]['num_ratings']}")
    st.sidebar.write(f"Rating: {popular_df.iloc[i]['avg_rating']}")

st.header("Recommend Books")

# Dropdown menu for selecting a book
book_list = pt.index.tolist()
book_name = st.selectbox("Select a book", book_list)

if st.button("Recommend"):
    try:
        recommendations = recommend(book_name)
        for idx, book in enumerate(recommendations, start=1):
            with st.container():
                st.markdown(f"### {idx}. <u>{book['title']}</u>", unsafe_allow_html=True)
                st.image(book['image'], width=100)
                st.markdown(f"**Author**: {book['author']}")
                st.markdown(f"**Publisher**: {book['publisher']}")
                st.markdown(f"**Publication Year**: {book['publication_year']}")
                st.markdown("---")  # Add a horizontal line between books for better separation
    except IndexError:
        st.write("Book not found in the dataset.")

st.write("Powered by Streamlit")
