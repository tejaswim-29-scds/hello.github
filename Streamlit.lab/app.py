import streamlit as st
import pandas

# Set the title of the Streamlit application
st.title("IMDb Top 250 Movies Dashboard")

# Add a short introduction
st.write("Explore the IMDb Top 250 movies using the options below.")

# Read the CSV file
movies = pandas.read_csv("ToP 250 movies on imdb in 2026-selected-columns.csv")

# Show the total number of movies
st.metric("Total Movies", len(movies))

st.divider()

# Create a search box for movie titles
st.subheader("Search Movies")
search_title = st.text_input("Enter a movie title")

# Start with all movies
filtered_movies = movies.copy()

# Filter movies when the user enters a title
if search_title:
    filtered_movies = filtered_movies[
        filtered_movies["primaryTitle"].str.contains(
            search_title, case=False, na=False
        )
    ]

# Create a content rating filter
st.subheader("Filter Movies")
available_ratings = sorted(movies["contentRating"].dropna().unique())

selected_ratings = st.multiselect(
    "Choose content ratings",
    available_ratings,
    default=available_ratings
)

filtered_movies = filtered_movies[
    filtered_movies["contentRating"].isin(selected_ratings)
]

# Display the filtered movie list
st.subheader("Movie List")
st.write("Number of movies found:", len(filtered_movies))

st.dataframe(
    filtered_movies[
        ["primaryTitle", "originalTitle", "type", "contentRating", "description"]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

# Let the user choose one movie to view its details
st.subheader("Movie Details")

if len(filtered_movies) > 0:
    movie_titles = filtered_movies["primaryTitle"].dropna().tolist()
    selected_movie_title = st.selectbox("Select a movie", movie_titles)

    selected_movie = filtered_movies[
        filtered_movies["primaryTitle"] == selected_movie_title
    ].iloc[0]

    st.header(selected_movie["primaryTitle"])

    st.write("**Original Title:**", selected_movie["originalTitle"])
    st.write("**Movie Type:**", selected_movie["type"])
    st.write("**Content Rating:**", selected_movie["contentRating"])
    st.write("**Description:**", selected_movie["description"])

    # Display the movie poster if an image link is available
    if pandas.notna(selected_movie["primaryImage"]):
        st.image(selected_movie["primaryImage"], caption=selected_movie["primaryTitle"])

    # Display the IMDb page link if available
    if pandas.notna(selected_movie["url"]):
        st.markdown(f"[Open IMDb Page]({selected_movie['url']})")

else:
    st.warning("No movies found. Try changing your search or filter.")

