import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ----- Page configs -----
st.set_page_config(
    page_title="Temperatures Dashboard",
    page_icon="📊",
)

# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write("Interactive Project to load a dataset with information about the daily temperatures of 10 cities around the world, extract some insights using Pandas and displaying them with Matplotlib.")
    st.write("Data extracted from: https://www.kaggle.com/datasets/sudalairajkumar/daily-temperature-of-major-cities (with some cleaning and modifications).")

# ----- Title of the page -----
st.title("🌦️ Temperatures Dashboard")
st.divider()

# ----- Loading the dataset -----
@st.cache_data
def load_data():
    data_path = "data/cities_temperatures.csv"
    temps_df = pd.read_csv(data_path)
    if temps_df is not None:
        temps_df["Date"] = pd.to_datetime(temps_df["Date"]).dt.date
        temps_df["AvgTemperatureCelsius"] = (temps_df["AvgTemperatureFahrenheit"] - 32) * 5 / 9  # Convert to Celsius
    return temps_df

temps_df = load_data()

# Displaying the dataset in an expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(temps_df)

# ----- Extracting some basic information from the dataset -----
unique_countries_list = temps_df["City"].unique().tolist()
min_date = temps_df["Date"].min()
max_date = temps_df["Date"].max()
min_temp = temps_df["AvgTemperatureCelsius"].min()
max_temp = temps_df["AvgTemperatureCelsius"].max()
min_temp_row = temps_df.loc[temps_df["AvgTemperatureCelsius"].idxmin()]
max_temp_row = temps_df.loc[temps_df["AvgTemperatureCelsius"].idxmax()]
min_temp_city = min_temp_row["City"]
min_temp_date = min_temp_row["Date"]
max_temp_city = max_temp_row["City"]
max_temp_date = max_temp_row["Date"]

# ----- Displaying the extracted information metrics -----
st.write("##")
st.header("Basic Information")

cols1 = st.columns([4, 1, 6])
cols1[0].dataframe(pd.Series(unique_countries_list, name="Cities"), use_container_width=True)
cols1[2].write("#")
cols1[2].write(f"### ☃️ Min Temperature: {min_temp:.1f}°C\n*{min_temp_city} on {min_temp_date}*")
cols1[2].write("#")
cols1[2].write(f"### 🏜️ Max Temperature: {max_temp:.1f}°C\n*{max_temp_city} on {max_temp_date}*")

# ----- Plotting the temperatures over time for the selected cities -----
st.write("##")
st.header("Comparing the Temperatures of the Cities")

selected_cities = st.multiselect("Select the cities to compare:", unique_countries_list, default=["Buenos Aires", "Dakar"], max_selections=4)
cols2 = st.columns([6, 1, 6])
start_date = cols2[0].date_input("Select the start date:", min_date)
end_date = cols2[2].date_input("Select the end date:", max_date)

if len(selected_cities) > 0:
    c = st.container(border=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    for city in selected_cities:
        city_df = temps_df[temps_df["City"] == city]
        city_df_period = city_df[(city_df["Date"] >= start_date) & (city_df["Date"] <= end_date)]
        ax.plot(city_df_period["Date"], city_df_period["AvgTemperatureCelsius"], label=city)
    ax.set_title("Temperature Trends Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Avg Temperature (°C)")
    ax.legend()
    c.pyplot(fig)

    # Histogram
    fig, ax = plt.subplots(figsize=(10, 5))
    for city in selected_cities:
        city_df = temps_df[temps_df["City"] == city]
        city_df_period = city_df[(city_df["Date"] >= start_date) & (city_df["Date"] <= end_date)]
        ax.hist(city_df_period["AvgTemperatureCelsius"], alpha=0.5, label=city, bins=20)
    ax.set_title("Temperature Distribution")
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Frequency")
    ax.legend()
    c.pyplot(fig)
