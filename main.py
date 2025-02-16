import telebot

TOKEN = "7723650646:AAGS2YD7N3WuPrG5BTQ8zl_qOaBqurnA4sY"  # Replace with your actual bot token
bot = telebot.TeleBot(TOKEN)

orders = {}  # Store user orders

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to PrintBot! Send your file to start printing.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    file_path = file_info.file_path
    file_name = message.document.file_name
    
    orders[user_id] = {'file_id': message.document.file_id, 'file_name': file_name}
    
    bot.send_message(user_id, "File received! Now send your name and dorm number (e.g., John Doe, Dorm 12).")

@bot.message_handler(func=lambda message: message.chat.id in orders and 'dorm' not in orders[message.chat.id])
def handle_details(message):
    user_id = message.chat.id
    orders[user_id]['dorm'] = message.text
    
    bot.send_message(user_id, "Thank you! Your order is being processed. Confirm? (Yes/No)")

@bot.message_handler(func=lambda message: message.text.lower() == 'yes' and message.chat.id in orders)
def confirm_order(message):
    user_id = message.chat.id
    order_details = orders[user_id]
    
    bot.send_message(user_id, f"✅ Order Confirmed!\n📂 File: {order_details['file_name']}\n🏠 Delivery: {order_details['dorm']}\nPrinting in progress...")
    
    # Send a notification to the admin (your ID)
    ADMIN_ID =  5663993489
    bot.send_message(ADMIN_ID, f"New Order!\nUser: {user_id}\nFile: {order_details['file_name']}\nDorm: {order_details['dorm']}")

bot.polling()
