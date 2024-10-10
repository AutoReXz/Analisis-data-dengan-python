import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(
    page_title="Bike Rental Analysis Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Function to load data
@st.cache_data
def load_data():
    df_day = pd.read_csv("Dataset/day.csv")
    df_hour = pd.read_csv("Dataset/hour.csv")
    
    # Convert date columns
    df_day["dteday"] = pd.to_datetime(df_day["dteday"])
    df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])
    
    # Create mappings
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_map = {1: 'Clear', 2: 'Mist/Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
    workingday_map = {0: 'Holiday', 1: 'Working Day'}
    
    # Apply mappings
    df_day['season_name'] = df_day['season'].map(season_map)
    df_day['weather_desc'] = df_day['weathersit'].map(weather_map)
    df_day['day_type'] = df_day['workingday'].map(workingday_map)
    df_hour['day_type'] = df_hour['workingday'].map(workingday_map)
    
    return df_day, df_hour

# Load data
df_day, df_hour = load_data()

# Dashboard title and description
st.title("🚲 Bike Rental Analysis Dashboard")
st.markdown("""
This dashboard provides comprehensive insights into bike rental patterns, helping to optimize 
rental operations and improve customer service.
""")

# Sidebar
with st.sidebar:
    st.header("Filters")
    year_filter = st.selectbox(
        "Select Year", 
        options=[0, 1], 
        format_func=lambda x: f"Year {x+1}"
    )
    season_filter = st.multiselect(
        "Select Seasons", 
        options=['Spring', 'Summer', 'Fall', 'Winter'], 
        default=['Spring', 'Summer', 'Fall', 'Winter']
    )
    
    # Add time range selector
    st.subheader("Time Range")
    hour_range = st.slider(
        "Select Hour Range",
        min_value=0,
        max_value=23,
        value=(0, 23)
    )

# Filter data based on selections
filtered_day_data = df_day[
    (df_day['yr'] == year_filter) &
    (df_day['season_name'].isin(season_filter))
]

filtered_hour_data = df_hour[
    (df_hour['yr'] == year_filter) &
    (df_hour['hr'].between(hour_range[0], hour_range[1]))
]

# Key Metrics Row
st.subheader("Key Performance Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    avg_daily_rentals = int(filtered_day_data['cnt'].mean())
    st.metric("Avg Daily Rentals", avg_daily_rentals)
with col2:
    max_daily_rentals = int(filtered_day_data['cnt'].max())
    st.metric("Max Daily Rentals", max_daily_rentals)
with col3:
    total_rentals = int(filtered_day_data['cnt'].sum())
    st.metric("Total Rentals", f"{total_rentals:,}")
with col4:
    avg_temp = round(filtered_day_data['temp'].mean() * 41, 1)
    st.metric("Avg Temperature (°C)", avg_temp)

# Main dashboard layout
tab1, tab2, tab3 = st.tabs(["Daily Patterns", "Seasonal Analysis", "Weather Impact"])

with tab1:
    st.subheader("Workday vs Holiday Analysis")
    hourly_avg = filtered_hour_data.groupby(['hr', 'day_type'])['cnt'].mean().reset_index()
    fig_hourly = px.line(
        hourly_avg,
        x='hr',
        y='cnt',
        color='day_type',
        title="Hourly Rental Patterns: Working Day vs Holiday",
        labels={'hr': 'Hour of Day', 'cnt': 'Average Rentals', 'day_type': 'Day Type'},
        color_discrete_map={'Holiday': 'blue', 'Working Day': 'red'}
    )
    fig_hourly.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Average Rentals",
        legend_title="Day Type",
        hovermode="x unified"
    )
    st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Add insights box
    with st.expander("📊 Insights on Daily Patterns"):
        st.write("""
        - **Peak Hours**: Working days show clear peaks during commute hours (8AM and 5PM)
        - **Midday Usage**: Holidays have more consistent usage throughout the day
        - **Early Morning**: Both types show minimal rentals between 2AM-5AM
        """)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Seasonal Rental Patterns")
        season_avg = filtered_day_data.groupby('season_name')['cnt'].agg(
            mean='mean',
            std='std'
        ).reset_index()
        fig_season = px.bar(
            season_avg, 
            x='season_name', 
            y='mean',
            error_y='std',  # Menggunakan deviasi standar sebagai error bars
            title="Average Rentals by Season (with standard deviation)",
            labels={'mean': 'Average Rentals', 'season_name': 'Season'},
            color='season_name'
        )
        st.plotly_chart(fig_season, use_container_width=True)
    
    with col2:
        st.subheader("Monthly Trends")
        monthly_avg = filtered_day_data.groupby(
            filtered_day_data['dteday'].dt.month
        )['cnt'].mean().reset_index()
        monthly_avg['month'] = monthly_avg['dteday'].apply(
            lambda x: pd.to_datetime(f"2024-{x}-01").strftime('%B')
        )
        fig_monthly = px.line(
            monthly_avg,
            x='month',
            y='cnt',
            title="Average Rentals by Month",
            labels={'cnt': 'Average Rentals', 'month': 'Month'}
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Weather Impact")
        weather_avg = filtered_day_data.groupby('weather_desc')['cnt'].mean().reset_index()
        fig_weather = px.bar(
            weather_avg,
            x='weather_desc',
            y='cnt',
            title="Average Rentals by Weather Condition",
            labels={'cnt': 'Average Rentals', 'weather_desc': 'Weather Condition'},
            color='weather_desc'
        )
        st.plotly_chart(fig_weather, use_container_width=True)
    
    with col2:
        st.subheader("Temperature vs Rentals")
        fig_temp = px.scatter(
            filtered_day_data,
            x='temp',
            y='cnt',
            title="Temperature vs Number of Rentals",
            labels={'cnt': 'Number of Rentals', 'temp': 'Temperature (normalized)'},
            trendline="ols"
        )
        st.plotly_chart(fig_temp, use_container_width=True)

# Insights and Recommendations
st.subheader("Key Insights and Recommendations")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Key Insights 🔍
    1. **Seasonal Impact**
       - Fall and Summer show highest rental numbers
       - Winter has lowest average rentals
    2. **Daily Patterns**
       - Clear peaks during commute hours on working days
       - More consistent usage throughout holidays
    3. **Weather Influence**
       - Clear weather leads to more rentals
       - Strong correlation between temperature and rental numbers
    """)

with col2:
    st.markdown("""
    ### Business Recommendations 💡
    1. **Inventory Management**
       - Optimize bike availability during peak seasons
       - Consider maintenance scheduling during off-peak times
    2. **Pricing Strategy**
       - Implement weather-based pricing
       - Different pricing for working days vs holidays
    3. **Marketing Campaigns**
       - Promote off-peak usage with special offers
       - Target recreational riders for holidays
    """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("Dashboard created by Galang")
with col2:
    st.markdown("Data last updated: 2024-03-14")
with col3:
    st.markdown("[Download Report](https://example.com)")
