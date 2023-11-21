import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
def load_data():
    hour_data = pd.read_csv('hour.csv')
    hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
    day_data = pd.read_csv('day.csv')
    return hour_data, day_data

hour_data, day_data = load_data()

# Change weathersit based on dataset description
weather_conditions = {
    1: "Clear",
    2: "Mist",
    3: "Light Snow",
    4: "Heavy Rain"
}


# Sidebar
analysis_type = st.sidebar.radio("Choose Analysis Type", ('Bike Rental Frequency', 'Bike Rental Analysis'))

if analysis_type == 'Bike Rental Frequency':
    st.title('Bike Sharing Demand Dashboard')
    st.subheader('Frequency of Rental Based on Day and Hour')
    # Convert min and max date to datetime objects
    min_date = hour_data['dteday'].min().to_pydatetime()
    max_date = hour_data['dteday'].max().to_pydatetime()

    # Date picker for selecting a date
    selected_date = st.date_input('Select a date', value=min_date, min_value=min_date, max_value=max_date)

    # Slider for selecting an hour
    selected_hour = st.slider('Select an hour', 0, 23, 0)

    # Filter data based on selected date and hour
    filtered_data = hour_data[(hour_data['dteday'] == pd.Timestamp(selected_date)) & (hour_data['hr'] == selected_hour)]

    # Create column for bike rented and weather conditions
    col1, col2 = st.columns(2)

    if not filtered_data.empty:
        # Display the total number of bikes rented
        with col1:
            total_rent = filtered_data['cnt'].sum()
            st.metric(f"Total bikes rented on {selected_date} at {selected_hour}:00 is", value = total_rent)


        # Display weather conditions
        with col2:
            weather_condition = filtered_data.iloc[0]  # Assuming the weather condition is consistent for the hour
            with st.expander(f"Weather Conditions on {selected_date} at {selected_hour}:00"):
                st.write(f"Weather Situation: {weather_conditions.get(weather_condition['weathersit'], 'Unknown')}")
                st.write(f"Temperature: {weather_condition['temp']}")
                st.write(f"Humidity: {weather_condition['hum']}")
                st.write(f"Wind Speed: {weather_condition['windspeed']}")
          
        # Plotting
        plt.figure(figsize=(6, 4))
        plt.bar(['Casual', 'Registered'], [filtered_data['casual'].sum(), filtered_data['registered'].sum()])
        plt.xlabel('User Type')
        plt.ylabel('Number of Bikes Rented')
        plt.title(f'Bike Rentals by User Type on {selected_date} at {selected_hour}:00')
        st.pyplot(plt)
    
    else:
        st.write("No data available for the selected date and hour.")

elif analysis_type == 'Bike Rental Analysis':
    st.title('Time Peak Analysis of Bike Rentals')
    st.subheader('Time Peak Analysis of Bike Rentals')
    # Hourly data plot
    hourly_rentals = hour_data.groupby('hr')['cnt'].mean().reset_index()
    st.bar_chart(hourly_rentals)

    # Daily data plot
    day_data['dteday'] = pd.to_datetime(day_data['dteday'])

    plt.figure(figsize=(15, 6))
    plt.plot(day_data['dteday'], day_data['cnt'], lw=1)
    plt.title('Daily Bike Rentals Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Number of Rentals')
    plt.grid(True)
    st.pyplot(plt)

    st.title('Weather Conditions of Bike Rentals')

    st.subheader('Correlation between Weather Conditions and Bike Rentals')
    # Correlation heatmap
    weather_related_columns = ['season', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'cnt']
    correlation_matrix = day_data[weather_related_columns].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0)
    st.pyplot(plt)

