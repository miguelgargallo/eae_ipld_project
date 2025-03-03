import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ----- Page configs -----
st.set_page_config(
    page_title="Netflix Data Analysis",
    page_icon="📊",
)

# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write(
        "Interactive Project to load a dataset with information about Netflix Movies and Series, extract some insights using Pandas and displaying them with Matplotlib.")
    st.write(
        "Data extracted from: https://www.kaggle.com/datasets/shivamb/netflix-shows (with some cleaning and modifications)")

# ----- Title of the page -----
st.title("🎬 Netflix Data Analysis")
st.divider()


# ----- Loading the dataset -----

@st.cache_data
def load_data():
    data_path = "data/netflix_titles.csv"
    movies_df = pd.read_csv(data_path, index_col="show_id")  # Load dataset and set index

    # Convert duration to numeric
    movies_df["duration"] = movies_df["duration"].str.extract(r'(\d+)').astype(float)

    return movies_df


movies_df = load_data()

# Displaying the dataset in an expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(movies_df)

# ----- Extracting some basic information from the dataset -----
min_year = movies_df["release_year"].min()
max_year = movies_df["release_year"].max()
num_missing_directors = movies_df["director"].isna().sum()
n_countries = movies_df["country"].nunique()
avg_title_length = movies_df["title"].str.len().mean()

# ----- Displaying the extracted information metrics -----
st.write("##")
st.header("Basic Information")

cols1 = st.columns(5)
cols1[0].metric("Min Release Year", min_year)
cols1[1].metric("Max Release Year", max_year)
cols1[2].metric("Missing Dir. Names", num_missing_directors)
cols1[3].metric("Countries", n_countries)
cols1[4].metric("Avg Title Length", str(round(avg_title_length, 2)))

# ----- Pie Chart: Top year producer countries -----
st.write("##")
st.header("Top Year Producer Countries")

cols2 = st.columns(2)
year = cols2[0].number_input("Select a year:", min_year, max_year, 2005)

top_10_countries = movies_df[movies_df["release_year"] == year]["country"].value_counts().head(10)

if not top_10_countries.empty:
    fig = plt.figure(figsize=(8, 8))
    plt.pie(top_10_countries, labels=top_10_countries.index, autopct="%.2f%%")
    plt.title(f"Top 10 Countries in {year}")
    st.pyplot(fig)
else:
    st.subheader("⚠️ No data available for the selected year.")

# ----- Line Chart: Avg duration of movies by year -----
st.write("##")
st.header("Avg Duration of Movies by Year")

movies_avg_duration_per_year = movies_df[movies_df["type"] == "Movie"].groupby("release_year")["duration"].mean()

if not movies_avg_duration_per_year.empty:
    fig = plt.figure(figsize=(9, 6))
    plt.plot(movies_avg_duration_per_year.index, movies_avg_duration_per_year, marker='o', linestyle='-')
    plt.xlabel("Year")
    plt.ylabel("Avg Duration (minutes)")
    plt.title("Average Duration of Movies Across Years")
    st.pyplot(fig)
else:
    st.subheader("⚠️ No movie duration data available.")
