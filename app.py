import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="NutriMeta", layout="wide")
st.title("🍎 NutriMeta: Peso Ideal y Menús")

# --- 2. DATOS ---
st.sidebar.header("Datos Personales")
genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino"])
edad = st.sidebar.number_input("Edad", 10, 100, 30)
peso = st.sidebar.number_input("Peso (kg)", 30.0, 200.0, 85.0)
talla = st.sidebar.number_input("Talla (cm)", 100, 250, 170)

st.sidebar.header("Medidas")
cintura = st.sidebar.number_input("Cintura (cm)", 40.0, 200.0, 95.0)
cadera = st.sidebar.number_input("Cadera (cm)", 40.0, 200.0, 105.0)
muneca = st.sidebar.number_input("Muñeca (cm)", 10.0, 30.0, 17.0)
actividad = st.sidebar.selectbox("Actividad", 
    ["Sedentario (1.2)", "Ligero (1.375)", "Moderado (1.55)", "Intenso (1.725)"])
medicamentos = st.sidebar.text_area("Medicamentos", "Ninguno")

# --- 3. CÁLCULOS ---
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
limite = 0.90 if genero == "Masculino" else 0.85
if icc >= limite: riesgo_icc = "Alto"

# TMB y GET
if genero == "Masculino":
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) + 5
else:
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) - 161

fa = 1.2
if "Ligero" in actividad: fa = 1.375
if "Moderado" in actividad: fa = 1.55
if "Intenso" in actividad: fa = 1.725
get_mant = tmb * fa

# META
meta_kcal = get_mant
objetivo = "MANTENER"
if imc > 25:
    objetivo = "BAJAR (Déficit)"
    meta_kcal = get_mant - 500
    if meta_kcal < 1200: meta_kcal = 1200
elif imc < 18.5:
    objetivo = "SUBIR (Superávit)"
    meta_kcal = get_mant + 300

# --- 4. RESULTADOS ---
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("IMC", f"{imc:.1f}", f"Ideal: {peso_ideal:.1f}kg")
c2.metric("META DIARIA", f"{int(meta_kcal)} kcal", objetivo)
c3.metric("Gasto Actual", f"{int(get_mant)} kcal", "Mantenimiento")
st.info(f"Complexión: {complexion} | ICC: {icc:.2f} ({riesgo_icc}) | Agua: {int(peso*35)} ml")

# --- 5. MENÚ SEGURO (LÍNEAS CORTAS) ---
st.markdown("---")
st.header(f"🥗 Menú Objetivo ({int(meta_kcal)} kcal)")

f = meta_kcal / 2000

def fila(dia, d, c, n, ch, pro, gr):
    return {
        "Día": dia, "Desayuno": d, "Comida": c, "Cena": n,
        "Total Kcal": int((ch*4 + pro*4 + gr*9)*f),
        "CH (cal)": int(ch*4*f), "PRO (cal)": int(pro*4*f), "GR (cal)": int(gr*9*f)
    }

lista = []

# LUNES
d = f"{int(40*f)}g Avena"
d += f" + {int(150*f)}ml Leche"
c = f"{int(120*f)}g Pollo"
c += f" + {int(60*f)}g Quinoa"
n = f"Ensalada Atún ({int(100*f)}g)"
n += " + 1 Tostada"
lista.append(fila("Lunes", d, c, n, 220, 110, 60))

# MARTES
d = f"2 Huevos ({int(100*f)}g)"
d += " + 1 Pan Integral"
c = f"{int(150*f)}g Pescado"
c += f" + {int(100*f)}g Arroz"
n = f"{int(200*f)}ml Yogurt"
n += f" + {int(15*f)}g Nueces"
lista.append(fila("Martes", d, c, n, 190, 120, 70))

# MIÉRCOLES
d = f"Licuado: {int(250*f)}ml Leche"
d += " + Plátano"
c = f"{int(120*f)}g Res Magra"
c += " + Nopales"
n = f"Quesadillas: {int(60*f)}g Queso"
n += " + 2 Tortillas"
lista.append(fila("Miércoles", d, c, n, 210, 115, 65))

# JUEVES
d = f"{int(150*f)}g Queso Cottage"
d += " + Fruta + Tostada"
c = f"Lentejas ({int(150*f)}g)"
c += " + Verduras"
n = f"Sandwich Pavo ({int(60*f)}g)"
n += " + Aguacate"
lista.append(fila("Jueves", d, c, n, 200, 105, 60))

# VIERNES
d = f"Omelet Espinacas"
d += f" ({int(100*f)}g huevo)"
c = f"Pasta ({int(60*f)}g crudo)"
c += f" + {int(100*f)}g Pollo"
n = f"Tacos Lechuga Atún ({int(100*f)}g)"
lista.append(fila("Viernes", d, c, n, 230, 110, 55))

# SÁBADO
d = "Hotcakes Avena (2 pzas)"
d += " + Fruta"
c = f"Ceviche ({int(150*f)}g pescado)"
c += " + 2 Tostadas"
n = "Molletes: 1 Bolillo"
n += f" + {int(40*f)}g Queso"
lista.append(fila("Sábado", d, c, n, 210, 100, 75))

# DOMINGO
d = "Pan Francés"
d += f" + {int(100*f)}ml Claras"
c = f"Pollo Rostizado ({int(120*f)}g)"
c += " + Ensalada"
n = "Sopa Verduras"
n += f" + {int(80*f)}g Pollo"
lista.append(fila("Domingo", d, c, n, 190, 125, 60))

df = pd.DataFrame(lista)
st.dataframe(df, use_container_width=True, hide_index=True)

st.download_button("📥 Descargar (CSV)", df.to_csv(index=False).encode('utf-8'), "dieta.csv",
