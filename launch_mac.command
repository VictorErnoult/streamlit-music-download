#!/bin/bash

# Ginette la Cassette - Launcher Script
# Double-click this file to run the app

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📼 Ginette la Cassette 🎅"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Python package is installed
python_package_installed() {
    python3 -c "import $1" >/dev/null 2>&1
}

# Check for Homebrew (macOS package manager)
if ! command_exists brew; then
    echo -e "${YELLOW}⚠️  Homebrew n'est pas installé.${NC}"
    echo ""
    echo "Homebrew est nécessaire pour installer ffmpeg automatiquement."
    echo ""
    echo "Installation de Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    
    if ! command_exists brew; then
        echo -e "${RED}❌ Échec de l'installation de Homebrew.${NC}"
        echo "Installe Homebrew manuellement depuis https://brew.sh"
        echo ""
        read -p "Appuie sur Entrée pour quitter..."
        exit 1
    fi
    echo -e "${GREEN}✅ Homebrew installé avec succès${NC}"
    echo ""
fi

# Check for Python 3
if ! command_exists python3; then
    echo -e "${YELLOW}⚠️  Python 3 n'est pas installé.${NC}"
    echo "Installation de Python 3 via Homebrew..."
    brew install python3
    
    if ! command_exists python3; then
        echo -e "${RED}❌ Échec de l'installation de Python 3.${NC}"
        echo ""
        read -p "Appuie sur Entrée pour quitter..."
        exit 1
    fi
    echo -e "${GREEN}✅ Python 3 installé avec succès${NC}"
    echo ""
fi

# Check for ffmpeg
if ! command_exists ffmpeg; then
    echo -e "${YELLOW}⚠️  ffmpeg n'est pas installé.${NC}"
    echo "Installation de ffmpeg via Homebrew..."
    brew install ffmpeg
    
    if ! command_exists ffmpeg; then
        echo -e "${RED}❌ Échec de l'installation de ffmpeg.${NC}"
        echo ""
        read -p "Appuie sur Entrée pour quitter..."
        exit 1
    fi
    echo -e "${GREEN}✅ ffmpeg installé avec succès${NC}"
    echo ""
fi

# Check for pip
if ! command_exists pip3; then
    echo -e "${YELLOW}⚠️  pip3 n'est pas disponible.${NC}"
    echo "Installation de pip..."
    python3 -m ensurepip --upgrade
    
    if ! command_exists pip3; then
        echo -e "${RED}❌ Échec de l'installation de pip.${NC}"
        echo ""
        read -p "Appuie sur Entrée pour quitter..."
        exit 1
    fi
    echo -e "${GREEN}✅ pip installé avec succès${NC}"
    echo ""
fi

# Install/Update Python dependencies
echo -e "${BLUE}📦 Vérification des dépendances Python...${NC}"

# Check if streamlit is installed
if ! python_package_installed streamlit; then
    echo "Installation des dépendances Python..."
    pip3 install -r requirements.txt --quiet
    echo -e "${GREEN}✅ Dépendances Python installées${NC}"
else
    # Check if requirements need updating
    pip3 install -r requirements.txt --quiet --upgrade 2>/dev/null
    echo -e "${GREEN}✅ Dépendances Python à jour${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Tout est prêt !${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 Lancement de l'application..."
echo ""
echo "L'application va s'ouvrir dans ton navigateur."
echo "Pour arrêter l'application, ferme cette fenêtre."
echo ""

# Launch Streamlit
python3 -m streamlit run app.py --server.headless true

# Keep terminal open if there's an error
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ L'application a rencontré une erreur.${NC}"
    echo ""
    read -p "Appuie sur Entrée pour quitter..."
fi

