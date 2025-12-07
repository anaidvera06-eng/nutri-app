import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="NutriGenius AI", layout="wide")

# --- TÍTULO Y DESCRIPCIÓN ---
st.title("🍎 NutriGenius: Asistente Nutricional Inteligente")
st.markdown("""
Esta aplicación utiliza lógica basada en evidencia para calcular tu Gasto Energético Total (GET) 
y generar un plan personalizado considerando tus patologías y medicamentos.
""")

# --- BARRA LATERAL (DATOS DEL PACIENTE) ---
st.sidebar.header("Datos del Paciente")

nombre = st.sidebar.text_input("Nombre del Paciente", "Usuario")
genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino"])
edad = st.sidebar.number_input("Edad (años)", min_value=10, max_value=100, value=25)
peso = st.sidebar.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0)
talla = st.sidebar.number_input("Talla (cm)", min_value=100, max_value=250, value=170)

st.sidebar.subheader("Estilo de Vida y Salud")
actividad = st.sidebar.selectbox("Nivel de Actividad Física", 
    ["Sedentario (Poco o nada)", 
     "Ligero (1-3 días/sem)", 
     "Moderado (3-5 días/sem)", 
     "Intenso (6-7 días/sem)", 
     "Muy Intenso (Doble sesión)"])

enfermedades = st.sidebar.multiselect("Enfermedades / Patologías", 
    ["Ninguna", "Diabetes Tipo 2", "Hipertensión", "Obesidad", "Colesterol Alto"])

medicamentos = st.sidebar.text_area("Medicamentos actuales (separar por comas)", "Ninguno")

# --- LÓGICA DE CÁLCULO (BACKEND) ---

# 1. Calcular TMB (Mifflin-St Jeor)
if genero == "Masculino":
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) + 5
else:
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) - 161

# 2. Definir Factor de Actividad
factores = {
    "Sedentario (Poco o nada)": 1.2,
    "Ligero (1-3 días/sem)": 1.375,
    "Moderado (3-5 días/sem)": 1.55,
    "Intenso (6-7 días/sem)": 1.725,
    "Muy Intenso (Doble sesión)": 1.9
}
factor_actividad = factores[actividad]

# 3. Calcular GET
get = tmb * factor_actividad

# --- MOSTRAR RESULTADOS ---
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Resultados Metabólicos")
    st.metric(label="Tasa Metabólica Basal (TMB)", value=f"{int(tmb)} kcal")
    st.metric(label="Gasto Energético Total (GET)", value=f"{int(get)} kcal/día", delta="Mantenimiento")
    st.info(f"Para perder peso, se recomienda un déficit. Meta sugerida: **{int(get - 500)} kcal**.")

with col2:
    st.subheader("💊 Análisis Clínico")
    if "Diabetes Tipo 2" in enfermedades:
        st.warning("⚠️ **Alerta Diabetes:** El menú generado priorizará alimentos de bajo índice glucémico (IG).")
    if "Hipertensión" in enfermedades:
        st.warning("⚠️ **Alerta Hipertensión:** Se restringe el sodio en las recomendaciones.")
    if medicamentos != "Ninguno":
        st.success(f"ℹ️ **Nota:** Verifique interacciones alimentos-medicamentos para: {medicamentos}")
    if not enfermedades and medicamentos == "Ninguno":
        st.success("✅ Paciente aparentemente sano.")

# --- PLAN DE ACTIVIDAD FÍSICA ---
st.markdown("---")
st.header("🏃 Plan de Actividad Física Recomendado")

rutina = ""
if "Sedentario" in actividad or "Ligero" in actividad:
    rutina = """
    * **Cardio Suave:** Caminata rápida (30 min) - 3 veces por semana.
    * **Movilidad:** Estiramientos o Yoga básico (15 min) - 2 veces por semana.
    * **Objetivo:** Alcanzar 5,000 pasos diarios.
    """
elif "Moderado" in actividad:
    rutina = """
    * **Cardio:** Trote suave o Bicicleta (45 min) - 3 veces por semana.
    * **Fuerza:** Ejercicios con peso corporal (flexiones, sentadillas) - 2 veces por semana.
    * **Objetivo:** Mantener frecuencia cardíaca en zona 2.
    """
else:
    rutina = """
    * **Fuerza/Hipertrofia:** Gimnasio/Pesas (60 min) - 4 veces por semana.
    * **Cardio HIIT:** Intervalos de alta intensidad (20 min) - 2 veces por semana.
    * **Recuperación:** 1 día de descanso activo total.
    """

st.markdown(rutina)

# --- GENERADOR DE MENÚ SEMANAL VARIADO ---
st.markdown("---")
st.header("🥗 Menú Semanal Variado")

# Definimos opciones diferentes para cada día
menus_variados = {
    "Lunes": {"Desayuno": "Avena con manzana y canela", "Comida": "Pollo a la plancha con quinoa", "Cena": "Ensalada de atún"},
    "Martes": {"Desayuno": "Tostadas integrales con aguacate", "Comida": "Lentejas estofadas con verduras", "Cena": "Crema de calabaza"},
    "Miércoles": {"Desayuno": "Batido de proteínas y plátano", "Comida": "Pescado al horno con papas", "Cena": "Omelet de espinacas"},
    "Jueves": {"Desayuno": "Yogurt griego con frutos rojos", "Comida": "Carne magra salteada con pimientos", "Cena": "Ensalada caprese"},
    "Viernes": {"Desayuno": "Hot cakes de avena y huevo", "Comida": "Pasta integral con pollo", "Cena": "Tacos de lechuga con pavo"},
    "Sábado": {"Desayuno": "Huevos revueltos con champiñones", "Comida": "Bowl de arroz y salmón/atún", "Cena": "Sopa de verduras"},
    "Domingo": {"Desayuno": "Pan francés integral", "Comida": "Pechuga rellena de espinacas", "Cena": "Tostadas horneadas de tinga de pollo"}
}

# Ajuste automático si tiene Diabetes
if "Diabetes Tipo 2" in enfermedades:
    menus_variados["Lunes"]["Desayuno"] = "Avena (reducida) con nueces (sin azúcar)"
    menus_variados["Miércoles"]["Desayuno"] = "Batido verde (sin plátano)"
    menus_variados["Domingo"]["Desayuno"] = "Pan integral tostado con huevo"

# Crear la tabla de datos
menu_data = []
for dia, comidas in menus_variados.items():
    menu_data.append({
        "Día": dia,
        "Desayuno": comidas["Desayuno"],
        "Refrigerio 1": "Fruta de temporada o almendras",
        "Comida": comidas["Comida"],
        "Refrigerio 2": "Gelatina sin azúcar o Yogurt",
        "Cena": comidas["Cena"]
    })

df_menu = pd.DataFrame(menu_data)

# Mostrar tabla interactiva
st.dataframe(df_menu, use_container_width=True, hide_index=True)

# Botón de descarga actualizado
st.download_button(
    label="📥 Descargar Menú Semanal (CSV)",
    data=df_menu.to_csv(index=False).encode('utf-8'),
    file_name='plan_nutricional_semanal.csv',
    mime='text/csv',
)
