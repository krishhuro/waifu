import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Replace 'YOUR_API_TOKEN' with your actual Telegram bot API token.
API_TOKEN = 'YOUR_API_TOKEN'

# Example character data (could be expanded)
characters = [
    {"name": "Waifu 1", "rarity": "Common", "image_url": "http://example.com/waifu1.jpg"},
    {"name": "Waifu 2", "rarity": "Rare", "image_url": "http://example.com/waifu2.jpg"},
    {"name": "Husbando 1", "rarity": "Epic", "image_url": "http://example.com/husbando1.jpg"},
    {"name": "Husbando 2", "rarity": "Common", "image_url": "http://example.com/husbando2.jpg"}
]

# User collection tracking (simple in-memory storage for demo purposes)
user_collection = {}

# Function to send random character with inline buttons
def send_random_character(update: Update, context: CallbackContext):
    character = random.choice(characters)
    keyboard = [
        [InlineKeyboardButton("Catch!", callback_data=character['name'])]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        f"A random character has appeared! \n\nName: {character['name']}\nRarity: {character['rarity']}",
        reply_markup=reply_markup
    )

# Function to handle character "catch" action
def catch_character(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    character_name = query.data  # This is the character's name

    # Add character to user's collection
    if user_id not in user_collection:
        user_collection[user_id] = []
    user_collection[user_id].append(character_name)

    # Acknowledge the action
    query.answer()
    query.edit_message_text(f"You have caught {character_name}!\nYour collection: {', '.join(user_collection[user_id])}")

# Function to display user's collection
def show_collection(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_collection or not user_collection[user_id]:
        update.message.reply_text("Your collection is empty!")
    else:
        update.message.reply_text(f"Your collection: {', '.join(user_collection[user_id])}")

# Start command function
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to the Waifu & Husbando Catcher Bot! Type /catch to encounter a random character."
    )

# Catch command function
def catch(update: Update, context: CallbackContext):
    send_random_character(update, context)

# Main function to set up the bot
def main():
    updater = Updater(API_TOKEN)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("catch", catch))
    dispatcher.add_handler(CommandHandler("collection", show_collection))
    dispatcher.add_handler(CallbackQueryHandler(catch_character))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
