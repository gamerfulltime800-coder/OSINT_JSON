import os
import json
import re
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters,
    ConversationHandler, CallbackContext
)

# ==================== CONFIGURATION ====================
BOT_TOKEN = "8519013928:AAF5veC4-eA-JSdh2nPIsFoWvFGSyC7N5O8"
# =======================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Conversation states
(
    NAME, NUMBER, COUNTRY, COUNTRY_CODE, LOCATION, 
    PLACE, ADDRESS, UPI_ID, TELEGRAM_NUMBER, WHATSAPP_NUMBER,
    AGE, INSTAGRAM, FACEBOOK, X, TELEGRAM_USERNAME, 
    SIM_CARRIER, CONFIRM
) = range(17)

user_data = {}

class OSINTDataCollector:
    def __init__(self):
        self.data_template = {
            "name": "", "number": "", "country": "", "country_code": "",
            "location": "", "place": "", "address": "", "upi_id": "",
            "telegram_number": "", "whatsapp_number": "", "age": "",
            "instagram": "", "facebook": "", "x": "", "telegram": "",
            "sim_carrier": "", "timestamp": ""
        }

    def validate_phone(self, phone):
        if phone.lower() == 'skip': return True
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        return re.match(r'^\+?[0-9]+$', cleaned) is not None

    def validate_age(self, age):
        if age.lower() == 'skip': return True
        try: return 1 <= int(age) <= 120
        except ValueError: return False

    def format_json(self, data):
        result = self.data_template.copy()
        result.update(data)
        result["timestamp"] = datetime.now().isoformat()
        return json.dumps(result, indent=2, ensure_ascii=False)

def start(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id] = {}
    
    update.message.reply_text(
        "🕵️ **Advanced OSINT Data Collection Bot**\n\n"
        "I'll help you collect OSINT information and format it as JSON.\n\n"
        "Type 'skip' for optional fields.\n\n"
        "**What is the person's full name?**",
        parse_mode='Markdown'
    )
    return NAME

def get_name(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id]["name"] = update.message.text
    update.message.reply_text("📞 **Phone Number:**\nEnter primary phone number (or 'skip'):")
    return NUMBER

def get_number(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    text = update.message.text
    collector = OSINTDataCollector()
    if text.lower() != 'skip' and not collector.validate_phone(text):
        update.message.reply_text("❌ Invalid phone number. Enter valid number or 'skip':")
        return NUMBER
    user_data[user_id]["number"] = text if text.lower() != 'skip' else "Not provided"
    update.message.reply_text("🌍 **Country:**\nEnter country name:")
    return COUNTRY

def get_country(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id]["country"] = update.message.text
    update.message.reply_text("🇺🇸 **Country Code:**\nEnter code (e.g., US, IN, UK):")
    return COUNTRY_CODE

def get_country_code(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id]["country_code"] = update.message.text.upper()
    update.message.reply_text("📍 **Location:**\nEnter city/state/region:")
    return LOCATION

def get_location(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id]["location"] = update.message.text
    update.message.reply_text("🏢 **Place:**\nEnter workplace/institution:")
    return PLACE

def get_place(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id]["place"] = update.message.text
    update.message.reply_text("🏠 **Address:**\nEnter full address (or 'skip'):")
    return ADDRESS

def get_address(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id]["address"] = update.message.text if update.message.text.lower() != 'skip' else "Not provided"
    update.message.reply_text("💳 **UPI ID:**\nEnter UPI ID (or 'skip'):")
    return UPI_ID

def get_upi_id(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id]["upi_id"] = update.message.text if update.message.text.lower() != 'skip' else "Not provided"
    update.message.reply_text("📱 **Telegram Number:**\nEnter Telegram number (or 'skip'):")
    return TELEGRAM_NUMBER

def get_telegram_number(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    text = update.message.text
    collector = OSINTDataCollector()
    if text.lower() != 'skip' and not collector.validate_phone(text):
        update.message.reply_text("❌ Invalid number. Enter valid number or 'skip':")
        return TELEGRAM_NUMBER
    user_data[user_id]["telegram_number"] = text if text.lower() != 'skip' else "Not provided"
    update.message.reply_text("💬 **WhatsApp Number:**\nEnter WhatsApp number (or 'skip'):")
    return WHATSAPP_NUMBER

def get_whatsapp_number(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    text = update.message.text
    collector = OSINTDataCollector()
    if text.lower() != 'skip' and not collector.validate_phone(text):
        update.message.reply_text("❌ Invalid number. Enter valid number or 'skip':")
        return WHATSAPP_NUMBER
    user_data[user_id]["whatsapp_number"] = text if text.lower() != 'skip' else "Not provided"
    update.message.reply_text("🎂 **Age:**\nEnter age (or 'skip'):")
    return AGE

def get_age(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    text = update.message.text
    collector = OSINTDataCollector()
    if text.lower() != 'skip' and not collector.validate_age(text):
        update.message.reply_text("❌ Invalid age (1-120). Enter valid age or 'skip':")
        return AGE
    user_data[user_id]["age"] = text if text.lower() != 'skip' else "Not provided"
    update.message.reply_text("📷 **Instagram:**\nEnter username (or 'skip'):")
    return INSTAGRAM

def get_instagram(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id]["instagram"] = update.message.text if update.message.text.lower() != 'skip' else "Not provided"
    update.message.reply_text("👥 **Facebook:**\nEnter profile URL/username (or 'skip'):")
    return FACEBOOK

def get_facebook(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id]["facebook"] = update.message.text if update.message.text.lower() != 'skip' else "Not provided"
    update.message.reply_text("🐦 **X (Twitter):**\nEnter username (or 'skip'):")
    return X

def get_x(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id]["x"] = update.message.text if update.message.text.lower() != 'skip' else "Not provided"
    update.message.reply_text("✈️ **Telegram Username:**\nEnter username without @ (or 'skip'):")
    return TELEGRAM_USERNAME

def get_telegram_username(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    text = update.message.text
    if text.lower() != 'skip' and text.startswith('@'):
        text = text[1:]
    user_data[user_id]["telegram"] = text if text.lower() != 'skip' else "Not provided"
    update.message.reply_text("📶 **SIM Carrier:**\nEnter mobile carrier (or 'skip'):")
    return SIM_CARRIER

def get_sim_carrier(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id]["sim_carrier"] = update.message.text if update.message.text.lower() != 'skip' else "Not provided"
    
    collector = OSINTDataCollector()
    preview_json = collector.format_json(user_data[user_id])
    
    summary = create_data_summary(user_data[user_id])
    
    update.message.reply_text(
        f"📋 **Data Summary:**\n{summary}\n\n"
        "Type 'confirm' to save as JSON or 'cancel' to start over:",
        parse_mode='Markdown'
    )
    return CONFIRM

def create_data_summary(data):
    summary_lines = []
    fields = [
        ("Name", "name"), ("Phone", "number"), ("Country", "country"),
        ("Location", "location"), ("Age", "age"), ("Telegram", "telegram"),
        ("Instagram", "instagram"), ("X", "x"), ("SIM Carrier", "sim_carrier")
    ]
    
    for display_name, field_name in fields:
        value = data.get(field_name, "Not provided")
        if value and value != "Not provided":
            summary_lines.append(f"• {display_name}: {value}")
    
    return "\n".join(summary_lines) if summary_lines else "No data provided"

def confirm_data(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    
    if update.message.text.lower() == 'confirm':
        collector = OSINTDataCollector()
        final_json = collector.format_json(user_data[user_id])
        
        filename = f"osint_data_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        update.message.reply_document(
            document=final_json.encode('utf-8'),
            filename=filename,
            caption="✅ **OSINT data saved as JSON!**\nUse /start for new data.",
            parse_mode='Markdown'
        )
        
        if user_id in user_data:
            del user_data[user_id]
        return ConversationHandler.END
    else:
        if user_id in user_data:
            del user_data[user_id]
        update.message.reply_text("❌ Cancelled. Use /start to begin.")
        return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if user_id in user_data:
        del user_data[user_id]
    update.message.reply_text("❌ Cancelled. Use /start to begin.")
    return ConversationHandler.END

def help_command(update: Update, context: CallbackContext):
    help_text = """
🕵️ **OSINT Data Collection Bot**

**Commands:**
/start - Start collecting data
/help - Show this message
/cancel - Cancel current collection

Type 'skip' for optional fields.
"""
    update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Start the bot."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            NUMBER: [MessageHandler(Filters.text & ~Filters.command, get_number)],
            COUNTRY: [MessageHandler(Filters.text & ~Filters.command, get_country)],
            COUNTRY_CODE: [MessageHandler(Filters.text & ~Filters.command, get_country_code)],
            LOCATION: [MessageHandler(Filters.text & ~Filters.command, get_location)],
            PLACE: [MessageHandler(Filters.text & ~Filters.command, get_place)],
            ADDRESS: [MessageHandler(Filters.text & ~Filters.command, get_address)],
            UPI_ID: [MessageHandler(Filters.text & ~Filters.command, get_upi_id)],
            TELEGRAM_NUMBER: [MessageHandler(Filters.text & ~Filters.command, get_telegram_number)],
            WHATSAPP_NUMBER: [MessageHandler(Filters.text & ~Filters.command, get_whatsapp_number)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, get_age)],
            INSTAGRAM: [MessageHandler(Filters.text & ~Filters.command, get_instagram)],
            FACEBOOK: [MessageHandler(Filters.text & ~Filters.command, get_facebook)],
            X: [MessageHandler(Filters.text & ~Filters.command, get_x)],
            TELEGRAM_USERNAME: [MessageHandler(Filters.text & ~Filters.command, get_telegram_username)],
            SIM_CARRIER: [MessageHandler(Filters.text & ~Filters.command, get_sim_carrier)],
            CONFIRM: [MessageHandler(Filters.text & ~Filters.command, confirm_data)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('cancel', cancel))

    print("🤖 Starting bot with stable version...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
