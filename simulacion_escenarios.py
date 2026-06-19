"""
Simulación del Diagrama de Forrester - Modelo de Inventario de Supermercado
Escenarios más contrastantes para análisis de dinámica de sistemas.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

# ─────────────────────────────────────────────────────────
# Parámetros de simulación
# ─────────────────────────────────────────────────────────
INITIAL_TIME = 0
FINAL_TIME = 90
TIME_STEP = 0.25

# ─────────────────────────────────────────────────────────
# Función de simulación (réplica del modelo Vensim)
# ─────────────────────────────────────────────────────────
def simular(params):
    cap_max_trastienda = params.get("Capacidad Max trastienda", 800)
    nivel_obj_gondola = params.get("Nivel Objetivo Gondola", 200)
    nivel_obj_trastienda = params.get("Nivel Objetivo Trastienda", 500)
    tasa_ventas_concretadas = params.get("Tasa de Ventas Concretadas", 15)
    tasa_gen_mermas = params.get("Tasa de generacion de mermas", 0.005)
    tasa_descarte = params.get("Tasa de descarte de mermados", 0.5)
    tiempo_proveedor = params.get("Tiempo de retraso del proveedor", 2)
    tiempo_ajuste = params.get("Tiempo de ajuste de reposicion", 1)
    
    inv_trastienda = params.get("Inventario inicial trastienda", 400)
    stock_gondola = params.get("Stock inicial gondola", 150)
    prod_mermados = params.get("Productos mermados inicial", 0)
    
    n_steps = int((FINAL_TIME - INITIAL_TIME) / TIME_STEP) + 1
    time = np.linspace(INITIAL_TIME, FINAL_TIME, n_steps)
    
    hist = {
        "time": time,
        "Inventario en Trastienda": np.zeros(n_steps),
        "Stock en Gondola": np.zeros(n_steps),
        "Productos Mermados": np.zeros(n_steps),
        "Descarga del camion": np.zeros(n_steps),
        "Translado a gondola": np.zeros(n_steps),
        "Ventas": np.zeros(n_steps),
        "Ventas deseadas": np.zeros(n_steps),
        "Generacion de mermados": np.zeros(n_steps),
        "Descarte de Basura": np.zeros(n_steps),
    }
    
    faltante_stock_init = max(0, nivel_obj_gondola - stock_gondola)
    smooth_value = faltante_stock_init
    
    for i in range(n_steps):
        hist["Inventario en Trastienda"][i] = inv_trastienda
        hist["Stock en Gondola"][i] = stock_gondola
        hist["Productos Mermados"][i] = prod_mermados
        
        faltante_stock = max(0, nivel_obj_gondola - stock_gondola)
        faltante_trastienda = max(0, nivel_obj_trastienda - inv_trastienda)
        
        smooth_value += (faltante_stock - smooth_value) / 0.5 * TIME_STEP
        
        tasa_llegada_camion = faltante_trastienda / tiempo_proveedor
        
        if inv_trastienda > 0:
            tasa_reposicion = smooth_value / tiempo_ajuste
        else:
            tasa_reposicion = 0
        
        if inv_trastienda < cap_max_trastienda:
            descarga = tasa_llegada_camion
        else:
            descarga = 0
        
        translado = min(inv_trastienda / TIME_STEP, tasa_reposicion)
        ventas = min(tasa_ventas_concretadas, stock_gondola / TIME_STEP)
        gen_mermados = stock_gondola * tasa_gen_mermas
        descarte = prod_mermados * tasa_descarte
        
        hist["Descarga del camion"][i] = descarga
        hist["Translado a gondola"][i] = translado
        hist["Ventas"][i] = ventas
        hist["Ventas deseadas"][i] = tasa_ventas_concretadas
        hist["Generacion de mermados"][i] = gen_mermados
        hist["Descarte de Basura"][i] = descarte
        
        if i < n_steps - 1:
            inv_trastienda += (descarga - translado) * TIME_STEP
            stock_gondola += (translado - gen_mermados - ventas) * TIME_STEP
            prod_mermados += (gen_mermados - descarte) * TIME_STEP
            inv_trastienda = max(0, inv_trastienda)
            stock_gondola = max(0, stock_gondola)
            prod_mermados = max(0, prod_mermados)
    
    return hist

# ─────────────────────────────────────────────────────────
# 3 Escenarios con diferencias más marcadas
# ─────────────────────────────────────────────────────────
escenarios = {
    "Esc. 1: Base (parámetros actuales)": {},
    "Esc. 2: Crisis de demanda\n(Ventas=50, Mermas=3%)": {
        "Tasa de Ventas Concretadas": 50,
        "Tasa de generacion de mermas": 0.03,
    },
    "Esc. 3: Crisis de suministro\n(Proveedor=10 días, Cap.trastienda=300)": {
        "Tiempo de retraso del proveedor": 10,
        "Capacidad Max trastienda": 300,
    },
}

colores = ["#3498db", "#e74c3c", "#2ecc71"]
nombres_cortos = ["Base", "Crisis demanda", "Crisis suministro"]

# Ejecutar
resultados = {}
for nombre, params in escenarios.items():
    resultados[nombre] = simular(params)
    print(f"✅ {nombre.split(chr(10))[0]} simulado")

output_dir = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────
# Estilo global
# ─────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'figure.facecolor': '#1a1a2e',
    'axes.facecolor': '#16213e',
    'axes.edgecolor': '#444',
    'axes.labelcolor': '#e0e0e0',
    'text.color': '#e0e0e0',
    'xtick.color': '#e0e0e0',
    'ytick.color': '#e0e0e0',
    'grid.color': '#2a2a4a',
    'grid.alpha': 0.5,
    'legend.facecolor': '#16213e',
    'legend.edgecolor': '#444',
})

nombres = list(escenarios.keys())

# ══════════════════════════════════════════════════════════
# GRÁFICA 1: NIVELES (Stocks)
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(3, 1, figsize=(14, 13), sharex=True)
fig.suptitle("COMPARACIÓN DE ESCENARIOS — NIVELES (Stocks)", fontsize=16, fontweight='bold', y=0.98)

# Inventario en Trastienda
ax = axes[0]
for idx, nombre in enumerate(nombres):
    h = resultados[nombre]
    ax.plot(h["time"], h["Inventario en Trastienda"], color=colores[idx], linewidth=2.5, 
           label=nombres_cortos[idx], alpha=0.9)
ax.axhline(y=500, color='#f39c12', linestyle='--', alpha=0.7, linewidth=1.5, label='Objetivo (500)')
ax.axhspan(0, 100, alpha=0.12, color='red')
ax.set_ylabel("Cajas")
ax.set_title("▭ Inventario en Trastienda", pad=8)
ax.legend(loc='right', fontsize=9)
ax.grid(True, alpha=0.3)

# Stock en Gondola
ax = axes[1]
for idx, nombre in enumerate(nombres):
    h = resultados[nombre]
    ax.plot(h["time"], h["Stock en Gondola"], color=colores[idx], linewidth=2.5,
           label=nombres_cortos[idx], alpha=0.9)
ax.axhline(y=200, color='#f39c12', linestyle='--', alpha=0.7, linewidth=1.5, label='Objetivo (200)')
ax.axhspan(0, 30, alpha=0.15, color='red', label='Zona crítica (<30)')
ax.set_ylabel("Cajas")
ax.set_title("▭ Stock en Góndola — ¿Se vacía?", pad=8)
ax.legend(loc='right', fontsize=9)
ax.grid(True, alpha=0.3)

# Productos Mermados
ax = axes[2]
for idx, nombre in enumerate(nombres):
    h = resultados[nombre]
    ax.plot(h["time"], h["Productos Mermados"], color=colores[idx], linewidth=2.5,
           label=nombres_cortos[idx], alpha=0.9)
ax.set_ylabel("Cajas")
ax.set_xlabel("Tiempo (días)", fontsize=12)
ax.set_title("▭ Productos Mermados — Acumulación de pérdidas", pad=8)
ax.legend(loc='right', fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.96])
path1 = os.path.join(output_dir, "esc_niveles.png")
plt.savefig(path1, dpi=150, bbox_inches='tight')
plt.close()
print(f"📊 Guardada: {path1}")

# ══════════════════════════════════════════════════════════
# GRÁFICA 2: FLUJOS
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(3, 1, figsize=(14, 13), sharex=True)
fig.suptitle("COMPARACIÓN DE ESCENARIOS — FLUJOS (Rates)", fontsize=16, fontweight='bold', y=0.98)

# Descarga del camion
ax = axes[0]
for idx, nombre in enumerate(nombres):
    h = resultados[nombre]
    ax.plot(h["time"], h["Descarga del camion"], color=colores[idx], linewidth=2.5,
           label=nombres_cortos[idx], alpha=0.9)
ax.set_ylabel("Cajas/Day")
ax.set_title("⊳ Descarga del camión — Reabastecimiento desde proveedor", pad=8)
ax.legend(loc='right', fontsize=9)
ax.grid(True, alpha=0.3)

# Ventas reales
ax = axes[1]
for idx, nombre in enumerate(nombres):
    h = resultados[nombre]
    tasa_deseada = list(escenarios.values())[idx].get("Tasa de Ventas Concretadas", 15)
    ax.plot(h["time"], h["Ventas"], color=colores[idx], linewidth=2.5,
           label=f'{nombres_cortos[idx]} (real)', alpha=0.9)
    ax.axhline(y=tasa_deseada, color=colores[idx], linestyle=':', alpha=0.4, linewidth=1)
ax.set_ylabel("Cajas/Day")
ax.set_title("⊳ Ventas — Real vs Demanda deseada (línea punteada)", pad=8)
ax.legend(loc='right', fontsize=9)
ax.grid(True, alpha=0.3)

# Generación de mermados
ax = axes[2]
for idx, nombre in enumerate(nombres):
    h = resultados[nombre]
    ax.plot(h["time"], h["Generacion de mermados"], color=colores[idx], linewidth=2.5,
           label=nombres_cortos[idx], alpha=0.9)
ax.set_ylabel("Cajas/Day")
ax.set_xlabel("Tiempo (días)", fontsize=12)
ax.set_title("⊳ Generación de mermados — Pérdidas por deterioro", pad=8)
ax.legend(loc='right', fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.96])
path2 = os.path.join(output_dir, "esc_flujos.png")
plt.savefig(path2, dpi=150, bbox_inches='tight')
plt.close()
print(f"📊 Guardada: {path2}")

# ══════════════════════════════════════════════════════════
# GRÁFICA 3: DASHBOARD RESUMEN
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 2, figsize=(15, 11))
fig.suptitle("DASHBOARD RESUMEN — IMPACTO DE CADA ESCENARIO", fontsize=16, fontweight='bold', y=0.98)

# [0,0] Stock en Gondola con zonas
ax = axes[0, 0]
for idx, nombre in enumerate(nombres):
    h = resultados[nombre]
    ax.plot(h["time"], h["Stock en Gondola"], color=colores[idx], linewidth=2.5,
           label=nombres_cortos[idx])
ax.axhline(y=200, color='#f39c12', linestyle='--', alpha=0.7, label='Objetivo (200)')
ax.axhspan(0, 30, alpha=0.15, color='red', label='Zona crítica')
ax.axhspan(30, 100, alpha=0.1, color='orange', label='Zona de riesgo')
ax.set_title("▭ Stock en Góndola", pad=8)
ax.set_ylabel("Cajas")
ax.set_xlabel("Días")
ax.legend(fontsize=8, loc='right')
ax.grid(True, alpha=0.3)

# [0,1] Ventas perdidas acumuladas
ax = axes[0, 1]
for idx, nombre in enumerate(nombres):
    h = resultados[nombre]
    tasa_deseada = list(escenarios.values())[idx].get("Tasa de Ventas Concretadas", 15)
    perdidas_acum = np.cumsum(np.maximum(0, tasa_deseada - h["Ventas"])) * TIME_STEP
    ax.plot(h["time"], perdidas_acum, color=colores[idx], linewidth=2.5,
           label=nombres_cortos[idx])
ax.set_title("⚠️ Ventas Perdidas ACUMULADAS", pad=8)
ax.set_ylabel("Cajas perdidas (total)")
ax.set_xlabel("Días")
ax.legend(fontsize=8, loc='upper left')
ax.grid(True, alpha=0.3)

# [1,0] Nivel de servicio (% demanda satisfecha por día)
ax = axes[1, 0]
for idx, nombre in enumerate(nombres):
    h = resultados[nombre]
    tasa_deseada = list(escenarios.values())[idx].get("Tasa de Ventas Concretadas", 15)
    # Calcular nivel de servicio como promedio móvil de 5 días
    servicio = (h["Ventas"] / tasa_deseada) * 100
    # Smooth para mejor visualización
    window = int(5 / TIME_STEP)
    servicio_smooth = np.convolve(servicio, np.ones(window)/window, mode='same')
    ax.plot(h["time"], servicio_smooth, color=colores[idx], linewidth=2.5,
           label=nombres_cortos[idx])
ax.axhline(y=100, color='#f39c12', linestyle='--', alpha=0.7, label='100% servicio')
ax.axhline(y=95, color='#e74c3c', linestyle=':', alpha=0.5, label='Meta 95%')
ax.set_title("📈 Nivel de Servicio (% demanda satisfecha)", pad=8)
ax.set_ylabel("% Servicio")
ax.set_xlabel("Días")
ax.set_ylim(0, 110)
ax.legend(fontsize=8, loc='lower right')
ax.grid(True, alpha=0.3)

# [1,1] Barras comparativas de métricas finales
ax = axes[1, 1]
metricas_nombres = ["Ventas\ntotales", "Ventas\nperdidas", "Mermas\ntotales", "Mín. Stock\nGóndola"]
x = np.arange(len(metricas_nombres))
width = 0.25

for idx, nombre in enumerate(nombres):
    h = resultados[nombre]
    tasa_deseada = list(escenarios.values())[idx].get("Tasa de Ventas Concretadas", 15)
    ventas_tot = np.sum(h["Ventas"]) * TIME_STEP
    ventas_deseadas = tasa_deseada * FINAL_TIME
    perdidas = max(0, ventas_deseadas - ventas_tot)
    mermas = np.sum(h["Generacion de mermados"]) * TIME_STEP
    min_gondola = np.min(h["Stock en Gondola"])
    
    valores = [ventas_tot, perdidas, mermas, min_gondola]
    bars = ax.bar(x + idx * width - width, valores, width, label=nombres_cortos[idx], 
                  color=colores[idx], alpha=0.85)
    
    # Etiquetas de valor
    for bar, val in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
               f'{val:.0f}', ha='center', va='bottom', fontsize=7, color='#e0e0e0')

ax.set_title("📊 Métricas Finales (90 días)", pad=8)
ax.set_xticks(x)
ax.set_xticklabels(metricas_nombres, fontsize=9)
ax.set_ylabel("Cajas")
ax.legend(fontsize=8, loc='upper right')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout(rect=[0, 0, 1, 0.96])
path3 = os.path.join(output_dir, "esc_dashboard.png")
plt.savefig(path3, dpi=150, bbox_inches='tight')
plt.close()
print(f"📊 Guardada: {path3}")

# ─────────────────────────────────────────────────────────
# Estadísticas finales
# ─────────────────────────────────────────────────────────
print("\n" + "="*70)
print("ESTADÍSTICAS COMPARATIVAS (90 días)")
print("="*70)

for idx, (nombre, hist) in enumerate(resultados.items()):
    tasa_deseada = list(escenarios.values())[idx].get("Tasa de Ventas Concretadas", 15)
    ventas_totales = np.sum(hist["Ventas"]) * TIME_STEP
    ventas_deseadas = tasa_deseada * FINAL_TIME
    mermas_totales = np.sum(hist["Generacion de mermados"]) * TIME_STEP
    min_gondola = np.min(hist["Stock en Gondola"])
    min_trastienda = np.min(hist["Inventario en Trastienda"])
    nivel_servicio = (ventas_totales / ventas_deseadas) * 100
    
    print(f"\n📦 {nombres_cortos[idx]}")
    print(f"   Ventas totales:        {ventas_totales:8.1f} Cajas (de {ventas_deseadas:.0f} deseadas)")
    print(f"   Ventas perdidas:       {max(0, ventas_deseadas - ventas_totales):8.1f} Cajas")
    print(f"   Nivel de servicio:     {nivel_servicio:8.1f}%")
    print(f"   Mermas totales:        {mermas_totales:8.1f} Cajas")
    print(f"   Mínimo Stock Góndola:  {min_gondola:8.1f} Cajas")
    print(f"   Mínimo Inv. Trastienda:{min_trastienda:8.1f} Cajas")
