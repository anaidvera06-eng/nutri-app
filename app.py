import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="NutriApp Pro", layout="wide")

# --- TÍTULO ---
st.title("🍎 Sistema de Evaluación Nutricional")
st.markdown("Calculadora clínica completa con Menús Inteligentes y Guía Educativa.")

# --- DATOS DEL PACIENTE ---
st.sidebar.header("1. Datos Generales")
genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino"])
edad = st.sidebar.number_input("Edad", 10, 100, 25)
peso = st.sidebar.number_input("Peso (kg)", 30.0, 200.0, 70.0)
talla = st.sidebar.number_input("Talla (cm)", 100, 250, 170)

st.sidebar.header("2. Medidas")
cintura = st.sidebar.number_input("Cintura (cm)", 40.0, 200.0, 80.0)
cadera = st.sidebar.number_input("Cadera (cm)", 40.0, 200.0, 95.0)
muneca = st.sidebar.number_input("Muñeca (cm)", 10.0, 30.0, 16.0)

st.sidebar.header("3. Actividad")
actividad = st.sidebar.selectbox("Nivel Actividad", 
    ["Sedentario", "Ligero", "Moderado", "Intenso", "Muy Intenso"])

enfermedades = st.sidebar.multiselect("Patologías", 
    ["Ninguna", "Diabetes", "Hipertensión", "Obesidad"])

# --- CÁLCULOS ---
talla_m = talla / 100
imc = peso / (talla_m ** 2)

# Peso Ideal
factor = 23 if genero == "Masculino" else 21.5
peso_ideal = (talla_m ** 2) * factor

# ICC
icc = cintura / cadera
riesgo_icc = "Bajo"
limit_icc = 0.90 if genero == "Masculino" else 0.85
if icc >= limit_icc: riesgo_icc = "Alto (Obesidad Central)"

# Complexión
r = talla / muneca
complexion = "Mediana"
if genero == "Masculino":
    if r > 10.4: complexion
