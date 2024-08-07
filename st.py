import streamlit as st
import pandas as pd
import time
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:Shankii007@localhost/redbus')



def load_data(query):
    return pd.read_sql(query, engine)

def get_route_names(operator):
    query = f"SELECT DISTINCT Route_name FROM {operator}_bus_details"
    df = load_data(query)
    return df['Route_name'].tolist()

def get_buses_for_route(operator, route_name):
    query = f"""
    SELECT * FROM {operator}_bus_details
    WHERE Route_name = '{route_name}'
    """
    return load_data(query)

st.set_page_config(
    page_title="REDBUS",
   page_icon=r"C:\Users\shank\Desktop\redbus\redbus-logo.png", 
    layout="wide"
)
st.markdown("""
<style>
h1 {
    color: red; /* Change to your desired color */
},
h2 {
    color: red; /* Change to your desired color */
            }
</style>
""", unsafe_allow_html=True)
#Progress = st.progress(0)
#for i in range(100):
   # time.sleep(0.05)
    #Progress.progress(i+1)
#st.balloons()
with st.spinner('Loading...'):
    # Simulate a long-running operation
    time.sleep(2)

def main():
    option = st.sidebar.radio("Page Options",["Home","Bus Details"])
    if option == "Home":
        st.title("About RedBus")
        st.write("""
        RedBus is an online bus ticket booking platform that allows users to book tickets for travel in India and other countries. 
        The company was founded in 2005 by a group of people from BITS Pilani, an engineering college in India, who wanted to provide 
        customers with the convenience of booking tickets online. RedBus is headquartered in Bangalore and works with a network of more 
        than 3,500 bus operators across India, Malaysia, Indonesia, Singapore, Peru, and Colombia
""")
        #st.image(r"C:\Users\shank\Desktop\img.jpg")
        st.write("Redbus Video")
        st.video("https://youtu.be/eyAAUGhvZu8?si=XV5H_Xe6KV-Rikzm")
        st.markdown("[REDBUS](https://www.redbus.in/)")
    else:
        st.sidebar.header("Bus Details")
        st.title("RedBus Dashbord")


        operator = st.sidebar.selectbox(
            "Choose a bus operator",
            ("APSRTC","KERALARTC","TSRTC","HRTC","RSRTC","SBSTC","UPSRTC","WBTC","CTU")  # Add more operators as needed
        )

        # Display route names based on selected operator
        if operator:
            route_names = get_route_names(operator.lower())
            selected_route = st.sidebar.selectbox("Select a route", ["Select a route"] + route_names)
            
            if selected_route != "Select a route":
                # Display buses for selected route
                st.write(f"Showing buses for route: {selected_route}")
                buses_df = get_buses_for_route(operator, selected_route)
                
                col1,col2= st.columns(2 , gap ="medium")
                col3,col4 = st.columns(2 , gap ="medium")
                
                st.sidebar.header("Filters")
            

                min_rating =col1.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=0.0)
                max_rating =col2.slider("Maximum Rating", min_value=0.0, max_value=5.0, value=5.0)

                min_price = col3.slider("Min_Price", min_value = 0 , max_value = 1000,value = 0)
                max_price = col4.slider("Max_Price", min_value = 0 , max_value = 1000,value = 1000)

                # Departure and Arrival Time filters
                min_departure_time = st.sidebar.time_input("Earliest Departure Time", value=pd.Timestamp("00:00").time())
                max_departure_time = st.sidebar.time_input("Latest Departure Time", value=pd.Timestamp("23:59").time())
                min_arrival_time = st.sidebar.time_input("Earliest Arrival Time", value=pd.Timestamp("00:00").time())
                max_arrival_time = st.sidebar.time_input("Latest Arrival Time", value=pd.Timestamp("23:59").time())

                # Convert times to strings for filtering
                buses_df['Departure_time'] = pd.to_datetime(buses_df['Departure_time'], format='%H:%M').dt.time
                buses_df['Arrival_time'] = pd.to_datetime(buses_df['Arrival_time'], format='%H:%M').dt.time

                filtered_data =  buses_df[
                        (buses_df["Ratings"]>=min_rating) & 
                        (buses_df["Ratings"]<= max_rating) &
                        (buses_df["Price"]>=min_price) & 
                        (buses_df["Price"]<= max_price) &
                        (buses_df['Departure_time'] >= min_departure_time) &
                        (buses_df['Departure_time'] <= max_departure_time) &
                        (buses_df['Arrival_time'] >= min_arrival_time) &
                        (buses_df['Arrival_time'] <= max_arrival_time)
                        ]
            
                st.write("Filtered Data")
                st.dataframe(filtered_data)
           
                

             
                
            else:
                st.write("Please select a route to view available buses.")
        else:
            st.write("Please select a bus operator to start.")

if __name__ == "__main__":
    main()
       