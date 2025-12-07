import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="NutriPro Excel", layout="wide")
st.title("🍎 Sistema Nutricional Integral")
st.markdown("Calculadora clínica completa: Meta de Peso, Menús Exactos, Ejercicio y Guía Educativa.")

# --- 2. DATOS DEL PACIENTE ---
st.sidebar.header("Datos Personales")
genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino"])
edad = st.sidebar.number_input("Edad", 10, 100, 30)
peso = st.sidebar.number_input("Peso (kg)", 30.0, 200.0, 85.0)
talla = st.sidebar.number_input("Talla (cm)", 100, 250, 170)

st.sidebar.header("Medidas Antropométricas")
cintura = st.sidebar.number_input("Cintura (cm)", 40.0, 200.0, 95.0)
cadera = st.sidebar.number_input("Cadera (cm)", 40.0, 200.0, 105.0)
muneca = st.sidebar.number_input("Muñeca (cm)", 10.0, 30.0, 17.0)

st.sidebar.header("Estilo de Vida")
act_opciones = [
    "Sedentario (Poco o nada de ejercicio)",
    "Ligero (1-3 días por semana)",
    "Moderado (3-5 días por semana)",
    "Intenso (6-7 días por semana)",
    "Muy Intenso (Doble sesión/Atleta)"
]
actividad = st.sidebar.selectbox("Nivel Actividad", act_opciones)
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
if icc >= limite: riesgo_icc = "Alto (Obesidad Central)"

# TMB y GET
if genero == "Masculino":
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) + 5
else:
    tmb = (10 * peso) + (6.25 * talla) - (5 * edad) - 161

fa = 1.2
if "Ligero" in actividad: fa = 1.375
if "Moderado" in actividad: fa = 1.55
if "Intenso" in actividad: fa = 1.725
if "Muy Intenso" in actividad: fa = 1.9
get_mant = tmb * fa

# META CALÓRICA
meta_kcal = get_mant
objetivo = "MANTENER PESO"
if imc > 25:
    objetivo = "BAJAR PESO (Déficit -500)"
    meta_kcal = get_mant - 500
    if meta_kcal < 1200: meta_kcal = 1200
elif imc < 18.5:
    objetivo = "SUBIR PESO (Superávit +300)"
    meta_kcal = get_mant + 300

# --- 4. RESULTADOS ---
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("IMC Actual", f"{imc:.1f}", f"Ideal: {peso_ideal:.1f}kg")
c2.metric("META DIARIA", f"{int(meta_kcal)} kcal", objetivo)
c3.metric("Gasto Actual", f"{int(get_mant)} kcal", "Mantenimiento")

st.info(f"**Análisis:** Complexión {complexion} | ICC {icc:.2f} ({riesgo_icc}) | Agua: {int(peso*35)} ml/día")

# --- 5. EJERCICIO ---
st.markdown("---")
st.header("🏃 Plan de Actividad Física")

rutina = ""
if "Sedentario" in actividad or "Ligero" in actividad:
    rutina = "**Fase de Activación:**\n* 🚶 **Cardio:** Caminata rápida 30 min (3 veces/semana).\n* 🧘 **Flexibilidad:** Estiramientos 10 min diarios.\n* 🎯 **Meta:** Lograr 5,000 pasos al día."
elif "Moderado" in actividad:
    rutina = "**Fase de Mantenimiento:**\n* 🏃 **Cardio:** Trote, Natación o Bici 45 min (3 veces/semana).\n* 💪 **Fuerza:** Ejercicios con peso corporal (2 veces/semana).\n* 🎯 **Meta:** Mantener frecuencia cardíaca en zona quema-grasa."
else:
    rutina = "**Fase de Rendimiento:**\n* 🏋️ **Fuerza:** Pesas/Gimnasio 60 min (4 veces/semana).\n* ⚡ **HIIT:** Intervalos alta intensidad 20 min (2 veces/semana).\n* 🎯 **Meta:** Aumentar masa muscular y resistencia."

st.success(rutina)

# --- 6. MENÚ DETALLADO ---
st.markdown("---")
st.header(f"🥗 Menú Detallado ({int(meta_kcal)} kcal)")

f = meta_kcal / 2000

def fila(dia, d, c, n, ch, pro, gr):
    return {
        "Día": dia, "Desayuno": d, "Comida": c, "Cena": n,
        "Total Kcal": int((ch*4 + pro*4 + gr*9)*f),
        "CH (kcal)": int(ch*4*f), "PRO (kcal)": int(pro*4*f), "GR (kcal)": int(gr*9*f)
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

# --- 7. GLOSARIO ---
st.markdown("---")
with st.expander("📖 Glosario: ¿Qué significan estos datos?"):
    st.markdown("""
    ### 1. IMC (Índice de Masa Corporal)
    Relación peso/estatura. Indica si tienes bajo peso, normal o sobrepeso.
    
    ### 2. GET (Gasto Energético Total)
    Calorías que gastas al día.
    * **Meta:** Son las calorías ajustadas (restando 500 para bajar de peso o sumando para subir).
    
    ### 3. ICC (Índice Cintura-Cadera)
    Mide distribución de grasa. Si es alto, hay riesgo cardiovascular.
    
    ### 4. Complexión
    Tamaño de tu estructura ósea (muñeca).
    """)

# BOTÓN DE DESCARGA ARREGLADO PARA EXCEL ESPAÑOL
# Usamos sep=';' para que Excel separe bien las columnas
csv = df.to_csv(index=False, sep=';').encode('utf-8-sig')

st.download_button(
    label="📥 Descargar Plan (Compatible Excel)",
    data=csv,
    file_name="plan_nutricional.csv",
    mime="text/csv"
)
