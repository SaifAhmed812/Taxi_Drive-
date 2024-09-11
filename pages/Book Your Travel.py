import streamlit as st
import pandas as pd
import pickle
import joblib
from datetime import datetime, timedelta
from io import BytesIO
import requests

# URLs for the pickle files
url_preprocessor = "https://raw.githubusercontent.com/SaifAhmed812/Taxi_Drive-/31bd35217e7316fdd7ba971f7a2570228114eeab/preprocessor.pkl"
url_model = "https://raw.githubusercontent.com/SaifAhmed812/Taxi_Drive-/f188a2c8712d35ac0e60d55ee3ec53c1b3279336/model_RD"

# Function to download a file from a URL and load it
def load_pickle_from_url(url, loader):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    return loader(BytesIO(response.content))

# Load the preprocessor
preprocessor = load_pickle_from_url(url_preprocessor, joblib.load)
# Load the model
model = load_pickle_from_url(url_model, pickle.load)

# Load your dataframes
url1 = "https://raw.githubusercontent.com/SaifAhmed812/Taxi_Drive-/8eae5a633f1daf373cbbcb61548f8dfae5592ea7/Data/_Cleaned_locations.csv"
url2 = "https://raw.githubusercontent.com/SaifAhmed812/Taxi_Drive-/8eae5a633f1daf373cbbcb61548f8dfae5592ea7/Data/Locations%20and%20codes.csv"
dfx = pd.read_csv(url1)
dfx2 = pd.read_csv(url2)

# Get unique locations
unique_pickup_locations = dfx['Column1'].unique().tolist()
#unique_dropoff_locations = dfx['Column2'].unique().tolist()

st.title("Taxi Fare Prediction")

def get_payment_code(value):
    payment_codes = {'cash': 1, 'credit': 2, 'mobile': 3, 'prcard': 4}
    return payment_codes.get(value, None)

def get_code_from_location(location):
    result = dfx2.loc[dfx2['pick_up_location'] == location, 'pulocationid']
    if not result.empty:
        return result.iloc[0]
    else:
        st.error(f"Location {location} not found")
        return None

def get_trip_distance(pick_up_location, drop_of_location):
    trip_distance = dfx[
        (dfx['Column1'] == pick_up_location) & (dfx['Column2'] == drop_of_location)
    ]['Column3'].values
    if trip_distance.size > 0:
        return trip_distance[0]
    else:
        return None

def get_trip_duration(current_hour, dropoff_hour):
    now = datetime.now()
    pick_up_time = now.replace(hour=current_hour, minute=0, second=0, microsecond=0)
    dropoff_time = now.replace(hour=dropoff_hour, minute=0, second=0, microsecond=0)

    # If drop-off time is earlier than pick-up time, assume it's on the next day
    if dropoff_time < pick_up_time:
        dropoff_time += timedelta(days=1)

    duration = dropoff_time - pick_up_time
    total_seconds = int(duration.total_seconds())

    hours = total_seconds // 3600
    seconds = total_seconds % 3600

    return hours, seconds

def get_unique_dropoff_locations(dfx , pick_up_location) :
    unique_dropoff_locations = dfx[dfx['Column1'] == pick_up_location]['Column2'].unique()

    return unique_dropoff_locations


with st.form(key="form1"):
    passenger_count = st.number_input("Passenger Count", 1, 5)
    Tip = st.number_input("Tip amount", min_value=0.0)
    pick_up_location = st.selectbox("Select Pick-Up Location", options=unique_pickup_locations)
  
    unique_dropoff_locations = get_unique_dropoff_locations(dfx,pick_up_location)#get drop off locations

    drop_of_location = st.selectbox("Select Drop-Off Location", options=unique_dropoff_locations)
    payment_type = st.selectbox("Payment Type", ["credit", "cash", "mobile", "prcard"])

    submit = st.form_submit_button(label="Submit")

    if submit:
        now = datetime.now()
        current_hour = now.hour

        code = get_payment_code(payment_type)
        drop_location = get_code_from_location(drop_of_location)
        pick_location = get_code_from_location(pick_up_location)

        if drop_location is None or pick_location is None:
            st.error("Invalid pick-up or drop-off location.")
        else:
            trip_distance = get_trip_distance(pick_up_location, drop_of_location)

            if trip_distance is None:
                trip_distance = 1.7510  # mean value
            else:
                trip_distance = float(trip_distance)

            new_data = {
                'passenger_count': passenger_count,
                'trip_distance': trip_distance,
                'ratecodeid': 1,
                'payment_type': code,
                "extra": 1.7412 ,#mean
                "mta_tax": 0.5,#constant
                "tip_amount": Tip,
                'congestion_surcharge': 2.422, #mean
                'pick_up_location': pick_location,
                'drop_of_location': drop_location,
                'pick_up_day': now.day,
                'pickup_hour': current_hour
            }

            new_data_df = pd.DataFrame(new_data, index=[0])

            if new_data_df.isna().any().any() or (new_data_df == float('inf')).any().any():
                st.error("Input data contains NaN or infinite values.")
            else:
                # Preprocess the new data
                new_data_preprocessed = preprocessor.transform(new_data_df)

                # Predict using the model
                try:
                    y_pred = model.predict(new_data_preprocessed)

                    # Assuming y_pred is an array with the first element being the fare amount
                    fare_amount = y_pred[0][0]  # Extract fare_amount
                    dropoff_hour = y_pred[0][1]  # Extract dropoff_hour

                    hours, seconds = get_trip_duration(current_hour, int(dropoff_hour))
                    if pick_up_location ==  drop_of_location :
                            fare_amount = 0.00

                    st.markdown('# Price in USD:')
                    st.markdown(f'## **${fare_amount:,.2f}**')
                    

                except Exception as e:
                    st.error(f"An error occurred during prediction: {e}")
