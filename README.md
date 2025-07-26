
# Interpolación Cúbica y Curvatura

Este proyecto realiza una interpolación cúbica sobre puntos definidos por el usuario,
calcula la curvatura en cada punto y exporta los resultados en archivos PDF y CSV.

## 📦 Estructura del Proyecto

```
interpolacion_modular/
├── main.py            # Script principal
├── interpolador.py    # Funciones matemáticas y validaciones
└── graficador.py      # Visualización y exportación de resultados
```

## 🛠️ Requisitos

- Python 3.8 o superior
- Paquetes necesarios:

```bash
pip install numpy matplotlib mplcursors scikit-learn
```

## 🚀 Uso

1. Ejecuta `main.py`
2. Selecciona puntos con el mouse (mínimo 4)
3. Visualiza la interpolación y curvatura
4. Se generarán:
   - Un archivo PDF con la curva coloreada por curvatura
   - Un archivo CSV con los valores interpolados y su curvatura

## 🧠 Créditos

Autor: Miguel Eduardo Venegas Monroy  
Fecha: Julio 2025
