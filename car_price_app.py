import os

import joblib
import pandas as pd
import streamlit as st

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'car_price_model.joblib')

BRANDS = ['Audi', 'BMW', 'Chevrolet', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Mercedes', 'Toyota', 'Volkswagen']
MODELS = [
    '3 Series', '5 Series', 'A3', 'A4', 'Accord', 'C-Class', 'CR-V', 'Camry', 'Civic', 'Corolla',
    'E-Class', 'Elantra', 'Equinox', 'Explorer', 'Fiesta', 'Focus', 'GLA', 'Golf', 'Impala',
    'Malibu', 'Optima', 'Passat', 'Q5', 'RAV4', 'Rio', 'Sonata', 'Sportage', 'Tiguan', 'Tucson', 'X5',
]
FUEL_TYPES = ['Diesel', 'Electric', 'Hybrid', 'Petrol']
TRANSMISSIONS = ['Automatic', 'Manual', 'Semi-Automatic']


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()

st.title('Bilprisprediktor')
st.write('Fyll i uppgifter om bilen i sidopanelen för att få ett predikterat pris.')

st.sidebar.header('Bilens uppgifter')
brand = st.sidebar.selectbox('Märke', BRANDS)
model_name = st.sidebar.selectbox('Modell', MODELS)
year = st.sidebar.slider('Årsmodell', min_value=2000, max_value=2023, value=2015)
engine_size = st.sidebar.slider('Motorstorlek (liter)', min_value=1.0, max_value=5.0, value=2.0, step=0.1)
fuel_type = st.sidebar.selectbox('Bränsletyp', FUEL_TYPES)
transmission = st.sidebar.selectbox('Växellåda', TRANSMISSIONS)
mileage = st.sidebar.number_input('Miltal (km)', min_value=0, max_value=500_000, value=50_000, step=1_000)
doors = st.sidebar.selectbox('Antal dörrar', [2, 3, 4, 5])
owner_count = st.sidebar.slider('Antal tidigare ägare', min_value=1, max_value=5, value=1)

if st.sidebar.button('Prediktera pris'):
    input_df = pd.DataFrame([{
        'Brand': brand,
        'Model': model_name,
        'Year': year,
        'Engine_Size': engine_size,
        'Fuel_Type': fuel_type,
        'Transmission': transmission,
        'Mileage': mileage,
        'Doors': doors,
        'Owner_Count': owner_count,
    }])

    predicted_price = model.predict(input_df)[0]
    st.success(f'Predikterat pris: {predicted_price:,.0f}'.replace(',', ' '))
