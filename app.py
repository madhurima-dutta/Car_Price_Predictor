import streamlit as st
import pandas as pd
import pickle

# Set page configuration
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Load the model
@st.cache_resource
def load_model():
    try:
        with open('car_price_model.pkl', 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# App title
st.title("🚗 Used Car Price Predictor")
st.markdown("""
This app predicts the price of a used car based on its features.
Fill in the details below and click 'Predict Price' to get an estimate.
""")

# Create form
with st.form("prediction_form"):
    st.subheader("Car Details")

    col1, col2 = st.columns(2)
    with col1:
        brand = st.selectbox("Car Brand", options=[
            'Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault', 'Mahindra', 'Tata',
            'Chevrolet', 'Datsun', 'Jeep', 'Mercedes-Benz', 'Mitsubishi', 'Audi', 'Volkswagen',
            'BMW', 'Nissan', 'Lexus', 'Jaguar', 'Land', 'MG', 'Volvo', 'Daewoo', 'Kia', 'Fiat',
            'Force', 'Ambassador', 'Ashok', 'Isuzu', 'Opel'
        ])
        year = st.number_input("Year of Manufacture", min_value=1990, max_value=2025, value=2015)
        km_driven = st.number_input("Kilometers Driven", min_value=0, max_value=500000, value=50000)
        fuel = st.selectbox("Fuel Type", options=['Diesel', 'Petrol', 'LPG', 'CNG'])
        seller_type = st.selectbox("Seller Type", options=['Individual', 'Dealer', 'Trustmark Dealer'])

    with col2:
        transmission = st.selectbox("Transmission", options=['Manual', 'Automatic'])
        owner = st.selectbox("Owner Type", options=[
            'First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner', 'Test Drive Car'
        ])
        mileage = st.number_input("Mileage (kmpl)", min_value=0.0, max_value=50.0, value=20.0, step=0.1)
        engine = st.number_input("Engine Capacity (CC)", min_value=500, max_value=5000, value=1200)
        max_power = st.number_input("Max Power (bhp)", min_value=20.0, max_value=500.0, value=80.0, step=0.1)
        seats = st.number_input("Number of Seats", min_value=2, max_value=10, value=5)

    submit_button = st.form_submit_button(label="Predict Price")

# Predict
if submit_button:
    if model is not None:
        try:
            car_age = 2025 - year  # Your model uses this

            input_data = pd.DataFrame({
                'brand': [brand],
                'year': [year],
                'km_driven': [km_driven],
                'fuel': [fuel],
                'seller_type': [seller_type],
                'transmission': [transmission],
                'owner': [owner],
                'mileage': [mileage],
                'engine': [engine],
                'max_power': [max_power],
                'seats': [seats],
                'car_age': [car_age]
            })

            st.markdown("#### Input Preview:")
            st.dataframe(input_data)

            prediction = model.predict(input_data)[0]
            prediction = max(50000, prediction)

            st.success(f"### Predicted Car Price: ₹{prediction:,.2f}")

            if prediction < 200000:
                st.info("This appears to be a budget-friendly car.")
            elif prediction < 500000:
                st.info("This appears to be a mid-range car.")
            elif prediction < 1000000:
                st.info("This appears to be a premium car.")
            else:
                st.info("This appears to be a luxury car.")

        except Exception as e:
            st.error(f"Error making prediction: {e}")
            st.info("Please check if the input values match the expected format for the model.")
    else:
        st.error("Model failed to load. Please ensure 'car_price_model.pkl' exists in the same directory.")

# Sidebar info
st.sidebar.header("About")
st.sidebar.info("This app uses a machine learning model trained on used car data to predict selling prices.")

st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Enter the car's details in the form  
2. Click **Predict Price**  
3. Minimum predicted price is ₹50,000
""")

st.sidebar.header("How to Run")
st.sidebar.code("streamlit run app.py")

st.markdown("---")
st.markdown("Car Price Prediction App | Made with Streamlit")
