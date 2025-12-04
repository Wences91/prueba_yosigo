#!/bin/bash
# Script de instalación para el proyecto de análisis GBD

echo "============================================"
echo "   INSTALACIÓN - Análisis de Datos GBD"
echo "============================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "   Por favor, instala Python 3.8 o superior"
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"
echo ""

# Verificar pip
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip no está instalado"
    echo "   Por favor, instala pip"
    exit 1
fi

echo "✓ pip encontrado"
echo ""

# Instalar dependencias
echo "📦 Instalando dependencias..."
echo ""

if pip3 install -r requirements.txt; then
    echo ""
    echo "============================================"
    echo "✓ INSTALACIÓN COMPLETADA CON ÉXITO"
    echo "============================================"
    echo ""
    echo "Para ejecutar el análisis, usa:"
    echo "  bash scripts/ejecutar.sh"
    echo ""
else
    echo ""
    echo "❌ Error durante la instalación"
    exit 1
fi
