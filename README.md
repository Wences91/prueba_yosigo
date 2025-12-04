# 📊 Análisis de Datos GBD (Global Burden of Disease)

Proyecto de análisis y visualización de datos de DALYs (Disability-Adjusted Life Years - Años de Vida Ajustados por Discapacidad) del estudio Global Burden of Disease.

## 🎯 Características

- 📈 **Evolución Temporal**: Gráficos de líneas mostrando la evolución de las principales causas de DALYs a lo largo de los años
- 🏆 **Rankings**: Gráficos de barras con las principales causas ordenadas por impacto
- 👥 **Comparación por Sexo**: Análisis comparativo entre hombres y mujeres (cuando hay datos disponibles)
- 🔥 **Mapas de Calor**: Visualización de la evolución temporal usando heatmaps
- 🎨 **Gráficos de Alta Calidad**: Exportación en alta resolución (300 DPI)
- ⚙️ **Configuración Flexible**: Fácil personalización de parámetros

## 📁 Estructura del Proyecto

```
prueba_yosigo/
├── data/                          # Datos de entrada
│   └── gbd_all_dalys_1423.csv    # Dataset GBD
├── src/                           # Código fuente
│   ├── analisis_gbd.py           # Script principal con clase AnalizadorGBD
│   └── analisis_personalizado.py # Script personalizable
├── output/                        # Resultados generados
│   └── graficos/                 # Gráficos generados
├── scripts/                       # Scripts de utilidad
│   ├── instalar.sh               # Script de instalación
│   ├── ejecutar.sh               # Ejecuta análisis básico
│   └── ejecutar_personalizado.sh # Ejecuta análisis personalizado
├── .gitignore                     # Archivos ignorados por git
├── requirements.txt               # Dependencias de Python
└── README.md                      # Este archivo
```

## 🚀 Inicio Rápido

### Instalación Automática

```bash
# Clonar o descargar el repositorio
git clone <url-del-repo>
cd prueba_yosigo

# Instalar dependencias
bash scripts/instalar.sh
```

### Instalación Manual

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Opción 1: Análisis Rápido (Recomendado)

Ejecuta el análisis con configuración predeterminada:

```bash
bash scripts/ejecutar.sh
```

O desde Python:

```bash
python3 src/analisis_gbd.py
```

**Esto generará automáticamente:**
- Evolución temporal de las 10 principales causas
- Ranking de las 20 principales causas (año 2017)
- Mapa de calor de las 15 principales causas

### Opción 2: Análisis Personalizado

Edita primero el archivo `src/analisis_personalizado.py` para configurar:
- Ubicación geográfica
- Grupo de edad
- Sexo
- Año específico
- Número de causas principales (top_n)

Luego ejecuta:

```bash
bash scripts/ejecutar_personalizado.sh
```

O desde Python:

```bash
python3 src/analisis_personalizado.py
```

### Opción 3: Uso Programático

```python
from pathlib import Path
import sys

# Añadir src al path si es necesario
sys.path.append('src')

from analisis_gbd import AnalizadorGBD

# Crear analizador
analizador = AnalizadorGBD("data/gbd_all_dalys_1423.csv")

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
    horizontal=True  # False para vertical
)

# Mapa de calor
analizador.heatmap_causas_años(
    top_n=20,
    ubicacion="Global",
    sexo="Both",
    edad="All ages"
)
```

## 📊 Tipos de Visualizaciones

### 1. Evolución Temporal
Gráfico de líneas mostrando cómo evolucionan las principales causas a lo largo del tiempo.

**Función:** `evolucion_temporal_top_causas()`

**Parámetros:**
- `top_n`: Número de causas principales (default: 10)
- `ubicacion`: Ubicación geográfica (ej: "Global")
- `sexo`: "Both", "Male" o "Female"
- `edad`: Grupo de edad (ej: "All ages")

### 2. Rankings
Gráfico de barras (horizontal o vertical) con las causas ordenadas por impacto.

**Función:** `ranking_causas()`

**Parámetros:**
- `año`: Año específico (None = promedio de todos los años)
- `top_n`: Número de causas (default: 20)
- `ubicacion`: Ubicación geográfica
- `sexo`: "Both", "Male" o "Female"
- `edad`: Grupo de edad
- `horizontal`: True para barras horizontales, False para verticales

### 3. Comparación por Sexo
Gráfico de barras agrupadas comparando hombres vs mujeres.

**Función:** `comparacion_por_sexo()`

**Parámetros:**
- `top_n`: Número de causas principales (default: 15)
- `ubicacion`: Ubicación geográfica
- `edad`: Grupo de edad
- `año`: Año específico (None = promedio)

**Nota:** Solo funciona si el dataset contiene datos separados por sexo.

### 4. Mapa de Calor
Heatmap mostrando la intensidad de DALYs por causa y año.

**Función:** `heatmap_causas_años()`

**Parámetros:**
- `top_n`: Número de causas principales (default: 15)
- `ubicacion`: Ubicación geográfica
- `sexo`: "Both", "Male" o "Female"
- `edad`: Grupo de edad

## 📦 Dependencias

- **pandas** (≥2.0.0): Análisis y manipulación de datos
- **matplotlib** (≥3.7.0): Creación de gráficos
- **seaborn** (≥0.12.0): Visualizaciones estadísticas
- **numpy** (≥1.24.0): Operaciones numéricas

## 📄 Datos

El archivo `data/gbd_all_dalys_1423.csv` contiene datos del Global Burden of Disease con las siguientes columnas:

| Columna | Descripción |
|---------|-------------|
| `measure_name` | Medida (DALYs) |
| `location_name` | Ubicación geográfica |
| `sex_name` | Sexo (Both/Male/Female) |
| `age_name` | Grupo de edad |
| `cause_name` | Causa/enfermedad |
| `year` | Año |
| `val` | Valor de DALYs |
| `upper`/`lower` | Intervalos de confianza |

**Información del dataset actual:**
- Años: 2014-2023
- Ubicaciones: 1 (Global)
- Causas/Enfermedades: 381
- Grupos de edad: 1 (All ages)
- Sexo: Both

## 🎨 Ejemplos de Salida

Los gráficos generados se guardan en `output/graficos/` con nombres descriptivos:

- `evolucion_temporal_top10_Global_Both_All_ages.png`
- `ranking_top20_2017_Global_Both_All_ages_horiz.png`
- `heatmap_top15_Global_Both_All_ages.png`

Todos los gráficos incluyen:
- Títulos descriptivos con parámetros utilizados
- Valores numéricos formateados con separadores de miles
- Colores profesionales y atractivos
- Alta resolución (300 DPI) para publicaciones

## 🔧 Personalización Avanzada

Para crear análisis más complejos, puedes:

1. Importar la clase `AnalizadorGBD` en tu propio script
2. Combinar múltiples visualizaciones
3. Modificar los parámetros de estilo en `analisis_gbd.py` (líneas 15-18)
4. Añadir nuevos métodos de visualización

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

MIT License - Siéntete libre de usar este proyecto para cualquier propósito.

## 📧 Soporte

Si encuentras problemas o tienes preguntas:
- Abre un issue en GitHub
- Revisa que todas las dependencias estén instaladas
- Verifica que el archivo de datos esté en la ubicación correcta

---

**¡Disfruta analizando datos del Global Burden of Disease!** 🎉
