import json
import os
import streamlit as st
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict

# Load books from JSON file
BOOKS_FILE = "books.json"
BOOKS = []

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOKS = json.load(f)

# Prepare the feature matrix for KNN
def prepare_data(books: List[Dict[str, str]]) -> np.ndarray:
    """Prepare feature matrix using TF-IDF for names and encoding for genre."""
    if not books:
        return np.array([])

    names = [book["name"] for book in books]
    genres = [book["genre"] for book in books]
    
    # Convert names to TF-IDF features
    vectorizer = TfidfVectorizer()
    name_features = vectorizer.fit_transform(names).toarray()
    
    # Combine name features with genre (one-hot encode genres)
    genre_features = np.array([[1, 0] if genre == "fiction" else [0, 1] for genre in genres])
    features = np.hstack((name_features, genre_features))
    return features

# Streamlit UI
st.title("Book Recommendation System")

# Book name input
book_name = st.text_input("Enter the name of the book:")

if st.button("Get Recommendations"):
    if not book_name:
        st.error("Please enter a book name.")
    else:
        # Prepare features and check the number of books
        features = prepare_data(BOOKS)
        
        if features.size == 0:
            st.error("No books available for recommendations.")
        else:
            # Fit the KNN model
            knn = NearestNeighbors(n_neighbors=3)  # Adjust n_neighbors as needed
            knn.fit(features)

            # Normalize the book name for case-insensitive matching
            normalized_book_name = book_name.lower()

            # Find the index of the book that matches the provided name
            book_index = next((index for index, book in enumerate(BOOKS) if book["name"].lower() == normalized_book_name), None)

            if book_index is None:
                st.error(f"No book found with the name '{book_name}'.")
            else:
                # Get the features of the book to find recommendations for
                query_features = features[book_index].reshape(1, -1)

                # Get the indices of the nearest neighbors
                distances, indices = knn.kneighbors(query_features)

                # Collect recommended books, excluding the original book
                recommendations = [BOOKS[i] for i in indices[0] if i != book_index]

                if not recommendations:
                    st.warning("No recommendations found for the book you entered.")
                else:
                    st.success("Recommended Books:")
                    for rec in recommendations:
                        st.write(f"**{rec['name']}** - Genre: {rec['genre']} - Price: ${rec['price']:.2f}")
