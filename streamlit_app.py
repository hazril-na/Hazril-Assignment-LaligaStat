import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="LaLiga Player Stats Dashboard", layout="wide")

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("laliga_player_stats_english.csv")
    return df

df = load_data()

st.title("⚽ LaLiga Player Stats Dashboard")

# 2. Cek Nama Kolom Dataset
st.subheader("📝 Nama Kolom Dataset")
st.write(df.columns.tolist())    # ini untuk melihat nama kolom

# 3. Tampilkan Data Awal
st.subheader("📋 Preview Dataset")
st.dataframe(df.head())

# Sidebar Filters
# -----------------------------
st.sidebar.header("Filter Data")

teams = df['Team'].unique()
selected_team = st.sidebar.selectbox("Select Team", options=teams)

positions = df['Position'].unique()
selected_position = st.sidebar.multiselect("Select Position(s)", options=positions, default=positions)

min_goals = int(df['Goals scored'].min())
max_goals = int(df['Goals scored'].max())
goal_range = st.sidebar.slider("Filter by Goals Scored", min_value=min_goals, max_value=max_goals, value=(min_goals, max_goals))

filtered_df = df[
    (df['Team'] == selected_team) &
    (df['Position'].isin(selected_position)) &
    (df['Goals scored'].between(goal_range[0], goal_range[1]))
]

st.subheader("📊 Filtered Data")
st.dataframe(filtered_df)

# -----------------------------
# Visualization 1: Goals by Player
# -----------------------------
st.subheader(f"⚽ Top Goal Scorers in {selected_team}")
top_scorers = filtered_df.sort_values(by='Goals scored', ascending=False).head(10)

fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.barplot(data=top_scorers, x='Goals scored', y='Name', ax=ax1, palette="viridis")
ax1.set_xlabel("Goals Scored")
ax1.set_ylabel("Player")
ax1.set_title("Top 10 Goal Scorers")
st.pyplot(fig1)

# -----------------------------
# Visualization 2: Goals vs Assists Scatter
# -----------------------------
st.subheader("⚽ Goals vs Assists Scatter Plot")
fig2, ax2 = plt.subplots(figsize=(7, 5))
sns.scatterplot(data=filtered_df, x='Goals scored', y='Assists', hue='Position', ax=ax2, s=100)
ax2.set_xlabel("Goals Scored")
ax2.set_ylabel("Assists")
st.pyplot(fig2)

# -----------------------------
# Basic Stats
# -----------------------------
st.subheader("📈 Basic Statistics")
st.metric("Total Players", len(filtered_df))
st.metric("Total Goals", int(filtered_df['Goals scored'].sum()))
st.metric("Total Assists", int(filtered_df['Assists'].sum()))
