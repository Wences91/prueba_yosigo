# Análisis de Datos GBD (Global Burden of Disease)

Este proyecto analiza datos de DALYs (Disability-Adjusted Life Years - Años de Vida Ajustados por Discapacidad) del estudio Global Burden of Disease, generando visualizaciones de evolución temporal y rankings de enfermedades.

## Características

- 📈 **Evolución Temporal**: Gráficos de líneas mostrando la evolución de las principales causas de DALYs a lo largo de los años
- 🏆 **Rankings**: Gráficos de barras con las principales causas ordenadas por impacto
- 👥 **Comparación por Sexo**: Análisis comparativo entre hombres y mujeres
- 🔥 **Mapas de Calor**: Visualización de la evolución temporal usando heatmaps

## Requisitos

- Python 3.8 o superior
- Bibliotecas listadas en `requirements.txt`

## Instalación

1. **Clonar o descargar el repositorio**

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

## Uso

### Uso Básico

Ejecutar el análisis con la configuración predeterminada:

```bash
python analisis_gbd.py
```

Esto generará automáticamente un reporte completo con los siguientes gráficos:
- Evolución temporal de las 10 principales causas
- Ranking de las 20 principales causas
- Comparación por sexo de las 15 principales causas
- Mapa de calor de las 15 principales causas

Todos los gráficos se guardarán en la carpeta `graficos/`.

### Uso Avanzado

Para personalizar el análisis, puedes usar el script `analisis_personalizado.py`:

```bash
python analisis_personalizado.py
```

O modificar directamente el archivo `analisis_gbd.py` para utilizar las siguientes funciones:

```python
from analisis_gbd import AnalizadorGBD

# Crear analizador
analizador = AnalizadorGBD("gbd_all_dalys_1423.csv")

# Evolución temporal de las 15 causas principales
analizador.evolucion_temporal_top_causas(
    top_n=15,
    ubicacion="Global",
    sexo="Both",
    edad="All ages"
)

# Ranking para un año específico
analizador.ranking_causas(
    año=2020,
    top_n=25,
    ubicacion="Global",
    sexo="Both",
    edad="All ages",
    horizontal=True
)

# Comparación por sexo
analizador.comparacion_por_sexo(
    top_n=20,
    ubicacion="Global",
    edad="All ages",
    año=2020
)

# Mapa de calor
analizador.heatmap_causas_años(
    top_n=20,
    ubicacion="Global",
    sexo="Both",
    edad="All ages"
)
```

## Parámetros Disponibles

### `evolucion_temporal_top_causas()`
- `top_n`: Número de causas principales a mostrar (default: 10)
- `ubicacion`: Ubicación geográfica (ej: "Global")
- `sexo`: "Both", "Male" o "Female"
- `edad`: Grupo de edad (ej: "All ages")

### `ranking_causas()`
- `año`: Año específico (None = promedio de todos los años)
- `top_n`: Número de causas a mostrar (default: 20)
- `ubicacion`: Ubicación geográfica
- `sexo`: "Both", "Male" o "Female"
- `edad`: Grupo de edad
- `horizontal`: True para barras horizontales, False para verticales

### `comparacion_por_sexo()`
- `top_n`: Número de causas principales (default: 15)
- `ubicacion`: Ubicación geográfica
- `edad`: Grupo de edad
- `año`: Año específico (None = promedio)

### `heatmap_causas_años()`
- `top_n`: Número de causas principales (default: 15)
- `ubicacion`: Ubicación geográfica
- `sexo`: "Both", "Male" o "Female"
- `edad`: Grupo de edad

## Estructura del Proyecto

```
.
├── gbd_all_dalys_1423.csv      # Archivo de datos
├── analisis_gbd.py              # Script principal de análisis
├── analisis_personalizado.py   # Script para análisis personalizado
├── requirements.txt             # Dependencias de Python
├── README.md                    # Este archivo
└── graficos/                    # Carpeta con los gráficos generados (se crea automáticamente)
```

## Datos

El archivo `gbd_all_dalys_1423.csv` contiene datos del Global Burden of Disease con las siguientes columnas:

- `measure_name`: Medida (DALYs)
- `location_name`: Ubicación geográfica
- `sex_name`: Sexo (Both/Male/Female)
- `age_name`: Grupo de edad
- `cause_name`: Causa/enfermedad
- `year`: Año
- `val`: Valor de DALYs
- `upper`/`lower`: Intervalos de confianza

## Ejemplos de Salida

Los gráficos generados incluyen:

1. **Evolución Temporal**: Líneas temporales mostrando cómo cambian los DALYs de las principales causas
2. **Rankings**: Barras horizontales o verticales con las causas ordenadas por impacto
3. **Comparación por Sexo**: Barras agrupadas comparando hombres vs mujeres
4. **Mapas de Calor**: Heatmap mostrando intensidad de DALYs por causa y año

## Contribuciones

Este proyecto es de código abierto. Siéntete libre de contribuir con mejoras o reportar problemas.

## Licencia

MIT License
