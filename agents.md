# Proyecto Flask + Vanilla JS  
## Proyecto final Bootcamp – Aprender a programar desde cero

---

## 🏊 A zambullirse donde cubre

Hasta ahora habéis estado ejercitando vuestras habilidades de programadores (tanto las básicas de pensamiento computacional como las avanzadas de programación en Python y desarrollo de distintos tipos de pequeñas aplicaciones - juegos, escritorio y web -).  
Os toca soltaros de la orilla y nadar en lo hondo.

El objetivo es desarrollar una pequeña aplicación (un prototipo) lo más completa funcionalmente y sin errores.  
Tendréis tres semanas para hacerlo, durante las cuales deberéis investigar, decidir, estudiar y aprender cosas nuevas.

**Objetivos fundamentales:**
- Aprender y disfrutar.
- Desarrollar el proyecto lo más avanzado posible.
- Se valorará tanto el modo de resolución como el alcance.
- Podéis modificar, añadir o reemplazar funcionalidades siempre que no sirva para “escaquearse del trabajo”.

---

## 📄 Sobre este documento

Cada funcionalidad aparece descrita con:
- Qué debe hacer la app.
- Restricciones obligatorias.
- Opciones opcionales para mejorar o destacar.

---

## 💰 La aplicación web: Registro de movimientos de criptomonedas

Vamos a crear un **registro de inversiones y compra/venta de criptos** para jugar con los valores y comprobar si nuestra inversión crece en euros o no.

### Monedas disponibles:
EUR, BTC, ETH, USDT, BNB, XRP, ADA, SOL, DOT, MATIC

### API externa:
Usaremos **CoinMarketCap API**:

- https://pro-api.coinmarketcap.com/v2/tools/price-conversion (conversiones)
- https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest (listado de valores)
- Plan gratuito: 10.000 peticiones/mes, 30 peticiones/minuto.

---

## 🎯 Objetivo y funcionamiento de la aplicación

La aplicación permitirá realizar tres tipos de conversiones (**from/to**):

1. **COMPRA:** De euros a cripto.  
   - Se considera inversión.  
   - Los euros son infinitos.

2. **TRADEO:** De una cripto a otra.  
   - Solo se puede usar el saldo disponible en criptos adquiridas previamente.

3. **VENTA:** De cripto a euros.  
   - Se considera recuperación de inversión.  
   - Si el valor obtenido supera lo invertido, hay beneficio.

---

## ⚙️ Backend con Flask

La API de backend tendrá tres endpoints principales:

---

### /api/v1/movimientos  
**GET**

Devuelve un JSON con la lista de movimientos (compras, ventas, tradeos).

**Formato de respuesta:**
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "fecha": "2021-01-01",
      "hora": "10:00:00",
      "from_moneda": "EUR",
      "from_cantidad": 3675.25,
      "to_moneda": "BTC",
      "to_cantidad": 1
    }
  ]
}

**En caso de error:**
{
  "status": "fail",
  "mensaje": "Mensaje de error"
}

---

### /api/v1/tasa/<moneda_from>/<moneda_to>  
**GET**

Devuelve la tasa de conversión entre dos monedas.

**Respuesta exitosa:**
{
  "status": "success",
  "rate": 19863.98,
  "monedas": ["EUR", "BTC", "ETH", ...]
}

**Error:**
{
  "status": "fail",
  "mensaje": "Mensaje de error"
}

---

### /api/v1/movimiento  
**POST**

Da de alta un nuevo movimiento (compra, venta o tradeo).

**Formato de envío:**
{
  "fecha": "2021-01-02",
  "hora": "11:00:00",
  "from_moneda": "BTC",
  "from_cantidad": 0.05,
  "to_moneda": "ETH",
  "to_cantidad": 2
}

**Restricciones:**
- Si from_moneda no es EUR, comprobar que hay saldo suficiente.  
- Saldo = (sumatoria de to_cantidad) - (sumatoria de from_cantidad).

**Respuestas posibles:**
- Éxito:
  { "status": "success", "id": 5, "monedas": ["EUR", ...] }
- Saldo insuficiente:
  { "status": "fail", "mensaje": "Saldo insuficiente" }
- Error:
  { "status": "fail", "mensaje": "Mensaje de error" }

---

### /api/v1/status  
**GET**

Devuelve el estado actual de la inversión en euros.

**Datos devueltos:**
- **Invertido:** total de euros usados en compras.  
- **Recuperado:** total de euros recuperados en ventas.  
- **Valor de compra:** invertido - recuperado.  
- **Valor actual:** valor en euros de todas las criptos según su tasa actual.

**Ejemplo:**
{
  "status": "success",
  "data": {
    "invertido": 1000.00,
    "recuperado": 750.00,
    "valor_compra": 250.00,
    "valor_actual": 2350.73
  }
}

---

## 💹 Ejemplo de cálculo

1. Compra: 0.1 BTC con 1000 €  
2. Tradeo: 0.05 BTC → 2 ETH  
3. Venta: 1 ETH → 750 €  

Resultado:
- Invertido: 1000 €
- Recuperado: 750 €
- Valor compra: 250 €
- Cartera actual: 0.05 BTC + 1 ETH  
  (≈ 2.350,73 € actuales)

---

## 🧠 Frontend con JavaScript

La interfaz unifica las tres funcionalidades principales.

### Listado de movimientos
- Petición a /api/v1/movimientos al cargar y tras cada operación.
- Si no hay movimientos, tabla vacía.
- En caso de error, alert al usuario.

### Estado de la inversión
- Petición a /api/v1/status al cargar o al pulsar “Actualizar”.
- Mostrar pérdidas en rojo.
- Usar botón o clic para recalcular (debido a límite de peticiones diario).

### Compra / Venta / Tradeo
1. Seleccionar moneda_from y moneda_to (deben ser diferentes).  
2. Ingresar cantidad y pulsar Calcular.  
3. Llamar a coinAPI para obtener la tasa actual.  
4. Mostrar cantidad destino (Q_To) y precio unitario.  
5. Si el usuario confirma, enviar POST a /api/v1/movimiento.  
6. Si todo va bien, refrescar la tabla de movimientos.

**Restricciones:**
- Debe existir saldo suficiente.
- From ≠ To.

---

## 🗄️ Tabla SQLite: movimientos

| Columna        | Tipo | Descripción |
|----------------|------|-------------|
| id             | INTEGER (PK) | Identificador |
| date           | TEXT | YYYY-MM-DD |
| time           | TEXT | HH:mm:SS |
| moneda_from    | TEXT | Código moneda origen |
| cantidad_from  | REAL | Cantidad origen |
| moneda_to      | TEXT | Código moneda destino |
| cantidad_to    | REAL | Cantidad destino |

---

## 🧩 Forma de trabajo

- Proyecto **individual**.
- Duración: del **20 de octubre al 2 de noviembre de 2025 (23:59 Madrid)**.
- Entrega: enlace al **repositorio remoto** con:
  - Código completo.
  - requirements.txt
  - Base de datos vacía o script para crearla.
  - Instrucciones de instalación en README.md.

Los proyectos se corregirán tras la fecha de entrega y se comunicará la nota por correo.
