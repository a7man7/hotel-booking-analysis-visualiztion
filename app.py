import streamlit as st
import pandas as pd
import joblib

# Load Pipeline
model = joblib.load("models/hotel_cancellation_model.pkl")

st.title("Hotel Booking Cancellation Prediction")

hotel = st.selectbox("Hotel", ["Resort Hotel", "City Hotel"])

lead_time = st.number_input("Lead Time", min_value=0)

arrival_date_year = st.number_input(
    "Arrival Year",
    min_value=2015,
    max_value=2030,
    value=2017
)

arrival_date_month = st.selectbox(
    "Month",
    [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]
)

arrival_date_week_number = st.number_input(
    "Week Number",
    min_value=1,
    max_value=53,
    value=1
)

arrival_date_day_of_month = st.number_input(
    "Day",
    min_value=1,
    max_value=31,
    value=1
)

stays_in_weekend_nights = st.number_input(
    "Weekend Nights",
    min_value=0,
    value=1
)

stays_in_week_nights = st.number_input(
    "Week Nights",
    min_value=0,
    value=2
)

adults = st.number_input("Adults", min_value=1, value=2)
children = st.number_input("Children", min_value=0, value=0)
babies = st.number_input("Babies", min_value=0, value=0)

meal = st.selectbox(
    "Meal",
    ["BB", "HB", "FB", "SC"]
)

country = st.text_input("Country", value="PRT")

market_segment = st.selectbox(
    "Market Segment",
    ["Online TA", "Offline TA/TO", "Direct", "Groups"]
)

distribution_channel = st.selectbox(
    "Distribution Channel",
    ["TA/TO", "Direct", "Corporate"]
)

is_repeated_guest = st.selectbox(
    "Repeated Guest",
    [0, 1]
)

previous_cancellations = st.number_input(
    "Previous Cancellations",
    min_value=0,
    value=0
)

previous_bookings_not_canceled = st.number_input(
    "Previous Bookings Not Canceled",
    min_value=0,
    value=0
)

reserved_room_type = st.text_input(
    "Reserved Room Type",
    value="A"
)

booking_changes = st.number_input(
    "Booking Changes",
    min_value=0,
    value=0
)

deposit_type = st.selectbox(
    "Deposit Type",
    ["No Deposit", "Non Refund", "Refundable"]
)

days_in_waiting_list = st.number_input(
    "Days In Waiting List",
    min_value=0,
    value=0
)

customer_type = st.selectbox(
    "Customer Type",
    ["Transient", "Transient-Party", "Contract", "Group"]
)

adr = st.number_input(
    "ADR",
    min_value=0.0,
    value=100.0
)

required_car_parking_spaces = st.number_input(
    "Parking Spaces",
    min_value=0,
    value=0
)

total_of_special_requests = st.number_input(
    "Special Requests",
    min_value=0,
    value=0
)

if st.button("Predict"):

    total_nights = (
        stays_in_weekend_nights +
        stays_in_week_nights
    )

    total_guests = (
        adults +
        children +
        babies
    )

    is_family = int(
        (children + babies) > 0
    )

    had_prev_cancel = int(
        previous_cancellations > 0
    )

    adr_per_guest = adr / max(total_guests, 1)

    data = pd.DataFrame([{
        "hotel": hotel,
        "lead_time": lead_time,
        "arrival_date_year": arrival_date_year,
        "arrival_date_month": arrival_date_month,
        "arrival_date_week_number": arrival_date_week_number,
        "arrival_date_day_of_month": arrival_date_day_of_month,
        "stays_in_weekend_nights": stays_in_weekend_nights,
        "stays_in_week_nights": stays_in_week_nights,
        "adults": adults,
        "children": children,
        "babies": babies,
        "meal": meal,
        "country": country,
        "market_segment": market_segment,
        "distribution_channel": distribution_channel,
        "is_repeated_guest": is_repeated_guest,
        "previous_cancellations": previous_cancellations,
        "previous_bookings_not_canceled": previous_bookings_not_canceled,
        "reserved_room_type": reserved_room_type,
        "booking_changes": booking_changes,
        "deposit_type": deposit_type,
        "days_in_waiting_list": days_in_waiting_list,
        "customer_type": customer_type,
        "adr": adr,
        "required_car_parking_spaces": required_car_parking_spaces,
        "total_of_special_requests": total_of_special_requests,
        "total_nights": total_nights,
        "total_guests": total_guests,
        "is_family": is_family,
        "had_prev_cancel": had_prev_cancel,
        "adr_per_guest": adr_per_guest
    }])

    prediction = model.predict(data)

    if prediction[0] == 1:
        st.error("Booking Will Be Cancelled")
    else:
        st.success("Booking Will Not Be Cancelled")



        #write in terminal streamlit run app.py