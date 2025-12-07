import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Evaluación Nutricional", layout="wide")

# --- TÍTULO PRINCIPAL ---
st.title("🍎 Sistema de Evaluación Nutricional Integral")
st.markdown("""
Calculadora clínica completa: GET, IMC, ICC, Peso Ideal y Complexión.
Genera planes de alimentación con conteo de macronutrientes y porciones.
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

# 2. Peso Ideal (Fórmula solicitada)
factor_peso_ideal = 23 if genero == "Masculino" else 21.5
peso_ideal = (talla_m ** 2) * factor_peso_ideal

# 3. ICC (Índice Cintura-Cadera)
icc = cintura / cadera
riesgo_icc = "Bajo"
if genero == "Masculino":
    if icc >= 0.90: riesgo_icc = "Obesidad Central (Riesgo Alto)"
else:
    if icc >= 0.85: riesgo_icc = "Obesidad Central (Riesgo Alto)"

# 4. Complexión Corporal (r = talla / muñeca)
r = talla / muneca
complexion = "Mediana" 

if genero == "Masculino":
    if r > 10.4: complexion = "Pequeña"
    elif 9.6 <= r <= 10.4: complexion = "Mediana"
    else: complexion = "Grande"
else: # Femenino
    if r > 11: complexion = "Pequeña"
    elif 10.1 <= r <= 11: complexion = "Mediana"
    else: complexion = "Grande"

# 5. TMB y GET (Mifflin-St Jeor)
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

# --- MOSTRAR RESULTADOS ---
st.markdown("---")
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("📊 Diagnóstico Antropométrico")
    
    # IMC
    estado_imc = "Normal"
    if imc < 18.5: estado_imc = "Bajo Peso"
    elif imc >= 25 and imc < 30: estado_imc = "Sobrepeso"
    elif imc >= 30: estado_imc = "Obesidad"
    st.metric("IMC Actual", f"{imc:.1f}", estado_imc)
    
    col_a, col_b = st.columns(2)
    col_a.metric("Peso Ideal", f"{peso_ideal:.1f} kg")
    col_b.metric("Complexión", complexion, f"r={r:.1f}")
    
    st.metric("ICC (Cintura-Cadera)", f"{icc:.2f}", riesgo_icc)

with col_der:
    st.subheader("⚡ Requerimiento Energético")
    st.metric("Metabolismo Basal (TMB)", f"{int(tmb)} kcal")
    st.metric("Gasto Total (GET)", f"{int(get)} kcal/día", "Mantenimiento")
    
    if "Diabetes Tipo 2" in enfermedades:
        st.warning("⚠️ Menú ajustado: bajo en azúcares simples.")
    if "Hipertensión" in enfermedades:
        st.warning("⚠️ Menú ajustado: bajo en sodio.")

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

# --- MENÚ SEMANAL CON MACROS ---
st.markdown("---")
st.header("🥗 Plan de Alimentación (Con Porciones y Macros)")

# Estructura de datos más compleja para incluir macros
# CH = Carbohidratos (g), PRO = Proteínas (g), GR = Grasas (g)
menus = {
    "Lunes": {
        "Des": "1 tza Avena cocida + 1/2 Manzana + 10 Nueces",
        "Com": "120g Pechuga asada + 1 tza Quinoa + Verduras",
        "Cen": "1 lata Atún en agua + Ensalada mixta + 1 Tostada",
        "Macros": {"CH": 220, "PRO": 110, "GR": 65}
    },
    "Martes": {
        "Des": "2 Tostadas integrales + 1/3 Aguacate + 2 Huevos",
        "Com": "1 tza Lentejas + 1 tza Verduras al vapor",
        "Cen": "1 tza Crema de Calabaza + 50g Queso Panela",
        "Macros": {"CH": 190, "PRO": 105, "GR": 70}
    },
    "Miércoles": {
        "Des": "Licuado: 1 tza Leche light + 1 Plátano + 1 cda Crema cacahuate",
        "Com": "150g Pescado empapelado + 1/2 tza Arroz integral",
        "Cen": "3 Tacos de lechuga con 90g Pollo deshebrado",
        "Macros": {"CH": 210, "PRO": 125, "GR": 60}
    },
    "Jueves": {
        "Des": "1 tza Yogurt griego sin azúcar + 1/2 tza Frutos rojos",
        "Com": "120g Carne molida (res magra) + Ejotes + 1 Tortilla",
        "Cen": "2 Nopales asados + 60g Queso Oaxaca + Salsa",
        "Macros": {"CH": 150, "PRO": 130, "GR": 65}
    },
    "Viernes": {
        "Des": "2 Hotcakes de avena y plátano + 1 huevo",
        "Com": "1 tza Pasta integral + 100g Pollo + Salsa tomate",
        "Cen": "Sándwich: 2 rebanadas pan integral + 3 rebanadas Pavo",
        "Macros": {"CH": 240, "PRO": 115, "GR": 55}
    },
    "Sábado": {
        "Des": "2 Huevos a la mexicana + 1 Tortilla maíz",
        "Com": "Ceviche de pescado (150g) + 2 Tostadas",
        "Cen": "Brochetas: Queso panela y Tomate cherry",
        "Macros": {"CH": 180, "PRO": 120, "GR": 75}
    },
    "Domingo": {
        "Des": "1 Pan francés integral (con huevo y canela)",
        "Com": "1 Pierna Pollo rostizado (sin piel) + Ensalada rusa",
        "Cen": "1 Quesadilla (tortilla maíz) + Flor de calabaza",
        "Macros": {"CH": 200, "PRO": 100, "GR": 80}
    }
}

# Ajustes simples por enfermedad
if "Diabetes Tipo 2" in enfermedades:
    menus["Lunes"]["Des"] = "1/2 tza Avena + 10 Nueces (Sin Manzana)"
    menus["Miércoles"]["Des"] = "Licuado: Leche de almendra + Fresas (Sin Plátano)"

# Generar Tabla
data_menu = []
for dia, info in menus.items():
    data_menu.append({
        "Día": dia,
        "Desayuno": info["Des"],
        "Colación 1": "1 Fruta (Manzana/Pera)",
        "Comida": info["Com"],
        "Colación 2": "1 Gelatina Light",
        "Cena": info["Cen"],
        "Carbos (g)": info["Macros"]["CH"],
        "Proteína (g)": info["Macros"]["PRO"],
        "Grasas (g)": info["Macros"]["GR"]
    })

df = pd.DataFrame(data_menu)
st.dataframe(df, use_container_width=True, hide_index=True)

st.caption("Nota: Los valores de macronutrientes son estimaciones promedio para fines educativos.")

# Botón Descarga
st.download_button("📥 Descargar Plan (CSV)", df.to_csv(index=False).encode('utf-8'), "dieta_completa.csv", "text/csv")
