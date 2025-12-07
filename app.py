import streamlit as st
import pandas as pd

# 1. Configuración
st.set_page_config(page_title="NutriApp", layout="wide")
st.title("🍎 Evaluación Nutricional")

# 2. Datos (Barra Lateral)
st.sidebar.header("Datos del Paciente")
genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino"])
edad = st.sidebar.number_input("Edad", 10, 100, 25)
peso = st.sidebar.number_input("Peso (kg)", 30.0, 200.0, 70.0)
talla = st.sidebar.number_input("Talla (cm)", 100, 250, 170)
actividad = st.sidebar.selectbox("Nivel Actividad", 
    ["Sedentario", "Ligero", "Moderado", "Intenso"])

# 3. Cálculos (Backend)
imc = peso / ((talla/100)**2)

# Fórmula TMB simplificada en una línea
if genero == "Masculino": tmb = (10*peso) + (6.25*talla) - (5*edad) + 5
else: tmb = (10*peso) + (6.25*talla) - (5*edad) - 161

# Diccionario simple de factores
factores = {"Sedentario":1.2, "Ligero":1.375, "Moderado":1.55, "Intenso":1.725}
get = tmb * factores[actividad]
agua = peso * 35

# 4. Resultados (Frontend)
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("IMC", f"{imc:.1f}", "Normal" if 18.5<=imc<25 else "Revisar")
c2.metric("Calorías Diarias (GET)", f"{int(get)} kcal", "Meta")
c3.metric("Agua Recomendada", f"{int(agua)} ml", f"{int(agua/250)} vasos")

# 5. Menú Semanal (Estructura compacta Anti-Error)
st.markdown("---")
st.subheader("🥗 Menú Sugerido")

# Creamos el menú por columnas (más difícil de romper al copiar)
df = pd.DataFrame({
    "Día": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
    "Desayuno": [
        "Avena cocida + Manzana", 
        "Huevo revuelto + Tostadas", 
        "Licuado (Leche+Plátano)", 
        "Yogurt Griego + Fruta", 
        "Hotcakes de Avena", 
        "Huevo a la Mexicana", 
        "Pan Francés Integral"
    ],
    "Comida": [
        "Pechuga Pollo + Quinoa", 
        "Lentejas + Arroz", 
        "Pescado Empapelado", 
        "Carne Res + Verduras", 
        "Pasta Integral + Pollo", 
        "Ceviche de Pescado", 
        "Pollo Rostizado + Ensalada"
    ],
    "Cena": [
        "Ensalada de Atún", 
        "Quesadillas (Panela)", 
        "Tacos de Lechuga", 
        "Nopales Asados + Queso", 
        "Sandwich de Pavo", 
        "Brochetas Caprese", 
        "Sopa de Verduras"
    ]
})

st.dataframe(df, use_container_width=True, hide_index=True)

# 6. Glosario y Cierre
with st.expander("📖 Ayuda: ¿Qué significan estos datos?"):
    st.write(f"**IMC:** Tu índice es {imc:.1f}. Lo ideal es entre 18.5 y 24.9.")
    st.write(f"**GET:** Necesitas {int(get)} calorías para mantener tu peso.")

st.success("✅ Aplicación cargada correctamente.")
