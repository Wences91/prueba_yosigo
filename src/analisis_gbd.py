#!/usr/bin/env python3
"""
Análisis de datos GBD (Global Burden of Disease) - DALYs
Genera gráficos de evolución temporal y rankings de enfermedades
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


class AnalizadorGBD:
    """Clase para analizar datos del Global Burden of Disease"""

    def __init__(self, archivo_csv):
        """Inicializa el analizador cargando los datos"""
        print(f"Cargando datos desde {archivo_csv}...")
        self.df = pd.read_csv(archivo_csv)
        print(f"✓ Datos cargados: {len(self.df)} registros")

        # Crear carpeta para guardar los gráficos
        # Detecta si se ejecuta desde src/ o desde raíz
        if Path.cwd().name == 'src':
            self.carpeta_graficos = Path("../output/graficos")
        else:
            self.carpeta_graficos = Path("output/graficos")
        self.carpeta_graficos.mkdir(parents=True, exist_ok=True)

        # Mostrar información básica
        self._mostrar_info_basica()

    def _mostrar_info_basica(self):
        """Muestra información básica sobre el dataset"""
        print("\n" + "="*60)
        print("INFORMACIÓN DEL DATASET")
        print("="*60)
        print(f"Años disponibles: {sorted(self.df['year'].unique())}")
        print(f"Ubicaciones: {self.df['location_name'].nunique()}")
        print(f"Enfermedades/Causas: {self.df['cause_name'].nunique()}")
        print(f"Grupos de edad: {self.df['age_name'].nunique()}")
        print(f"Sexos: {self.df['sex_name'].unique()}")
        print("="*60 + "\n")

    def evolucion_temporal_top_causas(self, top_n=10, ubicacion="Global",
                                      sexo="Both", edad="All ages"):
        """
        Genera gráfico de evolución temporal de las principales causas

        Args:
            top_n: Número de causas principales a mostrar
            ubicacion: Ubicación geográfica (ej: "Global", país específico)
            sexo: "Both", "Male" o "Female"
            edad: Grupo de edad
        """
        print(f"\n📊 Generando gráfico de evolución temporal (Top {top_n} causas)...")

        # Filtrar datos
        df_filtrado = self.df[
            (self.df['location_name'] == ubicacion) &
            (self.df['sex_name'] == sexo) &
            (self.df['age_name'] == edad)
        ].copy()

        # Calcular el total por causa (suma de todos los años)
        total_por_causa = df_filtrado.groupby('cause_name')['val'].sum().sort_values(ascending=False)
        top_causas = total_por_causa.head(top_n).index.tolist()

        # Filtrar solo las top causas
        df_top = df_filtrado[df_filtrado['cause_name'].isin(top_causas)]

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(16, 10))

        # Agrupar por año y causa
        evolucion = df_top.groupby(['year', 'cause_name'])['val'].sum().reset_index()

        # Crear líneas para cada causa
        for causa in top_causas:
            datos_causa = evolucion[evolucion['cause_name'] == causa]
            ax.plot(datos_causa['year'], datos_causa['val'],
                   marker='o', linewidth=2.5, label=causa, markersize=6)

        ax.set_xlabel('Año', fontsize=14, fontweight='bold')
        ax.set_ylabel('DALYs (Años de Vida Ajustados por Discapacidad)', fontsize=14, fontweight='bold')
        ax.set_title(f'Evolución Temporal de las {top_n} Principales Causas de DALYs\n{ubicacion} - {sexo} - {edad}',
                    fontsize=16, fontweight='bold', pad=20)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)

        # Formato del eje Y con separadores de miles
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

        plt.tight_layout()

        # Guardar
        nombre_archivo = f"evolucion_temporal_top{top_n}_{ubicacion.replace(' ', '_')}_{sexo}_{edad.replace(' ', '_')}.png"
        ruta = self.carpeta_graficos / nombre_archivo
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico guardado: {ruta}")
        plt.close()

        return evolucion

    def ranking_causas(self, año=None, top_n=20, ubicacion="Global",
                       sexo="Both", edad="All ages", horizontal=True):
        """
        Genera un gráfico de ranking de causas para un año específico

        Args:
            año: Año específico (si es None, usa el promedio de todos los años)
            top_n: Número de causas a mostrar
            ubicacion: Ubicación geográfica
            sexo: "Both", "Male" o "Female"
            edad: Grupo de edad
            horizontal: Si True, gráfico de barras horizontal; si False, vertical
        """
        titulo_año = f"año {año}" if año else "promedio todos los años"
        print(f"\n📊 Generando ranking de causas ({titulo_año}, Top {top_n})...")

        # Filtrar datos
        df_filtrado = self.df[
            (self.df['location_name'] == ubicacion) &
            (self.df['sex_name'] == sexo) &
            (self.df['age_name'] == edad)
        ].copy()

        if año:
            df_filtrado = df_filtrado[df_filtrado['year'] == año]
            if len(df_filtrado) == 0:
                print(f"⚠️ No hay datos para el año {año}")
                return None

        # Calcular ranking
        ranking = df_filtrado.groupby('cause_name')['val'].mean().sort_values(ascending=False).head(top_n)

        # Crear gráfico
        fig, ax = plt.subplots(figsize=(14, 10))

        if horizontal:
            # Gráfico de barras horizontal
            colores = sns.color_palette("rocket_r", n_colors=len(ranking))
            bars = ax.barh(range(len(ranking)), ranking.values, color=colores, edgecolor='black', linewidth=0.7)
            ax.set_yticks(range(len(ranking)))
            ax.set_yticklabels(ranking.index, fontsize=10)
            ax.set_xlabel('DALYs', fontsize=13, fontweight='bold')
            ax.invert_yaxis()

            # Añadir valores en las barras
            for i, (causa, valor) in enumerate(ranking.items()):
                ax.text(valor, i, f' {valor:,.0f}', va='center', fontsize=9, fontweight='bold')
        else:
            # Gráfico de barras vertical
            colores = sns.color_palette("rocket_r", n_colors=len(ranking))
            bars = ax.bar(range(len(ranking)), ranking.values, color=colores, edgecolor='black', linewidth=0.7)
            ax.set_xticks(range(len(ranking)))
            ax.set_xticklabels(ranking.index, rotation=45, ha='right', fontsize=9)
            ax.set_ylabel('DALYs', fontsize=13, fontweight='bold')

            # Añadir valores en las barras
            for i, (causa, valor) in enumerate(ranking.items()):
                ax.text(i, valor, f'{valor:,.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

        titulo = f'Ranking de las {top_n} Principales Causas de DALYs\n{ubicacion} - {sexo} - {edad}'
        if año:
            titulo += f' - Año {año}'
        else:
            titulo += ' - Promedio de todos los años'

        ax.set_title(titulo, fontsize=15, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='x' if horizontal else 'y')

        # Formato del eje con separadores de miles
        if horizontal:
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
        else:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

        plt.tight_layout()

        # Guardar
        orientacion = "horiz" if horizontal else "vert"
        año_str = f"{año}" if año else "promedio"
        nombre_archivo = f"ranking_top{top_n}_{año_str}_{ubicacion.replace(' ', '_')}_{sexo}_{edad.replace(' ', '_')}_{orientacion}.png"
        ruta = self.carpeta_graficos / nombre_archivo
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico guardado: {ruta}")
        plt.close()

        return ranking

    def comparacion_por_sexo(self, top_n=15, ubicacion="Global", edad="All ages", año=None):
        """
        Compara los DALYs entre hombres y mujeres

        Args:
            top_n: Número de causas principales
            ubicacion: Ubicación geográfica
            edad: Grupo de edad
            año: Año específico (si es None, usa el promedio)
        """
        print(f"\n📊 Generando comparación por sexo (Top {top_n} causas)...")

        # Verificar si hay datos por sexo
        sexos_disponibles = self.df['sex_name'].unique()
        if not ('Male' in sexos_disponibles and 'Female' in sexos_disponibles):
            print(f"⚠️  No hay datos separados por sexo (Male/Female) en el dataset")
            print(f"   Sexos disponibles: {', '.join(sexos_disponibles)}")
            print(f"   Omitiendo análisis de comparación por sexo...")
            return None

        # Filtrar datos
        df_filtrado = self.df[
            (self.df['location_name'] == ubicacion) &
            (self.df['age_name'] == edad) &
            (self.df['sex_name'].isin(['Male', 'Female']))
        ].copy()

        if año:
            df_filtrado = df_filtrado[df_filtrado['year'] == año]

        if len(df_filtrado) == 0:
            print(f"⚠️  No hay datos disponibles para los parámetros especificados")
            return None

        # Calcular totales por sexo
        comparacion = df_filtrado.groupby(['cause_name', 'sex_name'])['val'].mean().reset_index()

        # Obtener las top causas (basado en el total)
        total_causas = comparacion.groupby('cause_name')['val'].sum().sort_values(ascending=False).head(top_n)
        top_causas = total_causas.index.tolist()

        # Filtrar solo top causas
        comparacion_top = comparacion[comparacion['cause_name'].isin(top_causas)]

        # Preparar datos para el gráfico
        datos_pivot = comparacion_top.pivot(index='cause_name', columns='sex_name', values='val')
        datos_pivot = datos_pivot.reindex(top_causas)

        # Crear gráfico
        fig, ax = plt.subplots(figsize=(14, 10))

        x = np.arange(len(top_causas))
        ancho = 0.35

        bars1 = ax.bar(x - ancho/2, datos_pivot['Male'], ancho, label='Hombres',
                       color='steelblue', edgecolor='black', linewidth=0.7)
        bars2 = ax.bar(x + ancho/2, datos_pivot['Female'], ancho, label='Mujeres',
                       color='coral', edgecolor='black', linewidth=0.7)

        ax.set_xlabel('Causas', fontsize=13, fontweight='bold')
        ax.set_ylabel('DALYs', fontsize=13, fontweight='bold')

        titulo = f'Comparación de DALYs por Sexo - Top {top_n} Causas\n{ubicacion} - {edad}'
        if año:
            titulo += f' - Año {año}'
        else:
            titulo += ' - Promedio de todos los años'

        ax.set_title(titulo, fontsize=15, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(top_causas, rotation=45, ha='right', fontsize=9)
        ax.legend(fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')

        # Formato del eje Y
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

        plt.tight_layout()

        # Guardar
        año_str = f"{año}" if año else "promedio"
        nombre_archivo = f"comparacion_sexo_top{top_n}_{año_str}_{ubicacion.replace(' ', '_')}_{edad.replace(' ', '_')}.png"
        ruta = self.carpeta_graficos / nombre_archivo
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico guardado: {ruta}")
        plt.close()

        return datos_pivot

    def heatmap_causas_años(self, top_n=15, ubicacion="Global", sexo="Both", edad="All ages"):
        """
        Genera un mapa de calor mostrando la evolución de causas a lo largo de los años

        Args:
            top_n: Número de causas principales
            ubicacion: Ubicación geográfica
            sexo: Sexo
            edad: Grupo de edad
        """
        print(f"\n📊 Generando mapa de calor de evolución temporal (Top {top_n} causas)...")

        # Filtrar datos
        df_filtrado = self.df[
            (self.df['location_name'] == ubicacion) &
            (self.df['sex_name'] == sexo) &
            (self.df['age_name'] == edad)
        ].copy()

        # Obtener top causas
        total_por_causa = df_filtrado.groupby('cause_name')['val'].sum().sort_values(ascending=False)
        top_causas = total_por_causa.head(top_n).index.tolist()

        # Filtrar y pivotar
        df_top = df_filtrado[df_filtrado['cause_name'].isin(top_causas)]
        pivot_data = df_top.pivot_table(values='val', index='cause_name', columns='year', aggfunc='mean')
        pivot_data = pivot_data.reindex(top_causas)

        # Crear heatmap
        fig, ax = plt.subplots(figsize=(14, 10))

        sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd',
                   linewidths=0.5, cbar_kws={'label': 'DALYs'}, ax=ax)

        ax.set_title(f'Mapa de Calor: Evolución Temporal de DALYs - Top {top_n} Causas\n{ubicacion} - {sexo} - {edad}',
                    fontsize=15, fontweight='bold', pad=20)
        ax.set_xlabel('Año', fontsize=13, fontweight='bold')
        ax.set_ylabel('Causa', fontsize=13, fontweight='bold')

        plt.tight_layout()

        # Guardar
        nombre_archivo = f"heatmap_top{top_n}_{ubicacion.replace(' ', '_')}_{sexo}_{edad.replace(' ', '_')}.png"
        ruta = self.carpeta_graficos / nombre_archivo
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico guardado: {ruta}")
        plt.close()

        return pivot_data

    def generar_reporte_completo(self, ubicacion="Global", año_ranking=None):
        """
        Genera un reporte completo con todos los gráficos

        Args:
            ubicacion: Ubicación geográfica para el análisis
            año_ranking: Año específico para los rankings (None = promedio)
        """
        print("\n" + "="*60)
        print("GENERANDO REPORTE COMPLETO DE ANÁLISIS GBD")
        print("="*60)

        # 1. Evolución temporal top 10
        self.evolucion_temporal_top_causas(top_n=10, ubicacion=ubicacion)

        # 2. Ranking general
        self.ranking_causas(año=año_ranking, top_n=20, ubicacion=ubicacion)

        # 3. Comparación por sexo
        self.comparacion_por_sexo(top_n=15, ubicacion=ubicacion, año=año_ranking)

        # 4. Heatmap
        self.heatmap_causas_años(top_n=15, ubicacion=ubicacion)

        print("\n" + "="*60)
        print("✓ REPORTE COMPLETO GENERADO")
        print(f"✓ Todos los gráficos guardados en: {self.carpeta_graficos}/")
        print("="*60 + "\n")


def main():
    """Función principal"""
    # Archivo de datos - detecta si se ejecuta desde src/ o desde raíz
    if Path.cwd().name == 'src':
        archivo_csv = "../data/gbd_all_dalys_1423.csv"
    else:
        archivo_csv = "data/gbd_all_dalys_1423.csv"

    # Crear analizador
    analizador = AnalizadorGBD(archivo_csv)

    # Generar reporte completo
    analizador.generar_reporte_completo(ubicacion="Global", año_ranking=2017)

    # Ejemplos adicionales de uso:
    # analizador.evolucion_temporal_top_causas(top_n=15, ubicacion="Global")
    # analizador.ranking_causas(año=2020, top_n=25, ubicacion="Global")
    # analizador.comparacion_por_sexo(top_n=20, ubicacion="Global", año=2020)
    # analizador.heatmap_causas_años(top_n=20, ubicacion="Global")


if __name__ == "__main__":
    main()
