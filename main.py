# Import required libraries
import json
import re
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# ==================== BOT CONFIGURATION ====================
# REPLACE THIS WITH YOUR BOT TOKEN FROM @BotFather
BOT_TOKEN = "8519013928:AAF5veC4-eA-JSdh2nPIsFoWvFGSyC7N5O8"
# ===========================================================

# Define conversation steps - each number represents a different question
NAME, NUMBER, COUNTRY, COUNTRY_CODE, LOCATION, PLACE, ADDRESS = range(7)
UPI_ID, TELEGRAM_NUMBER, WHATSAPP_NUMBER, AGE, INSTAGRAM = range(7, 12)
FACEBOOK, X, TELEGRAM_USERNAME, SIM_CARRIER, CONFIRM = range(12, 17)

# Store user data temporarily
user_data = {}

def start(update, context):
    """Handler for /start command"""
    user_id = update.message.from_user.id
    user_data[user_id] = {}  # Create empty storage for this user
    
    welcome_message = """
🕵️ **OSINT Data Collection Bot**

I will help you collect information and save it as a JSON file.

**We will collect:**
• Basic Info (Name, Age, Location)
• Contact Details (Phone, Email, Social Media)
• Additional Info (Address, Work, Carrier)

Type 'skip' for any field you want to leave empty.

**What is the person's full name?**
    """
    
    update.message.reply_text(welcome_message, parse_mode='Markdown')
    return NAME

def get_name(update, context):
    """Get person's name"""
    user_id = update.message.from_user.id
    user_data[user_id]["name"] = update.message.text
    
    update.message.reply_text(
        "📞 **Phone Number**\n"
        "Enter primary phone number:\n"
        "(Type 'skip' if unknown)"
    )
    return NUMBER

def get_number(update, context):
    """Get phone number"""
    user_id = update.message.from_user.id
    text = update.message.text
    
    if text.lower() != 'skip':
        # Simple phone validation
        cleaned = re.sub(r'[\s\-\(\)]', '', text)
        if not re.match(r'^\+?[0-9]+$', cleaned):
            update.message.reply_text("❌ Please enter a valid phone number or type 'skip':")
            return NUMBER
    
    user_data[user_id]["number"] = text if text.lower() != 'skip' else "Not provided"
    update.message.reply_text("🌍 **Country**\nEnter country name:")
    return COUNTRY

def get_country(update, context):
    """Get country"""
    user_id = update.message.from_user.id
    user_data[user_id]["country"] = update.message.text
    update.message.reply_text("🇺🇸 **Country Code**\nEnter code (e.g., US, IN, UK):")
    return COUNTRY_CODE

def get_country_code(update, context):
    """Get country code"""
    user_id = update.message.from_user.id
    user_data[user_id]["country_code"] = update.message.text.upper()
    update.message.reply_text("📍 **Location**\nEnter city/state:")
    return LOCATION

def get_location(update, context):
    """Get location"""
    user_id = update.message.from_user.id
    user_data[user_id]["location"] = update.message.text
    update.message.reply_text("🏢 **Place**\nEnter workplace or institution:")
    return PLACE

def get_place(update, context):
    """Get workplace"""
    user_id = update.message.from_user.id
    user_data[user_id]["place"] = update.message.text
    update.message.reply_text("🏠 **Address**\nEnter full address (or 'skip'):")
    return ADDRESS

def get_address(update, context):
    """Get address"""
    user_id = update.message.from_user.id
    user_data[user_id]["address"] = update.message.text if update.message.text.lower() != 'skip' else "Not provided"
    update.message.reply_text("💳 **UPI ID**\nEnter UPI ID like name@bank (or 'skip'):")
    return UPI_ID

def get_upi_id(update, context):
    """Get UPI ID"""
    user_id = update.message.from_user.id
    user_data[user_id]["upi_id"] = update.message.text if update.message.text.lower() != 'skip' else "Not provided"
    update.message.reply_text("📱 **Telegram Number**\nEnter Telegram number (or 'skip'):")
    return TELEGRAM_NUMBER

def get_telegram_number(update, context):
    """Get Telegram number"""
    user_id = update.message.from_user.id
    text = update.message.text
    
    if text.lower() != 'skip':
        cleaned = re.sub(r'[\s\-\(\)]', '', text)
        if not re.match(r'^\+?[0-9]+$', cleaned):
            update.message.reply_text("❌ Please enter valid number or 'skip':")
            return TELEGRAM_NUMBER
    
    user_data[user_id]["telegram_number"] = text if text.lower() != 'skip' else "Not provided"
    update.message.reply_text("💬 **WhatsApp Number**\nEnter WhatsApp number (or 'skip'):")
    return WHATSAPP_NUMBER

def get_whatsapp_number(update, context):
    """Get WhatsApp number"""
    user_id = update.message.from_user.id
    text = update.message.text
    
    if text.lower() != 'skip':
        cleaned = re.sub(r'[\s\-\(\)]', '', text)
        if not re.match(r'^\+?[0-9]+$', cleaned):
            update.message.reply_text("❌ Please enter valid number or 'skip':")
            return WHATSAPP_NUMBER
    
    user_data[user_id]["whatsapp_number"] = text if text.lower() != 'skip' else "Not provided"
    update.message.reply_text("🎂 **Age**\nEnter age (or 'skip'):")
    return AGE

def get_age(update, context):
    """Get age"""
    user_id = update.message.from_user.id
    text = update.message.text
    
    if text.lower() != 'skip':
        try:
            age = int(text)
            if not (1 <= age <= 120):
                update.message.reply_text("❌ Age must be 1-120. Enter valid age or 'skip':")
                return AGE
        except ValueError:
            update.message.reply_text("❌ Please enter a number or 'skip':")
            return AGE
    
    user_data[user_id]["age"] = text if text.lower() != 'skip' else "Not provided"
    update.message.reply_text("📷 **Instagram**\nEnter username (or 'skip'):")
    return INSTAGRAM

def get_instagram(update, context):
    """Get Instagram"""
    user_id = update.message.from_user.id
    user_data[user_id]["instagram"] = update.message.text if update.message.text.lower() != 'skip' else "Not provided"
    update.message.reply_text("👥 **Facebook**\nEnter profile URL/username (or 'skip'):")
    return FACEBOOK

def get_facebook(update, context):
    """Get Facebook"""
    user_id = update.message.from_user.id
    user_data[user_id]["facebook"] = update.message.text if update.message.text.lower() != 'skip' else "Not provided"
    update.message.reply_text("🐦 **X (Twitter)**\nEnter username (or 'skip'):")
    return X

def get_x(update, context):
    """Get X/Twitter"""
    user_id = update.message.from_user.id
    user_data[user_id]["x"] = update.message.text if update.message.text.lower() != 'skip' else "Not provided"
    update.message.reply_text("✈️ **Telegram Username**\nEnter username without @ (or 'skip'):")
    return TELEGRAM_USERNAME

def get_telegram_username(update, context):
    """Get Telegram username"""
    user_id = update.message.from_user.id
    text = update.message.text
    if text.lower() != 'skip' and text.startswith('@'):
        text = text[1:]  # Remove @ if present
    user_data[user_id]["telegram"] = text if text.lower() != 'skip' else "Not provided"
    update.message.reply_text("📶 **SIM Carrier**\nEnter mobile carrier like Airtel, Jio (or 'skip'):")
    return SIM_CARRIER

def get_sim_carrier(update, context):
    """Get SIM carrier and show preview"""
    user_id = update.message.from_user.id
    user_data[user_id]["sim_carrier"] = update.message.text if update.message.text.lower() != 'skip' else "Not provided"
    
    # Add timestamp
    user_data[user_id]["timestamp"] = datetime.now().isoformat()
    
    # Create summary
    summary = "**Collected Data Summary:**\n"
    for field in ["name", "number", "country", "location", "age", "telegram", "instagram", "sim_carrier"]:
        value = user_data[user_id].get(field, "Not provided")
        if value != "Not provided":
            summary += f"• {field.title()}: {value}\n"
    
    # Show JSON preview
    json_data = json.dumps(user_data[user_id], indent=2, ensure_ascii=False)
    
    update.message.reply_text(
        f"{summary}\n"
        "**JSON Preview:**\n"
        f"```json\n{json_data}\n```\n\n"
        "Type **'confirm'** to save as JSON file or **'cancel'** to start over:",
        parse_mode='Markdown'
    )
    return CONFIRM

def confirm_data(update, context):
    """Final confirmation and save data"""
    user_id = update.message.from_user.id
    
    if update.message.text.lower() == 'confirm':
        # Create JSON file
        json_data = json.dumps(user_data[user_id], indent=2, ensure_ascii=False)
        filename = f"osint_data_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Send JSON file to user
        update.message.reply_document(
            document=json_data.encode('utf-8'),
            filename=filename,
            caption="✅ **Data saved successfully!**\nUse /start to collect new data.",
            parse_mode='Markdown'
        )
        
        # Clean up
        if user_id in user_data:
            del user_data[user_id]
            
        return ConversationHandler.END
    else:
        # Cancel operation
        if user_id in user_data:
            del user_data[user_id]
        
        update.message.reply_text(
            "❌ Operation cancelled.\n\n"
            "Use /start to begin new data collection."
        )
        return ConversationHandler.END

def cancel(update, context):
    """Cancel the conversation"""
    user_id = update.message.from_user.id
    if user_id in user_data:
        del user_data[user_id]
    
    update.message.reply_text(
        "❌ Data collection cancelled.\n\n"
        "Use /start when you're ready to begin."
    )
    return ConversationHandler.END

def help_command(update, context):
    """Show help message"""
    help_text = """
🤖 **OSINT Data Collection Bot**

**Available Commands:**
/start - Begin data collection
/help - Show this help message
/cancel - Cancel current operation

**How to use:**
1. Type /start to begin
2. Answer each question
3. Type 'skip' for unknown fields
4. Type 'confirm' to save data
5. Receive JSON file with all information

**All data is processed securely and temporarily.**
    """
    update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Main function to start the bot"""
    print("🚀 Starting OSINT Telegram Bot...")
    
    try:
        # Create bot instance
        updater = Updater(BOT_TOKEN, use_context=True)
        
        # Create conversation handler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                NAME: [MessageHandler(Filters.text, get_name)],
                NUMBER: [MessageHandler(Filters.text, get_number)],
                COUNTRY: [MessageHandler(Filters.text, get_country)],
                COUNTRY_CODE: [MessageHandler(Filters.text, get_country_code)],
                LOCATION: [MessageHandler(Filters.text, get_location)],
                PLACE: [MessageHandler(Filters.text, get_place)],
                ADDRESS: [MessageHandler(Filters.text, get_address)],
                UPI_ID: [MessageHandler(Filters.text, get_upi_id)],
                TELEGRAM_NUMBER: [MessageHandler(Filters.text, get_telegram_number)],
                WHATSAPP_NUMBER: [MessageHandler(Filters.text, get_whatsapp_number)],
                AGE: [MessageHandler(Filters.text, get_age)],
                INSTAGRAM: [MessageHandler(Filters.text, get_instagram)],
                FACEBOOK: [MessageHandler(Filters.text, get_facebook)],
                X: [MessageHandler(Filters.text, get_x)],
                TELEGRAM_USERNAME: [MessageHandler(Filters.text, get_telegram_username)],
                SIM_CARRIER: [MessageHandler(Filters.text, get_sim_carrier)],
                CONFIRM: [MessageHandler(Filters.text, confirm_data)],
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )

        # Register handlers
        updater.dispatcher.add_handler(conv_handler)
        updater.dispatcher.add_handler(CommandHandler('help', help_command))
        updater.dispatcher.add_handler(CommandHandler('cancel', cancel))

        # Start the bot
        print("✅ Bot is running and ready!")
        print("📱 Go to Telegram and send /start to your bot")
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

# Start the bot when script runs
if __name__ == '__main__':
    main()
