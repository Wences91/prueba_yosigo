#!/bin/bash
# Script para ejecutar el análisis personalizado de GBD

echo "============================================"
echo "   Análisis Personalizado de Datos GBD"
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

echo "Para personalizar el análisis, edita el archivo:"
echo "  src/analisis_personalizado.py"
echo ""
echo "Ejecutando análisis personalizado..."
echo ""

# Ejecutar análisis personalizado
python3 src/analisis_personalizado.py

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "✓ ANÁLISIS COMPLETADO"
    echo "============================================"
    echo ""
    echo "Los gráficos se han guardado en: output/graficos/"
    echo ""
else
    echo ""
    echo "❌ Error durante la ejecución del análisis"
    exit 1
fi
