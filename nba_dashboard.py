
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
import plotly.express as px
import streamlit as st

# -----------------------------
# 1. Get NBA Data (Current Season)
# -----------------------------
def get_player_stats(season='2024-25'):
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed='PerGame'
    ).get_data_frames()[0]
    return stats

# -----------------------------
# 2. Data Processing
# -----------------------------
df = get_player_stats()

# Convert per-game to per-36
df['PTS_per36'] = (df['PTS'] / df['MIN']) * 36
df['AST_per36'] = (df['AST'] / df['MIN']) * 36
df['REB_per36'] = (df['REB'] / df['MIN']) * 36

# True Shooting % approximation
df['TS%'] = df['PTS'] / (2 * (df['FGA'] + 0.44 * df['FTA']))

# -----------------------------
# 3. Streamlit Dashboard
# -----------------------------
st.set_page_config(page_title="NBA Player Performance Dashboard", layout="wide")

st.title("🏀 NBA Player Performance Dashboard")
st.markdown("Analyze per-36 stats, scoring efficiency, and usage trends.")

# Player filter
player_list = sorted(
    [p for p in df['PLAYER_NAME'].unique() if p is not None]
)

selected_player = st.selectbox("Select a Player", player_list)

# Scatter plot: Usage Rate vs TS%
fig1 = px.scatter(
    data_frame=df,
    x="FG_PCT",  # or any other existing column
    y="PTS",
    hover_name="PLAYER_NAME"
)


# Bar chart for selected player
player_stats = df[df['PLAYER_NAME'] == selected_player][['PTS_per36', 'AST_per36', 'REB_per36']].melt()
fig2 = px.bar(
    player_stats,
    x='variable',
    y='value',
    title=f"{selected_player} - Per 36 Minutes Stats",
    labels={'variable': 'Stat', 'value': 'Value'}
)

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
