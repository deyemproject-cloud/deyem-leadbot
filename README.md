# Deyem Project Lead Generation Bot 🤖

Bot Telegram per la raccolta e qualifica lead per Deyem Project.

## Features

✅ **Conversazione guidata** - 8 step per qualificare i lead
✅ **Raccolta dati** - Nome, azienda, email, telefono
✅ **Qualifica automatica** - Servizio, budget, timeline
✅ **Notifiche real-time** - Avvisi immediati su Telegram
✅ **Salvataggio dati** - JSON locale (facilmente esportabile)

## Setup

### 1. Crea il Bot su Telegram

1. Vai su [@BotFather](https://t.me/botfather)
2. Invia `/newbot`
3. Scegli nome: **Deyem Project**
4. Scegli username: **deyemproject_bot** (deve finire in _bot)
5. Copia il **TOKEN** che ti dà

### 2. Configura il Bot

```bash
# Installa dipendenze
pip install -r requirements.txt

# Setta il token
export DEYEM_BOT_TOKEN="il_tuo_token_qui"

# Oppure modifica direttamente bot.py (riga 25)
BOT_TOKEN = "il_tuo_token_qui"
```

### 3. Avvia il Bot

```bash
python bot.py
```

Il bot è ora attivo! 🎉

## Come funziona

### Per i Lead (utenti):
1. Trovano il bot su Telegram
2. Cliccano **Start** o scrivono `/start`
3. Completano il form (2 minuti)
4. Ricevono conferma

### Per te (Andrea):
1. Ricevi notifica istantanea su Telegram
2. Hai tutti i dati del lead
3. Puoi contattarli immediatamente

## Struttura Conversazione

1. **Benvenuto** - Introduzione al bot
2. **Nome** - Come ti chiami?
3. **Azienda** - Per chi lavori?
4. **Email** - Contatto principale
5. **Telefono** - Opzionale
6. **Servizio** - Dropdown con opzioni
7. **Budget** - Range mensile
8. **Timeline** - Quando iniziare?
9. **Messaggio** - Dettagli progetto
10. **Conferma** - Riepilogo e invio

## Customizzazione

### Modifica servizi offerti
```python
# In bot.py, riga 46
SERVICES = [
    "Content Creation",
    "Social Media Management",
    # Aggiungi/modifica qui
]
```

### Modifica budget range
```python
# In bot.py, riga 53
BUDGETS = [
    "€300-500/mese",
    # Modifica qui
]
```

### Cambia messaggi
Tutti i messaggi sono in italiano nel codice. Cerca le stringhe con `"""` e modifica.

## Esportazione Lead

I lead sono salvati in `leads.json` (un lead per riga):

```bash
# Visualizza ultimi 5 lead
tail -5 leads.json | python -m json.tool

# Esporta in CSV (richiede jq)
cat leads.json | jq -r '[.timestamp, .name, .company, .email, .service, .budget] | @csv' > leads.csv
```

## Deployment

### Opzione 1: VPS (Consigliato)
```bash
# Su un server sempre online
screen -S leadbot
python bot.py
# Ctrl+A+D per staccare
```

### Opzione 2: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY bot.py .
CMD ["python", "bot.py"]
```

### Opzione 3: Systemd Service
Crea `/etc/systemd/system/deyem-bot.service`:
```ini
[Unit]
Description=Deyem Lead Bot
After=network.target

[Service]
Type=simple
User=deyem
WorkingDirectory=/data/.openclaw/workspace/deyem-leadbot
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable deyem-bot
sudo systemctl start deyem-bot
```

## Integrazione Notion (Optional)

Per salvare automaticamente i lead in Notion:

1. Aggiungi questa funzione in `bot.py`:
```python
import requests

def save_to_notion(lead_data):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": "Bearer TUO_NOTION_TOKEN",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    # ... crea la richiesta
```

2. Chiama `save_to_notion()` in `confirm()`

## Troubleshooting

**Bot non risponde:**
- Controlla che il token sia corretto
- Verifica che non ci sia un altro bot in esecuzione

**Errori nel log:**
```bash
tail -f /var/log/deyem-bot.log
```

**Riavvia il bot:**
```bash
pkill -f "python bot.py"
python bot.py
```

## Supporto

Problemi? Scrivimi qui su Telegram! 👾

---

*Creato da JARVIS per Deyem Project*