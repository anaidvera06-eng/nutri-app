import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Evaluación Nutricional", layout="wide")

# --- TÍTULO PRINCIPAL ---
st.title("🍎 Sistema de Evaluación Nutricional Integral")
st.markdown("""
Calculadora clínica completa: GET, IMC, ICC, Peso Ideal y Complexión.
**Menús dinámicos:** Las porciones se ajustan automáticamente a tus calorías.
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
    st.metric("Gasto Total (GET)", f"{int(get)} kcal/día", "Meta Calórica")
    
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

# --- MENÚ SEMANAL INTELIGENTE (AJUSTADO AL GET) ---
st.markdown("---")
st.header(f"🥗 Plan de Alimentación (Ajustado a {int(get)} kcal)")

# Factor de Ajuste: Base 2000 kcal. 
# Si el GET es 2000, f=1. Si es 1500, f=0.75 (reduce porciones).
f = get / 2000 

# Función para formatear texto de alimentos con cantidades ajustadas
def cant(cantidad, unidad, alimento):
    cantidad_ajustada = cantidad * f
    # Redondeamos para que se vea bien (ej. 1.2 tzas)
    if cantidad_ajustada < 0.2: return f"{cantidad_ajustada:.2f} {unidad} {alimento}"
    return f"{cantidad_ajustada:.1f} {unidad} {alimento}"

menus = {
    "Lunes": {
        "Des": f"{cant(1, 'tza', 'Avena cocida')} + {cant(0.5, 'pza', 'Manzana')} + {cant(10, 'pzas', 'Nueces')}",
        "Com": f"{cant(120, 'g', 'Pechuga asada')} + {cant(1, 'tza', 'Quinoa')} + Verduras libres",
        "Cen": f"{cant(1, 'lata', 'Atún agua')} + Ensalada + {cant(1, 'pza', 'Tostada horneada')}",
        "Macros": {"CH": 220, "PRO": 110, "GR": 65}
    },
    "Martes": {
        "Des": f"{cant(2, 'pzas', 'Tostadas')} + {cant(0.3, 'pza', 'Aguacate')} + {cant(2, 'pzas', 'Huevos')}",
        "Com": f"{cant(1, 'tza', 'Lentejas')} + {cant(1, 'tza', 'Verduras vapor')}",
        "Cen": f"{cant(1, 'tza', 'Crema Calabaza')} + {cant(50, 'g', 'Queso Panela')}",
        "Macros": {"CH": 190, "PRO": 105, "GR": 70}
    },
    "Miércoles": {
        "Des": f"Licuado: {cant(1, 'tza', 'Leche light')} + {cant(1, 'pza', 'Plátano')} + {cant(1, 'cda', 'Crema cacahuate')}",
        "Com": f"{cant(150, 'g', 'Pescado empapelado')} + {cant(0.5, 'tza', 'Arroz integral')}",
        "Cen": f"{cant(3, 'pzas', 'Tacos lechuga')} con {cant(90, 'g', 'Pollo')}",
        "Macros": {"CH": 210, "PRO": 125, "GR": 60}
    },
    "Jueves": {
        "Des": f"{cant(1, 'tza', 'Yogurt griego')} + {cant(0.5, 'tza', 'Frutos rojos')}",
        "Com": f"{cant(120, 'g', 'Carne magra')} + Ejotes + {cant(1, 'pza', 'Tortilla')}",
        "Cen": f"{cant(2, 'pzas', 'Nopales asados')} + {cant(60, 'g', 'Queso Oaxaca')}",
        "Macros": {"CH": 150, "PRO": 130, "GR": 65}
    },
    "Viernes": {
        "Des": f"{cant(2, 'pzas', 'Hotcakes avena')} + {cant(1, 'pza', 'Huevo')}",
        "Com": f"{cant(1, 'tza', 'Pasta integral')} + {cant(100, 'g', 'Pollo')} + Salsa",
        "Cen": f"Sándwich: {cant(2, 'rebs', 'Pan integral')} + {cant(3, 'rebs', 'Pavo')}",
        "Macros": {"CH": 240, "PRO": 115, "GR": 55}
    },
    "Sábado": {
        "Des": f"{cant(2, 'pzas', 'Huevos mexicana')} + {cant(1, 'pza', 'Tortilla maíz')}",
        "Com": f"{cant(150, 'g', 'Ceviche pescado')} + {cant(2, 'pzas', 'Tostadas')}",
        "Cen": f"Brochetas: Queso panela y Tomate cherry (Libre)",
        "Macros": {"CH": 180, "PRO": 120, "GR": 75}
    },
    "Domingo": {
        "Des": f"{cant(1, 'pza', 'Pan francés integral')} con canela",
        "Com": f"{cant(1, 'pza', 'Pierna Pollo')} sin piel + Ensalada",
        "Cen": f"{cant(1, 'pza', 'Quesadilla maíz')} + Flor calabaza",
        "Macros": {"CH": 200, "PRO": 100, "GR": 80}
    }
}

# Ajustes Patológicos
if "Diabetes Tipo 2" in enfermedades:
    menus["Lunes"]["Des"] = f"{cant(0.5, 'tza', 'Avena')} + Nueces (Sin Manzana)"

# Generar Tabla
data_menu = []
for dia, info in menus.items():
    # Ajustar Macros proporcionalmente al GET
    ch_ajustado = int(info["Macros"]["CH"] * f)
    pro_ajustado = int(info["Macros"]["PRO"] * f)
    gr_ajustado = int(info["Macros"]["GR"] * f)
    
    # Calcular Kcal Totales del día (4 kcal por g de CH/PRO, 9 kcal por g de GR)
    kcal_dia = (ch_ajustado * 4) + (pro_ajustado * 4) + (gr_ajustado * 9)

    data_menu.append({
        "Día": dia,
        "Desayuno": info["Des"],
        "Colación 1": cant(1, "pza", "Fruta"),
        "Comida": info["Com"],
        "Colación 2": cant(1, "pza", "Gelatina Light"),
        "Cena": info["Cen"],
        "Carbos (g)": ch_ajustado,
        "Proteína (g)": pro_ajustado,
        "Grasas (g)": gr_ajustado,
        "Kcal Totales": kcal_dia 
    })

df = pd.DataFrame(data_menu)
st.dataframe(df, use_container_width=True, hide_index=True)

st.success(f"✅ Menú calculado para cubrir aproximadamente **{int(get)} kcal** diarias.")
st.caption("Nota: Las porciones se han ajustado automáticamente según tu requerimiento energético (GET).")

# Botón Descarga
st.download_button("📥 Descargar Plan (CSV)", df.to_csv(index=False).encode('utf-8'), "dieta_personalizada.csv", "text/csv")
