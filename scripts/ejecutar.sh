#!/bin/bash
# Script para ejecutar el análisis GBD

echo "============================================"
echo "   Ejecutando Análisis de Datos GBD"
echo "============================================"
echo ""

# Ir a la raíz del proyecto
cd "$(dirname "$0")/.." || exit

# Verificar que existe el archivo de datos
if [ ! -f "data/gbd_all_dalys_1423.csv" ]; then
    echo "❌ Error: No se encuentra el archivo de datos"
    echo "   Asegúrate de que data/gbd_all_dalys_1423.csv existe"
    exit 1
fi

# Ejecutar análisis
python3 src/analisis_gbd.py

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "✓ ANÁLISIS COMPLETADO"
    echo "============================================"
    echo ""
    echo "Los gráficos se han guardado en: output/graficos/"
    echo ""
    echo "Para ver los gráficos:"
    if command -v xdg-open &> /dev/null; then
        echo "  xdg-open output/graficos/"
    elif command -v open &> /dev/null; then
        echo "  open output/graficos/"
    else
        echo "  Abre la carpeta output/graficos/ en tu explorador de archivos"
    fi
    echo ""
else
    echo ""
    echo "❌ Error durante la ejecución del análisis"
    exit 1
fi
