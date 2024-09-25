import telebot
import os
from datetime import datetime

# Get the bot token from environment variables
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Check if the token was found
if not BOT_TOKEN:
    raise ValueError("Bot token not found. Make sure to set the TELEGRAM_BOT_TOKEN environment variable.")

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Function to modify the URL
def modify_url(url):
    if "?" in url:
        base_url = url.split("?")[0]
    else:
        base_url = url
    modified_url = base_url + "?download=1"
    return modified_url

# Function to log user info and URL into a file
def log_user_and_url(user_id, username, url):
    with open('log.txt', 'a') as log_file:
        log_file.write(f"{datetime.now()} - User ID: {user_id}, Username: {username}, URL: {url}\n")

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me a URL and I will modify it.")

# Handler for URLs
@bot.message_handler(func=lambda message: message.text.startswith('http'))
def modify_and_send_url(message):
    url = message.text
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Log the URL and user details
    log_user_and_url(user_id, username, url)
    
    modified_url = modify_url(url)
    bot.reply_to(message, f"Modified URL: {modified_url}")

# Catch invalid URLs
@bot.message_handler(func=lambda message: not message.text.startswith('http'))
def invalid_url(message):
    bot.reply_to(message, "Please send a valid URL.")

# Start polling (keep the bot running)
bot.infinity_polling()
