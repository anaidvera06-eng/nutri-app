import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="NutriPro Meta", layout="wide")
st.title("🍎 Sistema Nutricional: Meta Peso Ideal")
st.markdown("Calcula el requerimiento exacto para llegar al **Peso Ideal** y genera el menú acorde.")

# --- 2. DATOS DEL PACIENTE ---
st.sidebar.header("1. Datos Personales")
nombre = st.sidebar.text_input("Nombre", "Paciente")
genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino"])
edad = st.sidebar.number_input("Edad", 10, 100, 25)
peso = st.sidebar.number_input("Peso Actual (kg)", 30.0, 200.0, 80.0) # Puse 80kg para probar reducción
talla = st.sidebar.number_input("Talla (cm)", 100, 250, 170)

st.sidebar.header("2. Medidas y Estilo de Vida")
cintura = st.sidebar.number_input("Cintura (cm)", 50.0, 200.0, 90.0)
cadera = st.sidebar.number_input("Cadera (cm)", 50.0, 200.0, 105.0)
muneca = st.sidebar.number_input("Muñeca (cm)", 10.0, 30.0, 17.0)
actividad = st.sidebar.selectbox("Nivel Actividad", 
    ["Sedentario (1.2)", "Ligero (1.375)", "Moderado (1.55)", "Intenso (1.725)"])
medicamentos = st.sidebar.text_area("Medicamentos", "Ninguno")

# --- 3. CÁLCULOS CLÍNICOS ---

# A) Antropometría
talla_m = talla / 100
imc = peso / (talla_m ** 2)

# Peso Ideal (Lorentz/Broca ajustado)
factor_pi = 23 if genero == "Masculino" else 21.5
peso_ideal = (talla_m ** 2) * factor_pi

# Complexión
r = talla / muneca
complexion = "Mediana"
if genero == "Masculino":
    if r > 10.4: complexion = "Pequeña"
    elif r < 9.6: complexion = "Grande"
else:
    if r > 11: complexion = "Pequeña"
    elif r < 10.1: complexion = "Grande"

# ICC
icc = cintura / cadera
riesgo_icc = "Bajo"
limite = 0.90 if genero == "Masculino" else 0.85
if icc >= limite: riesgo_icc = "Alto (Obesidad Central)"

# B) Energética (Mifflin-St Jeor)
if genero == "Masculino":
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) + 5
else:
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) - 161

# Factor Actividad
fa = 1.2
if "Ligero" in actividad: fa = 1.375
if "Moderado" in actividad: fa = 1.55
if "Intenso" in actividad: fa = 1.725

get_mantenimiento = tmb * fa

# C) CÁLCULO DE LA META (Lógica para llegar al Peso Ideal)
# Estrategia clínica estándar: +/- 500 kcal para cambio sostenible
objetivo = "Mantener Peso"
get_meta = get_mantenimiento

if imc > 25.0: # Sobrepeso/Obesidad
    objetivo = "PERDER PESO (Déficit)"
    get_meta = get_mantenimiento - 500 # Déficit estándar
    if get_meta < 1200: get_meta = 1200 # Límite de seguridad
elif imc < 18.5: # Bajo Peso
    objetivo = "GANAR PESO (Superávit)"
    get_meta = get_mantenimiento + 300 # Superávit moderado

# --- 4. MOSTRAR DIAGNÓSTICO ---
st.markdown("---")
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("📊 Diagnóstico")
    st.metric("Peso Actual", f"{peso} kg", f"IMC: {imc:.1f}")
    st.metric("Peso Ideal Meta", f"{peso_ideal:.1f} kg", complexion)
    st.write(f"**ICC:** {icc:.2f}
