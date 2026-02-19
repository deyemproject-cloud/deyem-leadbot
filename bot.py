import logging
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Will be set via env variable
ANDREA_CHAT_ID = "1425431994"  # Your Telegram ID

# Conversation states
(
    WELCOME,
    NAME,
    COMPANY,
    EMAIL,
    PHONE,
    SERVICE,
    BUDGET,
    TIMELINE,
    MESSAGE,
    CONFIRM
) = range(10)

# Service options
SERVICES = [
    "Content Creation",
    "Social Media Management", 
    "Brand Identity",
    "Video Production",
    "AI Automation",
    "Full Marketing Package"
]

# Budget ranges
BUDGETS = [
    "€300-500/mese",
    "€500-1000/mese",
    "€1000-2000/mese",
    "€2000+/mese",
    "Da definire"
]

# Timeline options
TIMELINES = [
    " immediatamente",
    "Entro 1 mese",
    "Entro 3 mesi",
    "Solo informazioni"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation."""
    welcome_text = """
🎬 **Benvenuto in Deyem Project!**

Sono Jarvis, l'AI assistant di Andrea. Sono qui per capire come possiamo aiutarti a far crescere il tuo business con contenuti di alta qualità.

Questo prenderà solo **2 minuti**.

Pronto per iniziare? 👇
"""
    
    keyboard = [[InlineKeyboardButton("🚀 Inizia", callback_data="start_survey")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return WELCOME

async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Begin the survey after button click."""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "Perfetto! Iniziamo 💪\n\n"
        "**Step 1/8** - Come ti chiami?",
        parse_mode='Markdown'
    )
    
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get user's name."""
    context.user_data['name'] = update.message.text
    
    await update.message.reply_text(
        f"Piacere di conoscerti, {update.message.text}! 👋\n\n"
        "**Step 2/8** - Per quale azienda lavori?\n"
        "(o il tuo nome se sei un freelancer)",
        parse_mode='Markdown'
    )
    
    return COMPANY

async def get_company(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get company name."""
    context.user_data['company'] = update.message.text
    
    await update.message.reply_text(
        "**Step 3/8** - Qual è la tua email? 📧\n"
        "(Ti contatteremo qui per seguire la tua richiesta)",
        parse_mode='Markdown'
    )
    
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get email address."""
    email = update.message.text
    # Basic email validation
    if '@' not in email or '.' not in email:
        await update.message.reply_text(
            "⚠️ Sembra che l'email non sia valida.\n"
            "Per favore inserisci un'email corretta:"
        )
        return EMAIL
    
    context.user_data['email'] = email
    
    keyboard = [[InlineKeyboardButton("⏭️ Salta", callback_data="skip_phone")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "**Step 4/8** - Numero di telefono? 📱\n"
        "(Opzionale, ma utile per call veloci)",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return PHONE

async def skip_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skip phone number."""
    query = update.callback_query
    await query.answer()
    
    context.user_data['phone'] = "Non fornito"
    
    return await ask_service(query, context)

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get phone number."""
    context.user_data['phone'] = update.message.text
    
    return await ask_service(update.message, context)

async def ask_service(target, context: ContextTypes.DEFAULT_TYPE):
    """Ask for service type."""
    keyboard = [[InlineKeyboardButton(service, callback_data=f"service_{i}")] 
                for i, service in enumerate(SERVICES)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "**Step 5/8** - Di quale servizio hai bisogno? 🎯"
    
    if hasattr(target, 'reply_text'):
        await target.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await target.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    return SERVICE

async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get selected service."""
    query = update.callback_query
    await query.answer()
    
    service_idx = int(query.data.split('_')[1])
    context.user_data['service'] = SERVICES[service_idx]
    
    keyboard = [[InlineKeyboardButton(budget, callback_data=f"budget_{i}")] 
                for i, budget in enumerate(BUDGETS)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "**Step 6/8** - Qual è il tuo budget mensile stimato? 💰",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return BUDGET

async def get_budget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get budget range."""
    query = update.callback_query
    await query.answer()
    
    budget_idx = int(query.data.split('_')[1])
    context.user_data['budget'] = BUDGETS[budget_idx]
    
    keyboard = [[InlineKeyboardButton(timeline, callback_data=f"timeline_{i}")] 
                for i, timeline in enumerate(TIMELINES)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "**Step 7/8** - Quando vorresti iniziare? ⏰",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return TIMELINE

async def get_timeline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get timeline."""
    query = update.callback_query
    await query.answer()
    
    timeline_idx = int(query.data.split('_')[1])
    context.user_data['timeline'] = TIMELINES[timeline_idx]
    
    await query.edit_message_text(
        "**Step 8/8** - Hai qualche informazione aggiuntiva da condividere?\n\n"
        "Descrivi brevemente il tuo progetto o le tue esigenze specifiche:",
        parse_mode='Markdown'
    )
    
    return MESSAGE

async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get additional message."""
    context.user_data['message'] = update.message.text
    
    # Show summary
    summary = f"""
📋 **Riepilogo della tua richiesta:**

👤 **Nome:** {context.user_data['name']}
🏢 **Azienda:** {context.user_data['company']}
📧 **Email:** {context.user_data['email']}
📱 **Telefono:** {context.user_data['phone']}
🎯 **Servizio:** {context.user_data['service']}
💰 **Budget:** {context.user_data['budget']}
⏰ **Timeline:** {context.user_data['timeline']}
📝 **Note:** {context.user_data['message']}

Tutto corretto?
"""
    
    keyboard = [
        [InlineKeyboardButton("✅ Conferma", callback_data="confirm")],
        [InlineKeyboardButton("🔄 Ricomincia", callback_data="restart")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        summary,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return CONFIRM

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle confirmation."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "confirm":
        # Save lead data
        lead_data = {
            'timestamp': datetime.now().isoformat(),
            **context.user_data
        }
        
        # Save to JSON file
        try:
            with open('/data/.openclaw/workspace/deyem-leadbot/leads.json', 'a') as f:
                f.write(json.dumps(lead_data) + '\n')
        except Exception as e:
            logger.error(f"Error saving lead: {e}")
        
        # Notify Andrea
        notification = f"""
🚨 **NUOVO LEAD!**

👤 {lead_data['name']} ({lead_data['company']})
📧 {lead_data['email']}
📱 {lead_data['phone']}
🎯 {lead_data['service']}
💰 {lead_data['budget']}
⏰ {lead_data['timeline']}

📝 {lead_data['message']}
"""
        
        try:
            await context.bot.send_message(
                chat_id=ANDREA_CHAT_ID,
                text=notification,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error notifying Andrea: {e}")
        
        # Thank user
        await query.edit_message_text(
            "🎉 **Grazie per la tua richiesta!**\n\n"
            "Ho inviato tutto ad Andrea. Ti contatteremo entro **24 ore** per discutere del tuo progetto.\n\n"
            "Nel frattempo, seguici su Instagram per vedere i nostri lavori!\n\n"
            "👾 *- Jarvis, Deyem Project AI*",
            parse_mode='Markdown'
        )
    else:
        await query.edit_message_text(
            "Nessun problema! Ricominciamo...\n\n"
            "/start per ricominciare"
        )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text(
        "❌ Conversazione annullata.\n\n"
        "Scrivi /start quando vuoi ricominciare!"
    )
    
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message."""
    help_text = """
🤖 **Comandi disponibili:**

/start - Inizia la richiesta
/cancel - Annulla conversazione
/help - Mostra questo messaggio

**Cosa faccio:**
• Raccolgo informazioni sui potenziali clienti
• Qualifico i lead (servizio, budget, timeline)
• Invio notifiche ad Andrea in tempo reale
• Salvo tutto in modo sicuro

Hai domande? Scrivi qui! 👇
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main() -> None:
    """Run the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WELCOME: [CallbackQueryHandler(start_survey, pattern='^start_survey$')],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            COMPANY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_company)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            PHONE: [
                CallbackQueryHandler(skip_phone, pattern='^skip_phone$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)
            ],
            SERVICE: [CallbackQueryHandler(get_service, pattern='^service_')],
            BUDGET: [CallbackQueryHandler(get_budget, pattern='^budget_')],
            TIMELINE: [CallbackQueryHandler(get_timeline, pattern='^timeline_')],
            MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_message)],
            CONFIRM: [CallbackQueryHandler(confirm, pattern='^(confirm|restart)$')],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()