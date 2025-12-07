import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NutriPro", layout="wide")
st.title("🍎 Sistema Profesional de Evaluación Nutricional")
st.markdown("Calculadora clínica completa: ICC, Complexión, GET, Peso Ideal y Menú detallado con Macros en Kcal.")

# --- 2. BARRA LATERAL (DATOS COMPLETOS) ---
st.sidebar.header("1. Datos Personales")
nombre = st.sidebar.text_input("Nombre Paciente", "Paciente")
genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino"])
edad = st.sidebar.number_input("Edad", 10, 100, 25)
peso = st.sidebar.number_input("Peso (kg)", 30.0, 200.0, 70.0)
talla = st.sidebar.number_input("Talla (cm)", 100, 250, 170)

st.sidebar.header("2. Antropometría")
cintura = st.sidebar.number_input("Cintura (cm)", 40.0, 200.0, 80.0)
cadera = st.sidebar.number_input("Cadera (cm)", 40.0, 200.0, 95.0)
muneca = st.sidebar.number_input("Muñeca (cm)", 10.0, 30.0, 16.0)

st.sidebar.header("3. Antecedentes")
actividad = st.sidebar.selectbox("Nivel Actividad", 
    ["Sedentario (1.2)", "Ligero (1.375)", "Moderado (1.55)", "Intenso (1.725)"])
medicamentos = st.sidebar.text_area("Medicamentos", "Ninguno")

# --- 3. CÁLCULOS CLÍNICOS (BACKEND) ---
talla_m = talla / 100
imc = peso / (talla_m ** 2)

# Peso Ideal
factor_pi = 23 if genero == "Masculino" else 21.5
peso_ideal = (talla_m ** 2) * factor_pi

# Complexión (R = Talla/Muñeca)
r = talla / muneca
complexion = "Mediana"
if genero == "Masculino":
    if r > 10.4: complexion = "Pequeña"
    elif r < 9.6: complexion = "Grande"
else:
    if r > 11: complexion = "Pequeña"
    elif r < 10.1: complexion = "Grande"

# ICC (Cintura/Cadera)
icc = cintura / cadera
riesgo_icc = "Bajo"
limite = 0.90 if genero == "Masculino" else 0.85
if icc >= limite: riesgo_icc = "Alto (Obesidad Central)"

# TMB (Mifflin-St Jeor) y GET
if genero == "Masculino":
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) + 5
else:
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) - 161

# Factor actividad
if "Sedentario" in actividad: fa = 1.2
elif "Ligero" in actividad: fa = 1.375
elif "Moderado" in actividad: fa = 1.55
else: fa = 1.725
get = tmb * fa

# --- 4. RESULTADOS VISUALES ---
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Antropometría")
    st.metric("IMC", f"{imc:.1f}", f"Ideal: {peso_ideal:.1f}kg")
    st.metric("Complexión", complexion, f"r={r:.1f}")
    st.metric("ICC (Grasa)", f"{icc:.2f}", riesgo_icc)

with col2:
    st.subheader("⚡ Metabolismo")
    st.metric("Gasto Basal (TMB)", f"{int(tmb)} kcal")
    st.metric("Gasto Total (GET)", f"{int(get)} kcal", "Meta Diaria")

with col3:
    st.subheader("💊 Clínico")
    st.info(f"**Medicamentos:** {medicamentos}")
    st.write(f"**Hidratación:** {int(peso*35)} ml/día")

# --- 5. MENÚ INTELIGENTE (GRAMOS Y MACROS EN KCAL) ---
st.markdown("---")
st.header(f"🥗 Menú Detallado ({int(get)} kcal)")

# Factor de ajuste para las porciones
f = get / 2000

# Función segura para crear filas del menú (Anti-Error)
def agregar_dia(dia, des, com, cen, carbo_g, prot_g, gras_g):
    # Ajustar gramos de macros
    ch_g = carbo_g * f
    pr_g = prot_g * f
    gr_g = gras_g * f
    
    # Calcular Kcal aportadas por cada macro
    kcal_ch = ch_g * 4
