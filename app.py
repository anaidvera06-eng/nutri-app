import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="NutriPro Científico", layout="wide")
st.title("🍎 Sistema de Evaluación Nutricional Clínica")
st.markdown("Herramienta de cálculo dietoterapéutico: Estimación de requerimientos, composición corporal y planificación alimentaria.")

# --- 2. DATOS DEL PACIENTE ---
st.sidebar.header("Datos Antropométricos")
genero = st.sidebar.selectbox("Género Biológico", ["Masculino", "Femenino"])
edad = st.sidebar.number_input("Edad (años)", 10, 100, 30)
peso = st.sidebar.number_input("Peso Actual (kg)", 30.0, 200.0, 85.0)
talla = st.sidebar.number_input("Talla (cm)", 100, 250, 170)

st.sidebar.header("Perímetros")
cintura = st.sidebar.number_input("Circunferencia Cintura (cm)", 40.0, 200.0, 95.0)
cadera = st.sidebar.number_input("Circunferencia Cadera (cm)", 40.0, 200.0, 105.0)
muneca = st.sidebar.number_input("Perímetro Muñeca (cm)", 10.0, 30.0, 17.0)

st.sidebar.header("Estilo de Vida")
act_opciones = [
    "Sedentario (Menos de 1 hora de ejercicio/semana)",
    "Ligero (1 a 3 horas de ejercicio/semana)",
    "Moderado (3 a 6 horas de ejercicio/semana)",
    "Intenso (6 a 10 horas de ejercicio/semana)",
    "Muy Intenso (Más de 10 horas/semana o doble sesión)"
]
actividad = st.sidebar.selectbox("Nivel de Actividad Física", act_opciones)
medicamentos = st.sidebar.text_area("Farmacología Actual", "Ninguno")

# --- 3. CÁLCULOS FISIOLÓGICOS ---
talla_m = talla / 100
imc = peso / (talla_m ** 2)

# Peso Ideal (Fórmula de Lorentz modificada)
factor_pi = 23 if genero == "Masculino" else 21.5
peso_ideal = (talla_m ** 2) * factor_pi

# Complexión (Indice R)
r = talla / muneca
complexion = "Mediana"
if genero == "Masculino":
    if r > 10.4: complexion = "Pequeña"
    elif r < 9.6: complexion = "Grande"
else:
    if r > 11: complexion = "Pequeña"
    elif r < 10.1: complexion = "Grande"

# ICC (Distribución Adiposa)
icc = cintura / cadera
riesgo_icc = "Bajo"
limite = 0.90 if genero == "Masculino" else 0.85
if icc >= limite: riesgo_icc = "Elevado (Obesidad Central)"

# TMB (Mifflin-St Jeor)
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

# ESTRATEGIA NUTRICIONAL (META)
meta_kcal = get_mant
objetivo = "MANTENIMIENTO ENERGÉTICO"
if imc > 25:
    objetivo = "DÉFICIT CALÓRICO (Pérdida de Peso)"
    meta_kcal = get_mant - 500
    if meta_kcal < 1200: meta_kcal = 1200
elif imc < 18.5:
    objetivo = "SUPERÁVIT CALÓRICO (Ganancia de Peso)"
    meta_kcal = get_mant + 300

# --- 4. RESULTADOS CLÍNICOS ---
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("IMC (kg/m²)", f"{imc:.1f}", f"Ideal: {peso_ideal:.1f}kg")
c2.metric("Requerimiento Meta", f"{int(meta_kcal)} kcal", objetivo)
c3.metric("Gasto Basal (TMB)", f"{int(tmb)} kcal", "Energía en reposo")

st.info(f"**Perfil Somático:** Complexión {complexion} | ICC: {icc:.2f} ({riesgo_icc}) | Hidratación: {int(peso*35)} ml/día")

# --- 5. PRESCRIPCIÓN DE EJERCICIO ---
st.markdown("---")
st.header("🏃 Recomendación de Actividad Física")

rutina = ""
if "Sedentario" in actividad or "Ligero" in actividad:
    rutina = "**Fase de Adaptación:**\n* 🚶 **Aeróbico:** Caminata a paso veloz (60-70% FCmax) 30 min, 3 veces/semana.\n* 🧘 **Movilidad:** Ejercicios de rango de movimiento articular 10 min diarios.\n* 🎯 **Objetivo:** Adaptación cardiovascular y neuromuscular."
elif "Moderado" in actividad:
    rutina = "**Fase de Desarrollo:**\n* 🏃 **Mixto:** Sesiones de 45 min combinando trote/bici y natación.\n* 💪 **Fuerza-Resistencia:** Circuitos de autocargas (peso corporal) 2 veces/semana.\n* 🎯 **Objetivo:** Mejora de la capacidad oxidativa y tono muscular."
else:
    rutina = "**Fase de Rendimiento:**\n* 🏋️ **Hipertrofia/Fuerza:** Entrenamiento con cargas externas 60 min (4 veces/semana).\n* ⚡ **HIIT:** Intervalos de alta intensidad para potencia aeróbica.\n* 🎯 **Objetivo:** Optimización de composición corporal y potencia."

st.success(rutina)

# --- 6. PLAN ALIMENTARIO DETALLADO ---
st.markdown("---")
st.header(f"🥗 Distribución Dietética ({int(meta_kcal)} kcal)")

f = meta_kcal / 2000

def fila(dia, d, c, n, ch, pro, gr):
    return {
        "Día": dia, "Desayuno": d, "Comida": c, "Cena": n,
        "Total Kcal": int((ch*4 + pro*4 + gr*9)*f),
        "CH (kcal)": int(ch*4*f), "PRO (kcal)": int(pro*4*f), "LIP (kcal)": int(gr*9*f)
    }

lista = []

# LUNES
d = f"{int(40*f)}g Avena"
d += f" + {int(200*f)}ml Leche descremada"
c = f"{int(120*f)}g Pechuga de Pollo"
c += f" + {int(60*f)}g Quinoa cocida"
n = f"Ensalada Atún ({int(100*f)}g)"
n += " + 1 Tostada horneada"
lista.append(fila("Lunes", d, c, n, 220, 110, 60))

# MARTES
d = f"2 Huevos ({int(100*f)}g)"
d += " + 1 rebanada Pan Integral"
c = f"{int(150*f)}g Pescado blanco"
c += f" + {int(100*f)}g Arroz integral"
n = f"{int(200*f)}ml Yogurt Griego"
n += f" + {int(15*f)}g Nueces"
lista.append(fila("Martes", d, c, n, 190, 120, 70))

# MIÉRCOLES
d = f"Licuado: {int(250*f)}ml Leche"
d += " + 1 Plátano mediano"
c = f"{int(120*f)}g Res Magra (Corte fino)"
c += " + Nopales asados"
n = f"Quesadillas: {int(60*f)}g Panela"
n += " + 2 Tortillas maíz"
lista.append(fila("Miércoles", d, c, n, 210, 115, 65))

# JUEVES
d = f"{int(150*f)}g Queso Cottage bajo grasa"
d += " + Fruta de temporada"
c = f"Lentejas ({int(150*f)}g cocidas)"
c += " + Vegetales al vapor"
n = f"Sandwich: {int(60*f)}g Pechuga Pavo"
n += " + 1/4 Aguacate"
lista.append(fila("Jueves", d, c, n, 200, 105, 60))

# VIERNES
d = f"Omelet Espinacas"
d += f" ({int(100*f)}g huevo)"
c = f"Pasta Integral ({int(60*f)}g peso crudo)"
c += f" + {int(100*f)}g Pollo deshebrado"
n = f"Tacos Lechuga con Atún ({int(100*f)}g)"
lista.append(fila("Viernes", d, c, n, 230, 110, 55))

# SÁBADO
d = "Hotcakes Avena (2 pzas)"
d += " + Frutos rojos"
c = f"Ceviche ({int(150*f)}g pescado)"
c += " + 2 Tostadas horneadas"
n = "Molletes: 1/2 Bolillo sin migajón"
n += f" + {int(40*f)}g Queso"
lista.append(fila("Sábado", d, c, n, 210, 100, 75))

# DOMINGO
d = "Pan Francés Integral"
d += f" + {int(100*f)}ml Claras"
c = f"Pollo Rostizado ({int(120*f)}g sin piel)"
c += " + Ensalada fresca"
n = "Sopa de Verduras"
n += f" + {int(80*f)}g Pollo"
lista.append(fila("Domingo", d, c, n, 190, 125, 60))

df = pd.DataFrame(lista)
st.dataframe(df, use_container_width=True, hide_index=True)

# --- 7. GLOSARIO CIENTÍFICO (ACTUALIZADO) ---
st.markdown("---")
with st.expander("📖 Glosario de Términos Clínicos"):
    st.markdown("""
    ### 1. Índice de Masa Corporal (IMC)
    Indicador antropométrico que relaciona la masa corporal con la estatura al cuadrado ($kg/m^2$). Se utiliza para clasificar el estado nutricional (bajo peso, normopeso, sobrepeso, obesidad), aunque no distingue entre masa grasa y muscular.
    
    ### 2. Gasto Energético Total (GET)
    Cantidad diaria de energía que el organismo requiere para sostener sus funciones vitales (Tasa Metabólica Basal), la termogénesis de los alimentos y el gasto por actividad física. Es la base para determinar el superávit o déficit calórico.
    
    ### 3. Índice Cintura-Cadera (ICC)
    Medida antropométrica utilizada para evaluar la distribución del tejido adiposo. Un valor elevado (>0.90 en hombres, >0.85 en mujeres) sugiere acumulación de grasa visceral y un mayor riesgo metabólico y cardiovascular.
    
    ### 4. Complexión Corporal
    Clasificación de la morfología ósea basada en la relación entre la estatura y el perímetro de la muñeca. Permite ajustar el peso ideal de manera personalizada, diferenciando entre estructuras pequeñas, medianas y grandes.
    """)

# --- 8. AVISO LEGAL Y DESCARGA ---
# Botón compatible con Excel en español
csv = df.to_csv(index=False, sep=';').encode('utf-8-sig')

st.download_button(
    label="📥 Descargar Reporte Clínico (Excel)",
    data=csv,
    file_name="reporte_nutricional.csv",
    mime="text/csv"
)

st.warning("⚠️ **AVISO IMPORTANTE:** Esta aplicación es una herramienta de apoyo educativo y cálculo preliminar. Los resultados aquí mostrados **NO sustituyen** el diagnóstico, tratamiento o asesoría de un Licenciado en Nutrición o Médico especialista. Se recomienda acudir a consulta profesional para un plan personalizado.")


