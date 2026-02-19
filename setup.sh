#!/bin/bash
# Setup script for Deyem Lead Bot

echo "🤖 Deyem Project Lead Bot - Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trovato. Installalo prima:"
    echo "   sudo apt-get install python3 python3-pip"
    exit 1
fi

echo "✅ Python trovato"

# Install dependencies
echo ""
echo "📦 Installazione dipendenze..."
pip3 install -r requirements.txt

# Create leads.json if not exists
if [ ! -f "leads.json" ]; then
    touch leads.json
    echo "✅ File leads.json creato"
fi

echo ""
echo "📝 Configurazione token..."
echo ""
echo "1. Vai su @BotFather su Telegram"
echo "2. Crea un nuovo bot: /newbot"
echo "3. Scegli nome: Deyem Project"
echo "4. Scegli username: deyemproject_bot"
echo "5. Copia il token che ti dà"
echo ""
read -p "Incolla il token qui: " TOKEN

# Update bot.py with token
sed -i "s/BOT_TOKEN = \"YOUR_BOT_TOKEN_HERE\"/BOT_TOKEN = \"$TOKEN\"/" bot.py

echo ""
echo "✅ Setup completato!"
echo ""
echo "Per avviare il bot:"
echo "   python3 bot.py"
echo ""
echo "👾 Buona caccia ai lead!"