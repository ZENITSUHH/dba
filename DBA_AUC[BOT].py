#6882194604

import requests
import telebot
from telebot import types
import time

bot = telebot.TeleBot("7167579834:AAFmpwPdKHT6eE4aELSOB8CC8gi_tPrutPA")

user_groups = {}

started_users = set()

banned_users = set()

@bot.message_handler(commands=['start'])
def handle_start(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "YOU ARE BANNED")
    else:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        if user_groups.get(user_id, False):
            bot.reply_to(message, "Do /cmds for commands")
        else:
            if not all(user_groups.get(user_id, {}).values()):
                bot.send_message(message.chat.id, "Please join all groups first by clicking the buttons below.")
            else:
                welcome_message = ("🔸Welcome, {} To Auction Bot\n\n"
                                   "🔸You Can Submit Your Pokemon Through This Bot For Auction\n\n"
                                   "🔻But Before Using You Have To Join Our Auction Group By Clicking Below Two Buttons "
                                   "And Then Click 'Joined' Button").format(user_name)
                markup = types.InlineKeyboardMarkup(row_width=1)
                auction_group_button = types.InlineKeyboardButton("Join Auction Group", url="https://t.me/DBA_HEXA_AUCTION")
                trade_group_button = types.InlineKeyboardButton("Join Trade Group", url="https://t.me/DBA_HEXA_TRADE")
                joined_button = types.InlineKeyboardButton("Joined", callback_data="joined")
                markup.add(auction_group_button, trade_group_button, joined_button)
                bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
                user_id = message.from_user.id
                started_users.add(user_id)
                user_ids.add(user_id)


@bot.callback_query_handler(func=lambda call: call.data == "joined")
def joined_callback(call):
    user_id = call.from_user.id
    if user_id not in user_groups:
        user_groups[user_id] = {}
    user_groups[user_id][call.message.chat.id] = True
    bot.answer_callback_query(call.id, "Thanks for joining our group")

@bot.message_handler(commands=['cmds'])
def handle_cmds(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "YOU ARE BANNED")
    else:
        user_id = message.from_user.id
        if user_groups.get(user_id, False):
            bot.reply_to(message, '''
                     USER COMMANDS : - 

/start - Start The Bot
/add - Send Poke / TMs For Auction
/cancel - Cancel All Running Cmds
/item - List Of All Items In Auc
/natures - Get Natures Page 
/cmds - Get This Message
                     
ADMINS COMMANDS : - 
                     
/users - Get All Bot Users List
/list - Get List Of All Items In Auction 
/ban - Ban Any User
/unban - Unban Any User
/msg - Send Message To User
/approve - Make Someone Bot Admin
/broad - Send Message To All Bot 
/next - Send Next Item In Auction
/unapprove - Remove Someone Bot Admin
                     
OWNER COMMANDS :-

/clear - For Bot Owner''')
        else:
            bot.reply_to(message, "Please join our groups first by clicking the buttons in the start message.")

active_users = []

admin_ids = ["6882194604", "6843210459"]

@bot.message_handler(commands=['users'])
def handle_users(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "YOU ARE BANNED")
    else:
        user_id = message.from_user.id
        if str(user_id) in admin_ids:
            num_users = len(started_users)
            bot.send_message(message.chat.id, f"Total users who started the bot: {num_users}")
        else:
            bot.send_message(message.chat.id, "You are not authorized to use this command.")



admin_id = [6882194604, 6843210459]

@bot.message_handler(commands=['msg'])
def handle_msg(message):
    # Check if the user is an admin
    if message.from_user.id not in admin_id:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    try:
        _, user_id, user_message = message.text.split(maxsplit=2)
        user_id = int(user_id)
    except ValueError:
        bot.reply_to(message, "Invalid syntax. Use /msg (user_id) (message)")
        return

    try:
        bot.send_message(user_id, user_message)
        bot.reply_to(message, f"Message sent to user {user_id}")
    except Exception as e:
        bot.reply_to(message, f"Failed to send message to user {user_id}: {e}")

user_ids = set()

@bot.message_handler(commands=['broad'])
def handle_broad(message):
    if str(message.from_user.id) not in admin_ids:
        bot.reply_to(message, "You are not authorized to use this command.")
        return


    try:
        _, broad_message = message.text.split(maxsplit=1)
    except ValueError:
        bot.reply_to(message, "Invalid syntax. Use /broad (message)")
        return


    for user_id in user_ids:
        try:
            bot.send_message(user_id, broad_message)
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {e}")

    bot.reply_to(message, "Message forwarded to all users.")


@bot.message_handler(commands=['approve'])
def handle_approve(message):
    if str(message.from_user.id) not in admin_ids:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    try:
        _, user_id = message.text.split(maxsplit=1)
        admin_ids.append(user_id)
        admin_id.append(int(user_id)) 
        bot.reply_to(message, f"User with ID {user_id} has been successfully added to admin list.")
    except ValueError:
        bot.reply_to(message, "Invalid syntax. Use /approve <user_id>")


@bot.message_handler(commands=['ban'])
def handle_ban(message):
    if str(message.from_user.id) not in admin_ids:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    try:
        _, user_id = message.text.split(maxsplit=1)
        banned_users.add(user_id)  
        bot.reply_to(message, f"User with ID {user_id} has been banned.")
    except ValueError:
        bot.reply_to(message, "Invalid syntax. Use /ban <user_id>")


@bot.message_handler(commands=['unban'])
def handle_unban(message):
    if str(message.from_user.id) not in admin_ids:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    try:
        _, user_id = message.text.split(maxsplit=1)
        if user_id in banned_users:
            banned_users.remove(user_id) 
            bot.reply_to(message, f"User with ID {user_id} has been unbanned.")
        else:
            bot.reply_to(message, f"User with ID {user_id} is not banned.")
    except ValueError:
        bot.reply_to(message, "Invalid syntax. Use /unban <user_id>")

@bot.message_handler(commands=['unapprove'])
def handle_unapprove(message):
    if str(message.from_user.id) not in admin_ids:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    
    try:
        _, user_id = message.text.split(maxsplit=1)
        if user_id in admin_ids:
            admin_ids.remove(user_id)  
            admin_id.remove(int(user_id))  
            bot.reply_to(message, f"User with ID {user_id} has been removed from the admin list.")
        else:
            bot.reply_to(message, f"User with ID {user_id} is not an admin.")
    except ValueError:
        bot.reply_to(message, "Invalid syntax. Use /unapprove <user_id>")

item_counts = {
    "legendary": 0,
    "non_legendary": 0,
    "shiny": 0,
    "tms": 0,
    "teams": 0,
    "total_items": 0
}

# Check if the user is an admin
def is_admin(user_id):
    return user_id in admin_id

# Define the /item command handler
@bot.message_handler(commands=['item'])
def item(message):
    response = "🔹Currently Items In Auction - \n"
    response += "🔺Legendary: " + str(item_counts["legendary"]) + "\n"
    response += "🔺Non-Legendary: " + str(item_counts["non_legendary"]) + "\n"
    response += "🔺Shiny: " + str(item_counts["shiny"]) + "\n"
    response += "🔺TMs: " + str(item_counts["tms"]) + "\n"
    response += "🔺Teams: " + str(item_counts["teams"]) + "\n"
    response += "\n🔹Total Items: " + str(item_counts["total_items"]) + "\n"

    bot.reply_to(message, response)

def add_item(message, category):
    user_id = message.from_user.id
    if is_admin(user_id):
        item_counts[category] += 1
        item_counts["total_items"] += 1
        bot.reply_to(message, f"Added 1 item to {category.capitalize()} category.")
    else:
        bot.reply_to(message, "Only admins can perform this action.")

@bot.message_handler(commands=['legendary'])
def add_legendary(message):
    add_item(message, "legendary")

@bot.message_handler(commands=['non_legendary'])
def add_non_legendary(message):
    add_item(message, "non_legendary")

@bot.message_handler(commands=['shiny'])
def add_shiny(message):
    add_item(message, "shiny")

@bot.message_handler(commands=['tms'])
def add_tms(message):
    add_item(message, "tms")

@bot.message_handler(commands=['teams'])
def add_teams(message):
    add_item(message, "teams")

approved_items = {
    "legendary": [],
    "non_legendary": [],
    "shiny": [],
    "tms": [],
    "teams": []
}

group_id = -1002041160221 

def is_admin(user_id):
    return user_id in admin_id

@bot.message_handler(commands=['send'])
def send_message_prompt(message):
    if is_admin(message.from_user.id):
        bot.reply_to(message, "Type the message to send in the group")
        bot.register_next_step_handler(message, send_message)
    else:
        bot.reply_to(message, "Only admins can perform this action.")

def send_message(message):
    if message.forward_from or message.forward_from_chat:
        forwarded_message = message
    else:
        forwarded_message = message.text
    try:
        bot.forward_message(group_id, message.chat.id, message.id)
        bot.send_message(message.chat.id, "Message sent successfully.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Failed to send message: {e}")


stored_messages = {}


@bot.message_handler(commands=['store'])
def store_message_prompt(message):
    if is_admin(message.from_user.id):
        bot.reply_to(message, "Type the message you want to store:")
        bot.register_next_step_handler(message, store_message)
    else:
        bot.reply_to(message, "Only admins can perform this action.")

def store_message(message):
    stored_messages[message.message_id] = {"message": message.text, "chat_id": message.chat.id}
    bot.reply_to(message, "Message stored successfully.")

@bot.message_handler(commands=['next'])
def next_message(message):
    if is_admin(message.from_user.id):
        if stored_messages:
            next_message_id = next(iter(stored_messages))
            next_message_data = stored_messages.pop(next_message_id)
            bot.forward_message(message.chat.id, next_message_data["chat_id"], next_message_id)
        else:
            bot.reply_to(message, "No more stored messages.")
    else:
        bot.reply_to(message, "Only admins can perform this action.")

@bot.message_handler(func=lambda message: message.text == "." and (message.chat.type == "group" or message.chat.type == "supergroup") and str(message.from_user.id) in admin_ids)
def handle_dot(message):
    msg = bot.send_message(message.chat.id, "•")
    time.sleep(1.5)
    bot.edit_message_text("• •", message.chat.id, msg.message_id)
    time.sleep(1.5)
    bot.edit_message_text("• • •", message.chat.id, msg.message_id)
    time.sleep(1.5)
    keyboard = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton(text="Yes", callback_data="sell_pokemon")
    keyboard.add(yes_button)
    bot.edit_message_text("Do you want to sell the Pokemon?", message.chat.id, msg.message_id, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "sell_pokemon")
def sell_pokemon_callback(call):
    bot.answer_callback_query(call.id, "Pokemon has been sold!")
    bot.send_message(call.message.chat.id, "🔊 Pokemon Has Been Sold")

@bot.message_handler(commands=['sold'])
def handle_sold(message):
    if is_admin(message.from_user.id):
        try:
            command, *args = message.text.split(' ', 1)
            if len(args) != 1:
                raise ValueError
            pokemon_name = args[0]
            username = message.reply_to_message.from_user.username
            amount = message.reply_to_message.text
            reply_message = f"🔊 {pokemon_name} Has Been Sold\n\n🔸Sold to - @{username}\n🔸Sold for - {amount}\n\n❗ Join Trade Group To Get Seller Username After Auction"
            sent_message = bot.reply_to(message, reply_message)
            bot.pin_chat_message(message.chat.id, sent_message.id)  # Pin the message
        except ValueError:
            bot.reply_to(message, "Please provide the command in the format /sold (pokemon name)")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

@bot.message_handler(commands=['unsold'])
def handle_unsold(message):
    if is_admin(message.from_user.id):
        try:
            pokemon_name = message.text.split(' ', 1)[1]
            reply_message = f"❌ {pokemon_name} Has Been Unsold"
            sent_message = bot.reply_to(message, reply_message)
            bot.pin_chat_message(message.chat.id, sent_message.id)  # Pin the message
        except IndexError:
            bot.reply_to(message, "Please provide the name of the Pokemon to mark as unsold.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

bot.skip_pending = True

bot_owner_id = "6882194604"

def is_bot_owner(user_id):
    return str(user_id) == bot_owner_id

@bot.message_handler(commands=['clear'])
def clear_messages(message):
    if is_bot_owner(message.from_user.id):
        stored_messages.clear()
        bot.reply_to(message, "All stored messages have been cleared.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")


cancel_requested = False


@bot.message_handler(commands=['cancel'])
def cancel_command(message):
    global cancel_requested
    cancel_requested = True
    bot.reply_to(message, "All Running Commands Have Been Cancelled ✅")

submissions = {}


@bot.message_handler(commands=['add'])
def add_command(message):

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton("Legendary", callback_data="legendary"),
        types.InlineKeyboardButton("Non-Legendary", callback_data="non_legendary"),
        types.InlineKeyboardButton("Shiny", callback_data="shiny"),
        types.InlineKeyboardButton("TMs", callback_data="tms"),
        types.InlineKeyboardButton("Teams", callback_data="teams")
    )

    bot.reply_to(message, "Select the type of item you want to add:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ["legendary", "non_legendary", "shiny", "tms", "teams"])
def callback_handler(call):

    submissions[call.message.chat.id] = {"type": call.data}

    if call.data in ["legendary", "non_legendary", "shiny"]:

        bot.send_message(call.message.chat.id, "What is the name of the Pokemon you want to sell?")
        bot.register_next_step_handler(call.message, forward_info)
    elif call.data == "tms":

        bot.send_message(call.message.chat.id, "Enter the name of your TM:")
        bot.register_next_step_handler(call.message, forward_tm_info)
    elif call.data == "teams":

        bot.send_message(call.message.chat.id, "What is the name of your team?")
        bot.register_next_step_handler(call.message, forward_team_info)


def forward_info(message):
    submissions[message.chat.id]["name"] = message.text

  
    bot.send_message(message.chat.id, f"Please provide info of {message.text} by copying the text and pasting it here")
    bot.register_next_step_handler(message, forward_iv_ev)


def forward_iv_ev(message):
    submissions[message.chat.id]["info"] = message.text

    bot.send_message(message.chat.id, f"Please provide IVs/EVs of {submissions[message.chat.id]['name']} by copying the text and pasting it here")
    bot.register_next_step_handler(message, forward_moveset)


def forward_moveset(message):
    submissions[message.chat.id]["iv_ev"] = message.text


    bot.send_message(message.chat.id, f"Please provide the moveset of {submissions[message.chat.id]['name']} by copying the text and pasting it here")
    bot.register_next_step_handler(message, ask_iv_boosted)


def ask_iv_boosted(message):
    submissions[message.chat.id]["moveset"] = message.text


    bot.send_message(message.chat.id, "Is any IV boosted of this Pokemon?")
    bot.register_next_step_handler(message, ask_base)

def ask_base(message):

    submissions[message.chat.id]["iv_boosted"] = message.text

   
    bot.send_message(message.chat.id, "Tell me the base for your Pokemon?")
    bot.register_next_step_handler(message, send_submission)


def send_submission(message):

    submissions[message.chat.id]["base"] = message.text

    bot.send_message(message.chat.id, f"Your Pokemon {submissions[message.chat.id]['name']} has been sent for submission")

    send_to_admin(message.chat.id)

def forward_tm_info(message):
    submissions[message.chat.id]["name"] = message.text

    bot.send_message(message.chat.id, "Tell me the base for your TM:")
    bot.register_next_step_handler(message, send_submission)


def forward_team_info(message):
    submissions[message.chat.id]["name"] = message.text


    bot.send_message(message.chat.id, "Send the list of team members:")
    bot.register_next_step_handler(message, forward_team_members)

def forward_team_members(message):
    submissions[message.chat.id]["members"] = message.text

    
    bot.send_message(message.chat.id, "Tell me the base for your team:")
    bot.register_next_step_handler(message, send_submission)

def send_to_admin(chat_id):
    submission_data = submissions[chat_id]
    admin_chat_id = "6882194604"
    
    bot.send_message(admin_chat_id, "New Submission:")

    bot.send_message(admin_chat_id, f"Type: {submission_data['type']}")
    if submission_data['type'] in ["legendary", "non_legendary", "shiny"]:
        bot.send_message(admin_chat_id, f"Name: {submission_data['name']}")
        bot.send_message(admin_chat_id, f"Info: {submission_data['info']}")
        bot.send_message(admin_chat_id, f"IVs/EVs: {submission_data['iv_ev']}")
        bot.send_message(admin_chat_id, f"Moveset: {submission_data['moveset']}")
        bot.send_message(admin_chat_id, f"IV Boosted: {submission_data['iv_boosted']}")
        bot.send_message(admin_chat_id, f"Base: {submission_data['base']}")
    elif submission_data['type'] == "tms":
        bot.send_message(admin_chat_id, f"Name: {submission_data['name']}")
        bot.send_message(admin_chat_id, f"Base: {submission_data['base']}")
    elif submission_data['type'] == "teams":
        bot.send_message(admin_chat_id, f"Name: {submission_data['name']}")
        bot.send_message(admin_chat_id, f"Members: {submission_data['members']}")
        bot.send_message(admin_chat_id, f"Base: {submission_data['base']}")
    bot.send_message(admin_chat_id, f"User ID: {chat_id}")

bot.polling()