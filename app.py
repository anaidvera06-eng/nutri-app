import streamlit as st
import pandas as pd

# 1. Configuración inicial (Siempre va primero)
st.set_page_config(page_title="NutriApp", layout="wide")
st.title("🍎 Evaluación Nutricional")
st.markdown("Calculadora de GET, IMC, Hidratación y Menú.")

# 2. Barra Lateral (Inputs)
st.sidebar.header("Datos del Paciente")
nombre = st.sidebar.text_input("Nombre", "Paciente")
genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino"])
edad = st.sidebar.number_input("Edad", 10, 100, 25)
peso = st.sidebar.number_input("Peso (kg)", 30.0, 200.0, 70.0)
talla = st.sidebar.number_input("Talla (cm)", 100, 250, 170)

st.sidebar.header("Medidas")
cintura = st.sidebar.number_input("Cintura (cm)", 50.0, 150.0, 80.0)
cadera = st.sidebar.number_input("Cadera (cm)", 50.0, 150.0, 95.0)
muneca = st.sidebar.number_input("Muñeca (cm)", 10.0, 25.0, 16.0)

st.sidebar.header("Actividad Física")
# Usamos claves simples para evitar errores de texto
opcion_actividad = st.sidebar.selectbox("Nivel", 
    ["Sedentario (1.2)", "Ligero (1.375)", "Moderado (1.55)", "Intenso (1.725)", "Muy Intenso (1.9)"])

# 3. Cálculos Matemáticos (Backend)
# Extraemos el valor numérico de la actividad
if "Sedentario" in opcion_actividad: factor = 1.2
elif "Ligero" in opcion_actividad: factor = 1.375
elif "Moderado" in opcion_actividad: factor = 1.55
elif "Intenso" in opcion_actividad: factor = 1.725
else: factor = 1.9

# Fórmulas
talla_m = talla / 100
imc = peso / (talla_m * talla_m)
agua_litros = (peso * 35) / 1000

# TMB (Mifflin-St Jeor)
if genero == "Masculino":
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) + 5
else:
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) - 161

get = tmb * factor

# Diagnósticos simples
diag_imc = "Normal"
if imc < 18.5: diag_imc = "Bajo Peso"
elif imc >= 25: diag_imc = "Sobrepeso/Obesidad"

# 4. Mostrar Resultados (Frontend)
st.markdown("---") # Línea separadora
st.subheader("📊 Resultados del Paciente")

col1, col2, col3 = st.columns(3)
col1.metric("IMC Actual", f"{imc:.1f}", diag_imc)
col2.metric("Calorías Diarias (GET)", f"{int(get)} kcal", "Meta")
col3.metric("Agua Recomendada", f"{agua_litros:.1f} Litros", f"{int(agua_litros*4)} vasos")

# 5. Generador de Menú (Simplificado para evitar errores)
st.markdown("---")
st.subheader("🥗 Ejemplo de Menú Calculado")

# Ajuste de porciones según calorías
ajuste = get / 2000

# Creamos el menú directo sin diccionarios complejos
datos_menu = [
    {"Día": "Lunes", "Desayuno": f"{int(40*ajuste)}g Avena + Manzana", "Comida": f"{int(120*ajuste)}g Pollo + Quinoa", "Cena": "Ensalada Atún"},
    {"Día": "Martes", "Desayuno": "Tostadas con Huevo", "Comida": f"{int(1.5*ajuste)} tzas Lentejas", "Cena": "Crema Calabaza"},
    {"Día": "Miércoles", "Desayuno": "Licuado Plátano", "Comida": f"{int(150*ajuste)}g Pescado + Arroz", "Cena": "Tacos Lechuga"},
    {"Día": "Jueves", "Desayuno": "Yogurt con Fruta", "Comida": f"{int(120*ajuste)}g Res + Verduras", "Cena": "Nopales Asados"},
    {"Día": "Viernes", "Desayuno": "Hotcakes Avena", "Comida": "Pasta con Pollo", "Cena": "Sandwich Pavo"},
    {"Día": "Sábado", "Desayuno": "Huevo Mexicana", "Comida": "Ceviche Pescado", "Cena": "Brochetas Queso"},
    {"Día":1}

