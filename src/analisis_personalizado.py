#!/usr/bin/env python3
"""
Script de análisis personalizado de datos GBD
Modifica los parámetros según tus necesidades
"""

from analisis_gbd import AnalizadorGBD
from pathlib import Path


def main():
    """
    Análisis personalizado - Modifica estos parámetros según necesites
    """

    # ============================================================================
    # CONFIGURACIÓN - Modifica estos valores según tus necesidades
    # ============================================================================

    # Archivo de datos - detecta si se ejecuta desde src/ o desde raíz
    if Path.cwd().name == 'src':
        ARCHIVO_CSV = "../data/gbd_all_dalys_1423.csv"
    else:
        ARCHIVO_CSV = "data/gbd_all_dalys_1423.csv"

    # Ubicación geográfica para analizar
    # Ejemplo: "Global", "United States", "Spain", etc.
    UBICACION = "Global"

    # Sexo para el análisis
    # Opciones: "Both", "Male", "Female"
    SEXO = "Both"

    # Grupo de edad
    # Ejemplo: "All ages", "15-49 years", etc.
    EDAD = "All ages"

    # Año específico para rankings (None = promedio de todos los años)
    AÑO_RANKING = 2017

    # Número de causas principales a mostrar en cada gráfico
    TOP_EVOLUCION = 10      # Para gráfico de evolución temporal
    TOP_RANKING = 20        # Para ranking de causas
    TOP_COMPARACION = 15    # Para comparación por sexo
    TOP_HEATMAP = 15        # Para mapa de calor

    # ============================================================================
    # ANÁLISIS - No es necesario modificar lo siguiente
    # ============================================================================

    print("\n" + "="*70)
    print("ANÁLISIS PERSONALIZADO DE DATOS GBD")
    print("="*70)
    print(f"Ubicación: {UBICACION}")
    print(f"Sexo: {SEXO}")
    print(f"Edad: {EDAD}")
    print(f"Año para ranking: {AÑO_RANKING if AÑO_RANKING else 'Promedio'}")
    print("="*70 + "\n")

    # Crear analizador
    analizador = AnalizadorGBD(ARCHIVO_CSV)

    # Puedes comentar/descomentar los análisis que quieras ejecutar
    # (añade # al inicio de la línea para comentar)

    # 1. Evolución temporal
    print("\n--- Generando evolución temporal ---")
    analizador.evolucion_temporal_top_causas(
        top_n=TOP_EVOLUCION,
        ubicacion=UBICACION,
        sexo=SEXO,
        edad=EDAD
    )

    # 2. Ranking de causas
    print("\n--- Generando ranking de causas ---")
    analizador.ranking_causas(
        año=AÑO_RANKING,
        top_n=TOP_RANKING,
        ubicacion=UBICACION,
        sexo=SEXO,
        edad=EDAD,
        horizontal=True  # Cambia a False para barras verticales
    )

    # 3. Comparación por sexo
    print("\n--- Generando comparación por sexo ---")
    analizador.comparacion_por_sexo(
        top_n=TOP_COMPARACION,
        ubicacion=UBICACION,
        edad=EDAD,
        año=AÑO_RANKING
    )

    # 4. Mapa de calor
    print("\n--- Generando mapa de calor ---")
    analizador.heatmap_causas_años(
        top_n=TOP_HEATMAP,
        ubicacion=UBICACION,
        sexo=SEXO,
        edad=EDAD
    )

    # ============================================================================
    # ANÁLISIS ADICIONALES (OPCIONAL)
    # ============================================================================
    # Descomenta las siguientes líneas para análisis adicionales

    # Comparar diferentes años
    # print("\n--- Ranking año 2020 ---")
    # analizador.ranking_causas(año=2020, top_n=15, ubicacion=UBICACION)

    # print("\n--- Ranking promedio todos los años ---")
    # analizador.ranking_causas(año=None, top_n=15, ubicacion=UBICACION)

    # Análisis por sexo separado
    # print("\n--- Evolución temporal - Solo hombres ---")
    # analizador.evolucion_temporal_top_causas(top_n=10, ubicacion=UBICACION, sexo="Male")

    # print("\n--- Evolución temporal - Solo mujeres ---")
    # analizador.evolucion_temporal_top_causas(top_n=10, ubicacion=UBICACION, sexo="Female")

    print("\n" + "="*70)
    print("✓ ANÁLISIS COMPLETADO")
    print(f"✓ Todos los gráficos guardados en: graficos/")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
