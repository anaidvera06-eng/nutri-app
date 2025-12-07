import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="NutriGenius Pro", layout="wide")

# --- TÍTULO ---
st.title("🍎 Sistema de Evaluación Nutricional Integral")
st.markdown("""
Calculadora clínica de GET, IMC, ICC, Peso Ideal y Complexión Corporal.
Genera planes de alimentación y ejercicio personalizados.
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
# Mujeres: Talla^2 * 21.5 | Hombres: Talla^2 * 23
factor_peso_ideal = 23 if genero == "Masculino" else 21.5
peso_ideal = (talla_m ** 2) * factor_peso_ideal

# 3. ICC (Índice Cintura-Cadera)
icc = cintura / cadera
riesgo_icc = "Bajo"
# Puntos de corte estándar (OMS): Hombres >= 0.90, Mujeres >= 0.85
if genero == "Masculino":
    if icc >= 0.90: riesgo_icc = "Obesidad Central (Riesgo Alto)"
else:
    if icc >= 0.85: riesgo_icc = "Obesidad Central (Riesgo Alto)"

# 4. Complexión Corporal (r = talla / muñeca)
r = talla / muneca
complexion = "Mediana" # Valor default

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
    
    # Peso Ideal y Complexión
    col_a, col_b = st.columns(2)
    col_a.metric("Peso Ideal Sugerido", f"{peso_ideal:.1f} kg")
    col_b.metric("Complexión Corporal", complexion, f"r={r:.1f}")
    
    # ICC
    st.metric("Índice Cintura-Cadera (ICC)", f"{icc:.2f}", riesgo_icc)

with col_der:
    st.subheader("⚡ Requerimiento Energético")
    st.metric("Metabolismo Basal (TMB)", f"{int(tmb)} kcal")
    st.metric("Gasto Total (GET)", f"{int(get)} kcal/día", "Mantenimiento")
    
    st.info(f"💡 **Estrategia:** Para llegar a tu peso ideal de **{peso_ideal:.1f} kg**, se sugiere ajustar calorías y actividad.")
    
    if "Diabetes Tipo 2" in enfermedades:
        st.warning("⚠️ Plan ajustado para control glucémico.")
    if "Hipertensión" in enfermedades:
        st.warning("⚠️ Plan bajo en sodio.")

# --- PLAN DE ACTIVIDAD FÍSICA ---
st.markdown("---")
st.header("🏃 Rutina de Ejercicio Personalizada")

rutina = ""
if "Sedentario" in actividad or "Ligero" in actividad:
    rutina = "**Fase de Activación:**\n* 🚶 Caminata a paso veloz: 30 min (3-4 veces/sem)\n* 🧘 Estiramientos: 10 min diarios."
elif "Moderado" in actividad:
    rutina = "**Fase de Mantenimiento:**\n* 🏃 Trote/Bici: 45 min (3 veces/sem)\n* 💪 Fuerza (peso corporal): 20 min (2 veces/sem)."
else:
    rutina = "**Fase Deportiva:**\n* 🏋️ Pesas/Gimnasio: 60 min (4 veces/sem)\n* ⚡ HIIT/Cardio Intenso: 20 min (2 veces/sem)."

st.info(rutina)

# --- MENÚ SEMANAL ---
st.markdown("---")
st.header("🥗 Plan de Alimentación Semanal")

# Base de menús
menus = {
    "Lunes": {"Des": "Avena cocida con manzana", "Com": "Pechuga asada + Quinoa", "Cen": "Ensalada de Atún"},
    "Martes": {"Des": "Tostadas con aguacate y huevo", "Com": "Lentejas con verduras", "Cen": "Crema de Calabaza"},
    "Miércoles": {"Des": "Licuado de fresa y nuez", "Com": "Pescado empapelado + Arroz", "Cen": "Tacos de lechuga con pollo"},
    "Jueves": {"Des": "Yogurt griego con fruta", "Com": "Carne molida con ejotes", "Cen": "Nopales asados con queso"},
    "Viernes": {"Des": "Hotcakes de avena", "Com": "Pasta integral con pollo", "Cen": "Sándwich de pavo"},
    "Sábado": {"Des": "Huevos a la mexicana", "Com": "Ceviche de pescado", "Cen": "Brochetas de queso y tomate"},
    "Domingo": {"Des": "Pan francés integral", "Com": "Pollo rostizado (sin piel)", "Cen": "Quesadillas (tortilla maíz)"}
}

# Ajustes patológicos simples
if "Diabetes Tipo 2" in enfermedades:
    menus["Lunes"]["Des"] = "Avena (reducida) + Claras"
    menus["Viernes"]["Des"] = "Omelet de espinaca"
if "Hipertensión" in enfermedades:
    menus["Lunes"]["Cen"] = "Ensalada (sin sal añadida)"

# Generar Tabla
data_menu = []
for dia, comidas in menus.items():
    data_menu.append({
        "Día": dia,
        "Desayuno": comidas["Des"],
        "Colación 1": "Fruta o Semillas",
        "Comida": comidas["Com"],
        "Colación 2": "Gelatina light o Yogurt",
        "Cena": comidas["Cen"]
    })

df = pd.DataFrame(data_menu)
st.dataframe(df, use_container_width=True, hide_index=True)

# Botón Descarga
st.download_button("📥 Descargar Plan (CSV)", df.to_csv(index=False).encode('utf-8'), "dieta.csv", "text/csv")

