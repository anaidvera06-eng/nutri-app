import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="NutriMeta", layout="wide")
st.title("🍎 NutriMeta: Cálculo para Peso Ideal")
st.markdown("Calcula calorías exactas para llegar al peso ideal (Déficit/Superávit) con menú detallado.")

# --- 2. DATOS DEL PACIENTE ---
st.sidebar.header("Datos Personales")
nombre = st.sidebar.text_input("Nombre", "Paciente")
genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino"])
edad = st.sidebar.number_input("Edad", 10, 100, 30)
peso = st.sidebar.number_input("Peso Actual (kg)", 30.0, 200.0, 85.0)
talla = st.sidebar.number_input("Talla (cm)", 100, 250, 170)

st.sidebar.header("Medidas")
cintura = st.sidebar.number_input("Cintura (cm)", 40.0, 200.0, 95.0)
cadera = st.sidebar.number_input("Cadera (cm)", 40.0, 200.0, 105.0)
muneca = st.sidebar.number_input("Muñeca (cm)", 10.0, 30.0, 17.0)

st.sidebar.header("Estilo de Vida")
actividad = st.sidebar.selectbox("Nivel Actividad", 
    ["Sedentario (1.2)", "Ligero (1.375)", "Moderado (1.55)", "Intenso (1.725)"])
medicamentos = st.sidebar.text_area("Medicamentos", "Ninguno")

# --- 3. CÁLCULOS (CEREBRO DE LA APP) ---

# Antropometría
talla_m = talla / 100
imc = peso / (talla_m ** 2)

# Peso Ideal
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
limit_icc = 0.90 if genero == "Masculino" else 0.85
if icc >= limit_icc: riesgo_icc = "Alto (Obesidad Central)"

# TMB (Mifflin-St Jeor)
if genero == "Masculino":
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) + 5
else:
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) - 161

# GET Mantenimiento
fa = 1.2
if "Ligero" in actividad: fa = 1.375
if "Moderado" in actividad: fa = 1.55
if "Intenso" in actividad: fa = 1.725
get_mant = tmb * fa

# CÁLCULO DE LA META (DÉFICIT O SUPERÁVIT)
meta_kcal = get_mant
objetivo = "MANTENER PESO"

if imc > 25: # Sobrepeso
    objetivo = "BAJAR PESO (Déficit)"
    meta_kcal = get_mant - 500
    if meta_kcal < 1200: meta_kcal = 1200 # Seguridad
elif imc < 18.5: # Bajo Peso
    objetivo = "SUBIR PESO (Superávit)"
    meta_kcal = get_mant + 300

# --- 4. RESULTADOS ---
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Diagnóstico IMC", f"{imc:.1f}", f"Ideal: {peso_ideal:.1f}kg")
c2.metric("META DIARIA", f"{int(meta_kcal)} kcal", objetivo)
c3.metric("Gasto Actual", f"{int(get_mant)} kcal", "Mantenimiento")

st.info(f"Complexión: {complexion} | ICC: {icc:.2f} ({riesgo_icc}) | Hidratación: {int(peso*35)} ml/día")

# --- 5. MENÚ DETALLADO (ANTI-ERROR) ---
st.markdown("---")
st.header(f"🥗 Menú Objetivo ({int(meta_kcal)} kcal)")

# Factor de ajuste
f = meta_kcal / 2000

# Función segura para agregar días
def fila(dia, d, c, n, ch_g, pro_g, gr_g):
    ch_k = int(ch_g * f * 4)
    pro_k = int(pro_g * f * 4)
    gr_k = int(gr_g * f * 9)
    total = ch_k + pro_k + gr_k
    return {
        "Día": dia, "Desayuno": d, "Comida": c, "Cena": n,
        "Total Kcal": total, "CH (kcal)": ch_k, "PRO (kcal)": pro_k, "GR (kcal)": gr_k
    }

lista = []

# LUNES
d = f"{int(40*f)}g Avena + {int(150*f)}ml Leche + {int(100*f)}g Fruta"
c = f"{int(120*f)}g Pollo + {int(150*f)}g Verdura + {int(60*f)}g Quinoa"
n = f"Ensalada Atún ({int(100*f)}g) + 1 Tostada"
lista.append(fila("Lunes", d, c, n, 220, 110, 60))

# MARTES
d = f"2 Huevos ({int(100*f)}g) + 1 Pan Integral + Verdura"
c = f"{int(150*f)}g Pescado + {int(100*f)}g Arroz + Ensalada"
n = f"{int(200*f)}ml Yogurt Griego + {int(15*f)}g Nueces"
lista.append(fila("Martes", d, c, n, 190, 120, 70))

# MIÉRCOLES
d = f"Licuado: {int(250*f)}ml Leche + Plátano + {int(15*f)}g Crema Cacahuate"
c = f"{int(120*f)}g Res Magra + Nopales + Frijoles ({int(100*f)}g)"
n = f"Quesadillas: {int(60*f)}g Queso + 2 Tortillas Maíz"
lista.append(fila("Miércoles", d, c, n, 210, 115, 65))

# JUEVES
d = f"{int(150*f)}g Queso Cottage + {int(100*f)}g Fruta +
