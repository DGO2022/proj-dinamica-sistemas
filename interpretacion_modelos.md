# Interpretación de los Modelos de Inventario

## 1. ¿De qué trata este proyecto?
Se trata de una simulación que muestra cómo funciona el inventario de una tienda o supermercado. El sistema está dividido en dos lugares físicos: 
*   **La Trastienda:** El almacén cerrado donde se guardan las reservas.
*   **La Góndola:** Los estantes a la vista donde los clientes agarran los productos.

El objetivo principal de esta tienda es sencillo: **intentar que nunca falten productos para vender, pero sin llenar el almacén hasta que ya no quepa nada.**

---

## 2. Diagrama Causal (La lógica detrás de las decisiones)
Este diagrama nos cuenta "qué causa qué". Nos muestra que el sistema siempre está buscando el equilibrio (no quiere tener estantes vacíos, ni tampoco repletos hasta explotar).

Sus reglas principales son tres:
1.  **Las Compras al Proveedor:** Cuando los trabajadores ven que la trastienda se está quedando sin cajas (hay un "faltante"), piden más al proveedor. El proveedor manda camiones, pero si la trastienda alcanza su límite de capacidad, tienen que dejar de descargar.
2.  **El Relleno de Estantes:** A medida que la góndola se vacía, los empleados sacan cajas de la trastienda para rellenarla. Obviamente, esto solo se puede hacer si aún quedan cajas guardadas atrás.
3.  **Las Salidas (Ventas y Basura):** Los estantes se vacían constantemente por dos motivos: el deseado (los clientes compran los productos) y el indeseado (productos que se caen, se rompen o caducan, y terminan en la basura como mermas).

---

## 3. Diagrama de Forrester (Las matemáticas y la simulación)
Mientras que el diagrama causal nos dice *cómo* funciona la tienda en teoría, el diagrama de Forrester nos permite ponerle **números** y simular los días en una computadora para ver qué pasaría en la vida real.

Se divide en acumulaciones y movimientos:
*   **Los "Tanques" (Niveles):** Son los lugares donde las cajas se quedan quietas acumulándose. En el modelo hay tres: las cajas en la trastienda, las cajas en la góndola, y las cajas dañadas acumuladas antes de botarlas.
*   **Las "Tuberías" (Flujos):** Es el movimiento físico diario. Las cajas entran por la puerta trasera (descarga del camión), caminan por los pasillos (traslado a góndola), y salen por la puerta principal (ventas) o por el basurero (descarte).

**¿Para qué sirve simular esto?**
En la simulación del Forrester podemos jugar con los números para ver si la tienda sobrevive. Por ejemplo, evalúa qué pasaría si:
*   El proveedor es lento y tarda 2 días en traer el camión.
*   El almacén es pequeño y solo caben 800 cajas.
*   Logramos vender unas 15 cajas diarias.
*   Se nos echa a perder un 0.5% de la mercadería por día.

### Conclusión General
Ambos modelos nos enseñan visualmente que el éxito de esta tienda depende totalmente de **sincronizar los tiempos**. Si el camión tarda mucho, la trastienda se vacía, los estantes se vacían y las ventas caen a cero. Además, se debe cuidar la mercadería exhibida, porque lo que se malogra (mermas) es dinero que se va directo a la basura.
