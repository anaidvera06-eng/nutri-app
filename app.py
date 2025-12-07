import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Evaluación Nutricional", layout="wide")

# --- TÍTULO PRINCIPAL ---
st.title("🍎 Sistema de Evaluación Nutricional Integral")
st.markdown("""
Calculadora clínica completa: GET, IMC, ICC, Hidratación y Menús Personalizados.
**Versión Profesional:** Porciones exactas y medidas caseras.
""")

# --- BARRA LATERAL (DATOS) ---
st.sidebar.header("1. Datos Generales")
nombre = st.sidebar.text_input("Nombre", "Paciente")
genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino"])
edad = st.sidebar.number_input("Edad", 10, 100, 25)
peso = st.sidebar.number_input("Peso Actual (kg)", 30.0, 200.0, 70.0)
talla = st.sidebar.number_input("Talla (cm)", 100, 250, 170)

st.sidebar.header("2. Medidas Antropométricas")
cintura = st.sidebar.number_input("Cintura (cm)", 40.0, 200.0, 80.0)
cadera = st.sidebar.number_input("Cadera (cm)", 40.0, 200.0, 95.0)
muneca = st.sidebar.number_input("Circunferencia Muñeca (cm)", 10.0, 30.0, 16.0)

st.sidebar.header("3. Estilo de Vida")
actividad = st.sidebar.selectbox("Nivel de Actividad", 
    ["Sedentario (Poco o nada)", 
     "Ligero (1-3 días/sem)", 
     "Moderado (3-5 días/sem)", 
     "Intenso (6-7 días/sem)", 
     "Muy Intenso (Doble sesión)"])

enfermedades = st.sidebar.multiselect("Patologías", 
    ["Ninguna", "Diabetes Tipo 2", "Hipertensión", "Obesidad", "Colesterol Alto"])

medicamentos = st.sidebar.text_area("Medicamentos", "Ninguno")

# --- LÓGICA MATEMÁTICA (BACKEND) ---

# 1. Cálculos Básicos
talla_m = talla / 100
imc = peso / (talla_m ** 2)

# 2. Peso Ideal
factor_peso_ideal = 23 if genero == "Masculino" else 21.5
peso_ideal = (talla_m ** 2) * factor_peso_ideal

# 3. ICC (Índice Cintura-Cadera)
icc = cintura / cadera
riesgo_icc = "Bajo"
if genero == "Masculino":
    if icc >= 0.90: riesgo_icc = "Obesidad Central (Riesgo Alto)"
else:
    if icc >= 0.85: riesgo_icc = "Obesidad Central (Riesgo Alto)"

# 4. Complexión Corporal
r = talla / muneca
complexion = "Mediana" 
if genero == "Masculino":
    if r > 10.4: complexion = "Pequeña"
    elif 9.6 <= r <= 10.4: complexion = "Mediana"
    else: complexion = "Grande"
else: 
    if r > 11: complexion = "Pequeña"
    elif 10.1 <= r <= 11: complexion = "Mediana"
    else: complexion = "Grande"

# 5. TMB y GET
if genero == "Masculino":
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) + 5
else:
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) - 161

factores_actividad = {
    "Sedentario (Poco o nada)": 1.2,
    "Ligero (1-3 días/sem)": 1.375,
    "Moderado (3-5 días/sem)": 1.55,
    "Intenso (6-7 días/sem)": 1.725,
    "Muy Intenso (Doble sesión)": 1.9
}
get = tmb * factores_actividad[actividad]

# 6. Hidratación
agua_ml = peso * 35

# --- MOSTRAR RESULTADOS ---
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Diagnóstico")
    estado_imc = "Normal"
    if imc < 18.5: estado_imc = "Bajo Peso"
    elif imc >= 25 and imc < 30: estado_imc = "Sobrepeso"
    elif imc >= 30: estado_imc = "Obesidad"
    st.metric("IMC", f"{imc:.1f}", estado_imc)
    st.metric("Peso Ideal", f"{peso_ideal:.1f} kg")

with col2:
    st.subheader("⚡ Calorías")
    st.metric("Metabolismo Basal", f"{int(tmb)} kcal")
    st.metric("Gasto Total (GET)", f"{int(get)} kcal", "Meta Diaria")

with col3:
    st.subheader("💧 Hidratación")
    st.metric("Agua Diaria", f"{int(agua_ml)} ml", f"{int(agua_ml/250)} vasos")
    st.metric("Complexión", complexion)

# Alertas Clínicas
if "Diabetes Tipo 2" in enfermedades:
    st.warning("⚠️ **Alerta Clínica:** Menú con índice glucémico controlado.")
if "Hipertensión" in enfermedades:
    st.warning("⚠️ **Alerta Clínica:** Menú bajo en sodio.")

# --- PLAN DE ACTIVIDAD FÍSICA ---
st.markdown("---")
st.header("🏃 Rutina de Ejercicio")
rutina = ""
if "Sedentario" in actividad or "Ligero" in actividad:
    rutina = "**Activación:** 🚶 Caminata veloz: 30 min (3-4 veces/sem) + 🧘 Estiramientos."
elif "Moderado" in actividad:
    rutina = "**Mantenimiento:** 🏃 Trote/Bici: 45 min (3 veces/sem) + 💪 Fuerza ligera."
else:
    rutina = "**Rendimiento:** 🏋️ Pesas: 60 min (4 veces/sem) + ⚡ Cardio HIIT."
st.info(rutina)

# --- MENÚ SEMANAL ---
st.markdown("---")
st.header(f"🥗 Plan de Alimentación (Ajustado a {int(get)} kcal)")

# Factor de Ajuste
f = get / 2000 

def cant(cantidad, unidad, alimento):
    cantidad_ajustada = cantidad * f
    if unidad == "g" or unidad == "ml":
        return f"{int(cantidad_ajustada)} {unidad} {alimento}"
    return f"{cantidad_ajustada:.1f} {unidad} {alimento}"

menus = {
    "Lunes": {
        "Des": f"{cant(40, 'g', 'Avena cruda')} + {cant(100, 'g', 'Manzana')} + {cant(15, 'g', 'Nueces')}",
        "Com": f"{cant(120, 'g', 'Pechuga asada')} + {cant(1, 'tza', 'Quinoa')} + Verduras",
        "Cen": f"{cant(100, 'g', 'Atún agua')} + Ensalada + {cant(1, 'pza', 'Tostada')}",
        "Macros": {"CH": 220, "PRO": 110, "GR": 65}
    },
    "Martes": {
        "Des": f"{cant(2, 'pzas', 'Tostadas')} + {cant(60, 'g', 'Aguacate')} + {cant(100, 'g', 'Huevo')}",
        "Com": f"{cant(1.5, 'tza', 'Lentejas')} + {cant(1, 'tza', 'Verduras vapor')}",
        "Cen": f"{cant(1, 'tza', 'Crema Calabaza')} + {cant(60, 'g', 'Queso Panela')}",
        "Macros": {"CH": 190, "PRO": 105, "GR": 70}
    },
    "Miércoles": {
        "Des": f"Licuado: {cant(250, 'ml', 'Leche')} + {cant(100, 'g', 'Plátano')} + {cant(15, 'g', 'Cacahuate')}",
        "Com": f"{cant(150, 'g', 'Pescado')} + {cant(100, 'g', 'Arroz integral')}",
        "Cen": f"{cant(3, 'pzas', 'Tacos lechuga')} + {cant(90, 'g', 'Pollo')}",
        "Macros": {"CH": 210, "PRO": 125, "GR": 60}
    },
    "Jueves": {
        "Des": f"{cant(150, 'g', 'Yogurt griego')} + {cant(80, 'g', 'Frutos rojos')}",
        "Com": f"{cant(120, 'g', 'Carne magra')} + Ejotes + {cant(1, 'pza', 'Tortilla')}",
        "Cen": f"{cant(2, 'pzas', 'Nopales')} + {cant(80, 'g', 'Queso Oaxaca')}",
        "Macros": {"CH": 150, "PRO": 130, "GR": 65}
    },
    "Viernes": {
        "Des": f"{cant(2, 'pzas', 'Hotcakes avena')} + {cant(50, 'g', 'Huevo')}",
        "Com": f"{cant(1.5, 'tza', 'Pasta integral')} + {cant(100, 'g', 'Pollo')} + Salsa",
        "Cen": f"Sándwich: {cant(2, 'rebs', 'Pan')} + {cant(60, 'g', 'Pavo')}",
        "Macros": {"CH": 240, "PRO": 115, "GR": 55}
    },
    "Sábado": {
        "Des": f"{cant(100, 'g', 'Huevos mexicana')} + {cant(1, 'pza', 'Tortilla')}",
        "Com": f"{cant(150, 'g', 'Ceviche')} + {cant(2, 'pzas', 'Tostadas')}",
        "Cen": f"Brochetas: {cant(80, 'g', 'Queso panela')} y Tomate",
        "Macros": {"CH": 180, "PRO": 120, "GR": 75}
    },
    "Domingo": {
        "Des": f"{cant(1, 'pza', 'Pan francés')} con canela",
        "Com": f"{cant(1, 'pza', 'Pierna Pollo')} + Ensalada",
        "Cen": f"{cant(1, 'pza', 'Quesadilla')} + Flor calabaza",
        "Macros": {"CH": 200, "PRO": 100, "GR": 80}
    }
}

if "Diabetes Tipo 2" in enfermedades:
    menus["Lunes"]["Des"] = f"{cant(30, 'g', 'Avena')} + Nueces (Sin Manzana)"

data_menu = []
total_macros = {"Carbohidratos": 0, "Proteínas": 0, "Grasas": 0}

for dia, info in menus.items():
    ch = int(info["Macros"]["CH"] * f)
    pro = int(info["Macros"]["PRO"] * f)
    gr = int(info["Macros"]["GR"] * f)
    kcal = (ch * 4) + (pro * 4) + (gr * 9)
    total_macros["Carbohidratos"] += ch
    total_macros["Proteínas"] += pro
    total_macros["Grasas"] += gr

    data_menu.append({
        "Día": dia
