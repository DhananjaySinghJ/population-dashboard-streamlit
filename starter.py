# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# URL of the dataset containing quarterly population data of Canada
URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv"

# Read the CSV file into a DataFrame with specified data types for each column
df = pd.read_csv(URL, dtype={'Quarter': str, 
                            'Canada': np.int32,
                            'Newfoundland and Labrador': np.int32,
                            'Prince Edward Island': np.int32,
                            'Nova Scotia': np.int32,
                            'New Brunswick': np.int32,
                            'Quebec': np.int32,
                            'Ontario': np.int32,
                            'Manitoba': np.int32,
                            'Saskatchewan': np.int32,
                            'Alberta': np.int32,
                            'British Columbia': np.int32,
                            'Yukon': np.int32,
                            'Northwest Territories': np.int32,
                            'Nunavut': np.int32})

# Set the title of the Streamlit app
st.title("Population of Canada")

# Add a markdown link to the source table
st.markdown("Source table can be found [here](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)")

# Add an expander to show the full data table when clicked
with st.expander("See full data table"):
    st.write(df)

# Create a form for user input
with st.form("population-form"):
    # Divide the form into three columns
    col1, col2, col3 = st.columns(3)

    # First column: Choose starting date
    with col1:
        st.write("Choose a starting date")
        start_quarter = st.selectbox("Quarter", options=["Q1", "Q2", "Q3", "Q4"], index=2, key="start_q")
        start_year = st.slider("Year", min_value=1991, max_value=2023, value=1991, step=1, key="start_y")

    # Second column: Choose ending date
    with col2:
        st.write("Choose an end date")
        end_quarter = st.selectbox("Quarter", options=["Q1", "Q2", "Q3", "Q4"], index=0, key="end_q")
        end_year = st.slider("Year", min_value=1991, max_value=2023, value=2023, step=1, key="end_y")
        
    # Third column: Choose location
    with col3:
        st.write("Choose a location")
        target = st.selectbox("Choose a location", options=df.columns[1:], index=0)

    # Submit button for the form
    submit_btn = st.form_submit_button("Analyze", type="primary")

# Format the selected dates into strings
start_date = f"{start_quarter} {start_year}"
end_date = f"{end_quarter} {end_year}"

# Function to format the date for comparison purposes
def format_date_for_comparison(date):
    if date[1] == 2:
        return float(date[2:]) + 0.25
    elif date[1] == 3:
        return float(date[2:]) + 0.50
    elif date[1] == 4:
        return float(date[2:]) + 0.75
    else:
        return float(date[2:])

# Function to check if the end date is before the start date
def end_before_start(start_date, end_date):
    num_start_date = format_date_for_comparison(start_date)
    num_end_date = format_date_for_comparison(end_date)

    if num_start_date > num_end_date:
        return True
    else:
        return False

# Function to display the dashboard based on the selected dates and location
def display_dashboard(start_date, end_date, target):
    # Create two tabs: Population change and Compare
    tab1, tab2 = st.tabs(["Population change", "Compare"])
    
    # Tab for population change
    with tab1:
        st.subheader(f"Population change from {start_date} to {end_date}")

        # Create two columns within the tab
        col1, col2 = st.columns(2)
        
        with col1:
            # Get the initial and final population values
            initial = df.loc[df['Quarter'] == start_date, target].item()
            final = df.loc[df['Quarter'] == end_date, target].item()

            # Calculate the percentage difference
            percentage_diff = round((final - initial) / initial * 100, 2)
            delta = f"{percentage_diff}%"
            st.metric(start_date, value=initial)
            st.metric(end_date, value=final, delta=delta)
        
        with col2:
            # Filter the dataframe to get the data between start and end dates
            start_idx = df.loc[df['Quarter'] == start_date].index.item()
            end_idx = df.loc[df['Quarter'] == end_date].index.item()
            filtered_df = df.iloc[start_idx: end_idx+1]

            # Plot the population data over time
            fig, ax = plt.subplots()
            ax.plot(filtered_df['Quarter'], filtered_df[target])
            ax.set_xlabel('Time')
            ax.set_ylabel('Population')
            ax.set_xticks([filtered_df['Quarter'].iloc[0], filtered_df['Quarter'].iloc[-1]])
            fig.autofmt_xdate()
            st.pyplot(fig)

    # Tab for comparing population data with other locations
    with tab2:
        st.subheader('Compare with other locations')
        all_targets = st.multiselect("Choose other locations", options=filtered_df.columns[1:], default=[target])
        
        # Plot the population data for selected locations over time
        fig, ax = plt.subplots()
        for each in all_targets:
            ax.plot(filtered_df['Quarter'], filtered_df[each])
        ax.set_xlabel('Time')
        ax.set_ylabel('Population')
        ax.set_xticks([filtered_df['Quarter'].iloc[0], filtered_df['Quarter'].iloc[-1]])
        fig.autofmt_xdate()
        st.pyplot(fig)

# Check if selected dates are within the available data range and if they are valid
if start_date not in df['Quarter'].tolist() or end_date not in df['Quarter'].tolist():
    st.error("No data available. Check your quarter and year selection")
elif end_before_start(start_date, end_date):
    st.error("Dates don't work. Start date must come before end date.")
else:
    display_dashboard(start_date, end_date, target)
