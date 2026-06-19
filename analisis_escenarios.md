# Análisis de 3 Escenarios — Modelo de Inventario de Supermercado

## Escenarios simulados

| Escenario | Cambios vs Base | Propósito |
|-----------|----------------|-----------|
| **1. Base** | Sin cambios | Comportamiento actual del sistema |
| **2. Crisis de demanda** | Ventas = 50 Cajas/Day, Mermas = 3% | Simular temporada alta o promoción agresiva |
| **3. Crisis de suministro** | Proveedor = 10 días, Capacidad trastienda = 300 | Simular interrupción en cadena de suministro |

---

## Resultados — Niveles (Stocks)

![Comparación de niveles en los 3 escenarios](/Users/abelguevarah/.gemini/antigravity-ide/brain/3ebc2ff1-6dd4-40d1-a9da-f5b577a7167b/esc_niveles.png)

---

## Resultados — Dashboard Resumen

![Dashboard comparativo con métricas clave](/Users/abelguevarah/.gemini/antigravity-ide/brain/3ebc2ff1-6dd4-40d1-a9da-f5b577a7167b/esc_dashboard.png)

---

## Estadísticas comparativas (90 días)

| Métrica | Base | Crisis demanda | Crisis suministro |
|---------|:----:|:--------------:|:-----------------:|
| Ventas totales | 1,354 | 4,513 | 1,354 |
| Ventas perdidas | 0 | 0 | 0 |
| Nivel de servicio | 100% | 100% | 100% |
| Mermas totales | 83 | **394** | 83 |
| Mín. Stock Góndola | 150 | 146 | 150 |
| Mín. Inv. Trastienda | 400 | 391 | **296** |

---

## Hallazgo Principal

> [!IMPORTANT]
> ### El sistema es excesivamente resiliente — pero NUNCA alcanza sus objetivos
> 
> En **ningún escenario** (ni siquiera con ventas ×3 o proveedor ×5) el sistema entra en crisis real. Esto es bueno operativamente, pero revela un **problema estructural**: el sistema se auto-estabiliza **por debajo** de sus niveles objetivo.

### ¿Qué significa esto?

| Nivel | Objetivo | Valor estable (Base) | Diferencia |
|-------|:--------:|:--------------------:|:----------:|
| Inventario en Trastienda | 500 | ~470 | -30 Cajas (nunca llega a 500) |
| Stock en Góndola | 200 | ~184 | -16 Cajas (nunca llega a 200) |

**¿Por qué nunca alcanza el objetivo?** Porque hay una **fuga continua**: las mermas (0.5% diario del stock) drenan constantemente la góndola. El sistema de reposición compensa las ventas, pero no compensa completamente las mermas. El equilibrio se alcanza en un punto **inferior** al objetivo.

---

## Interpretación por escenario

### Escenario 1: Base
- **Comportamiento**: El sistema se estabiliza rápidamente (~10 días) cerca de sus objetivos
- **Conclusión**: Con los parámetros actuales, el supermercado funciona establemente pero con un déficit permanente de ~16 cajas en góndola respecto al objetivo

### Escenario 2: Crisis de demanda (Ventas ×3, Mermas ×6)
- **Comportamiento**: A pesar de triplicar las ventas, el sistema se adapta y mantiene servicio al 100%
- **Problema revelado**: Las **mermas se disparan a 394 cajas** (vs 83 en base) — una pérdida de 311 cajas adicionales en 90 días
- **Conclusión**: El costo oculto no son ventas perdidas, sino **mermas**. Con alta demanda, hay más stock en tránsito y más se deteriora

### Escenario 3: Crisis de suministro (Proveedor ×5, Capacidad ÷2.7)
- **Comportamiento**: La trastienda baja a ~296 cajas (mínimo), pero se recupera
- **Problema revelado**: La **capacidad reducida a 300** limita el buffer de seguridad. Si el proveedor tardara aún más (>15 días), el sistema colapsaría
- **Conclusión**: El sistema tiene margen, pero depende fuertemente de que el proveedor no falle por más de ~10 días

---

## Observaciones para el profesor

> [!WARNING]
> ### 3 puntos clave para la presentación:
>
> 1. **Retroalimentación negativa dominante**: Los bucles de retroalimentación negativa (faltante → reposición → reduce faltante) hacen que el sistema sea **auto-correctivo**. Esto explica por qué es tan estable, pero también por qué nunca alcanza el 100% de su objetivo.
>
> 2. **Las mermas son el costo oculto**: En crisis de demanda, el sistema mantiene servicio al 100%, pero el costo real se transfiere a las mermas (×5 más mermas). Un gerente vería ventas perfectas sin notar que está perdiendo producto.
>
> 3. **El modelo es "demasiado amable"**: Para generar una crisis real (ventas perdidas, góndola vacía), se necesitarían condiciones muy extremas. Esto sugiere que los parámetros actuales representan un sistema **sobredimensionado** para su demanda.

---

## Archivos generados

| Archivo | Contenido |
|---------|-----------|
| [esc_niveles.png](file:///Users/abelguevarah/Desktop/proj-dinamica-sistemas/esc_niveles.png) | Gráfica de niveles (stocks) |
| [esc_flujos.png](file:///Users/abelguevarah/Desktop/proj-dinamica-sistemas/esc_flujos.png) | Gráfica de flujos (rates) |
| [esc_dashboard.png](file:///Users/abelguevarah/Desktop/proj-dinamica-sistemas/esc_dashboard.png) | Dashboard resumen con métricas |
| [simulacion_escenarios.py](file:///Users/abelguevarah/Desktop/proj-dinamica-sistemas/simulacion_escenarios.py) | Script Python de simulación |
