import logging
import constants as key
from telegram.ext import *
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from pymongo import MongoClient

client = MongoClient("")
db = client[""]
collection = db[""]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

MSG, AGE, GENDER, PREF, BIO, CHOOSE_STATE, WELC, CHAT, MATCHREQUEST, REJECT= range(10)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def start(update, context):
    """Starts the bot and lets user choose register, match or chat"""
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    name = update.message.from_user.first_name
    x = {'user_id': user_id, 'username': username, 'name': name, 'age': '0', 'gender': '0', 'bio': '', 'connected': False, 'partner_id': '0'}
    exist = collection.find_one({'user_id': user_id})

    if not exist:
        collection.insert_one(x)
    else:
        partner_id = exist["partner_id"]
        collection.update_one({"user_id": user_id}, {"$set": {"connected": False, "partner_id":'0'}})
        if partner_id:
            collection.update_one({"user_id": partner_id}, {"$set": {"connected": False, "partner_id":'0'}})


    reply_keyboard = [['Register your profile', 'Match with a Donut']]
    update.message.reply_text('Please choose one option!', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose one'
    ),)

    return CHOOSE_STATE

# def choose_state(update, context):
#     choice = update.message.text
#     print(choice)
#     if choice == 'Register your profile':
#         return REGISTER
#     elif choice == 'Match with a Donut':
#         return MATCH
#     else: return CHAT

def register(update, context):
    update.message.reply_text('Welcome to Kopi Meets Donuts! We will start off with your age, gender, sexual pref and a short bio',
                              reply_markup=ReplyKeyboardRemove(),)
    #asking for age here, query in next function
    update.message.reply_text('What is your age?')
    user = update.message.from_user
    logger.info("register function: Age of %s: %s", user.first_name, update.message.from_user)
    return AGE

def register_age(update, context):
    # query for the age here.
    age = update.message.text
    user = update.message.from_user

    if (not age.isdigit()):
        update.message.reply_text('Please enter a valid age number!')
        return AGE

    user_id = update.message.from_user.id
    collection.update_one({"user_id": user_id}, {"$set": {"age": age}}, upsert=True)
    logger.info("register_age function: Age of %s: %s", user.first_name, update.message.text)

    # asking for gender for the next state:
    reply_keyboard = [['Male', 'Female', 'Others']]
    update.message.reply_text('What is your gender?', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='M/F/Others'
    ))
    return GENDER


def register_gender(update, context):
    #query for the gender here
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    gender = update.message.text
    user_id = update.message.from_user.id
    collection.update_one({"user_id": user_id},{"$set": {"gender": gender}})

    #asking for preference
    reply_keyboard = [['Male', 'Female', 'Either', 'Others']]

    update.message.reply_text(
    'Which gender do you wish to connect with?',
        reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='M/F/Either/Others',))
    return PREF


def register_pref(update, context):
    #query for pref here
    user = update.message.from_user
    logger.info("Sexual preference of %s: %s", user.first_name, update.message.text)
    pref = update.message.text
    user_id = update.message.from_user.id
    collection.update_one({"user_id": user_id},{"$set": {"pref": pref}})

    #asking for bio
    update.message.reply_text('Type a short bio about yourself! Can be a fun fact or anything',
                              reply_markup=ReplyKeyboardRemove())
    return BIO


def register_bio(update, context):
    #query for bio here
    user = update.message.from_user
    logger.info("Biography of %s: %s", user.first_name, update.message.text)
    bio = update.message.text
    user_id = update.message.from_user.id
    collection.update_one({"user_id": user_id},{"$set": {"bio": bio}})

    update.message.reply_text('Registration Successful!')

    #after registration, should prompt the options and go back to choose state again
    reply_keyboard = [['Register your profile', 'Match with a Donut', 'Chat with your Donut!']]
    update.message.reply_text('Please choose one option!', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose one'
    ), )
    return CHOOSE_STATE


def match(update, context):
    user_id = update.message.from_user.id
    user_data = collection.find_one({"user_id" : user_id})
    print(user_data)
    user_gender = user_data["gender"]
    user_pref = user_data["pref"]
    print(user_data["gender"])
    print(user_data["pref"])

    #Guard prevents someone who has requested to enter matching page again
    if user_data['connected'] == True:
        update.message.reply_text("You are awaiting request, please wait for your partner to accept or reject.")
        reply_keyboard = [['Register your profile', 'Match with a Donut', 'Chat with your Donut!']]
        update.message.reply_text('Please choose one option!', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose one'
        ), )
        return CHOOSE_STATE

    # matching
    if user_gender == "Male" and user_pref == "Male":
        match_list = collection.find({"gender": "Male", "pref": "Male", "connected": False})

    elif user_gender == "Female" and user_pref == "Female":
        match_list = collection.find({"gender": "Female", "pref": "Female", "connected": False})

    elif user_gender == "Male" and user_pref == "Female":
        match_list = collection.find({"gender": "Female", "pref": "Male", "connected": False})

    elif user_gender == "Female" and user_pref == "Male":
        match_list = collection.find({"gender": "Male", "pref": "Female", "connected": False})

    elif user_gender == "Male" and user_pref == "Either":
        match_list = collection.find({"pref": "Male", "connected": False})

    elif user_gender == "Female" and user_pref == "Either":
        match_list = collection.find({"pref": "Female", "connected": False})

    else:
        match_list = collection.find({"gender": "Others", "pref": "Others", "connected": False})

    test_array = []
    message = ''

    for y in match_list:
        entry = y["name"]
        user_username = y["username"]
        if user_username != user_data["username"]:
            test_array.append(entry)
            message += 'Username: ' + y["name"] + '\n'
            message += 'Age: ' + y["age"] + '\n'
            message += 'Bio: ' + y["bio"] + '\n'
            message += '\n'

    reply_keyboard = [test_array]
    print(reply_keyboard)
    update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose one'
    ), )
    return MATCHREQUEST

def match_request(update, context):
    # Your ID
    user_id = update.message.from_user.id
    partner_name = update.message.text

    # Retrieve Partner ID from DB
    partner_data = collection.find_one({"name": partner_name})
    partner_id = partner_data["user_id"]
    partner_connectedness = partner_data["connected"]

    # Update the partner ID into the Database
    collection.update_one({"user_id": user_id}, {"$set": {"partner_id": partner_id}})
    collection.update_one({"name": partner_name}, {"$set": {"partner_id": user_id}})

    #Set user 'connected' to true, 'partner' remains false.
    collection.update_one({"user_id": user_id}, {"$set": {"connected": True}})

    #Sends request to significant other
    if not partner_connectedness:
        # keyboard = [['/Accept', '/Reject']]
        context.bot.send_message(chat_id=partner_id, text='You have a request, type /Accept to accept or /Reject to reject')

    #after sending the request, should prompt the options and go back to the menu
    reply_keyboard = [['Chat with your Donut!']]
    update.message.reply_text('Please choose one option!', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose one'
    ), )
    return CHOOSE_STATE


def toggle(update, context):
    ans = update.message.text
    user_id = update.message.from_user.id
    user_data = collection.find_one({"user_id": user_id})
    partner_id = user_data["partner_id"]
    partner_data = collection.find_one({"user_id": partner_id})

    if ans == '/Accept':
        collection.update_one({"user_id": user_id}, {"$set": {"connected": True}})
        context.bot.send_message(chat_id=partner_id, text='You have been accepted :)')
        reply_keyboard = [['Chat with your donut now!']]
        update.message.reply_text("Let's start chatting!", reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose one'
        ), )
        return CHAT

    elif ans == '/Reject':
        collection.update_one({"user_id": user_id}, {"$set": {"connected": False}})
        collection.update_one({"user_id": partner_id}, {"$set": {"connected": False}})

        context.bot.send_message(chat_id=partner_id, text='You have been rejected :(')

        # after sending no, should prompt the options and go back to the menu
        reply_keyboard = [['Register your profile', 'Match with a Donut', 'Chat with your Donut!']]
        update.message.reply_text('Please choose one option!', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose one'
        ), )
        return CHOOSE_STATE

def chat(update, context):
    user_id = update.message.from_user.id
    user_data = collection.find_one({"user_id": user_id})
    partner_id = user_data["partner_id"]
    partner_data = collection.find_one({"user_id": partner_id})
    partner_connected = partner_data["connected"]
    user_connected = user_data["connected"]

    message = ''

    if partner_connected and user_connected:
        partner_name = partner_data["name"]
        message += ("Age: " + partner_data["age"] + '\n')
        message += ("Bio: " + partner_data["bio"] + '\n')
        update.message.reply_text('You\'re matched with your Kopi, ' + partner_name + '! Dive right in, Donut!')
        update.message.reply_text(message)
        return MSG
    else:
        update.message.reply_text('You do not have an active chat!')

        reply_keyboard = [['Register your profile', 'Match with a Donut', 'Chat with your Donut!']]
        update.message.reply_text('Please choose one option!', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose one'
        ), )
        return CHOOSE_STATE

def msg(update, context):
    user_id = update.message.from_user.id
    user_data = collection.find_one({"user_id": user_id})
    partner_id = user_data["partner_id"]

    context.bot.send_message(chat_id=partner_id, text=update.message.text)
    return MSG

def cancel(update, context):
    #/quit will make connected to False for both parties.
    user_id = update.message.from_user.id

    user_data = collection.find_one({"user_id": user_id})
    partner_id = user_data["partner_id"]

    context.bot.send_message(chat_id=partner_id, text="Your partner has left the chat. Please /cancel and /start to match again.")

    collection.update_one({"user_id": user_id}, {"$set": {"connected": False}})
    collection.update_one({"user_id": partner_id}, {"$set": {"connected": False}})

    if partner_id:
        collection.update_one({"user_id": user_id}, {"$set": {"partner_id":'0'}})


    user = update.message.from_user

    logger.info("User %s quit the conversation", user.first_name)
    update.message.reply_text('Thanks for using KopiMeetsDonut!')

    return ConversationHandler.END

def main():
    updater = Updater(key.API_KEY, use_context=True)
    dp = updater.dispatcher

    quit = CommandHandler('cancel', cancel)
    accept = CommandHandler(['Accept', 'Reject'], toggle)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)], #start function here
        states={
            CHOOSE_STATE: [accept, MessageHandler(Filters.regex('Register your profile'), register),
                           MessageHandler(Filters.regex('Match with a Donut'), match),
                           MessageHandler(Filters.regex('Chat with your Donut'), chat)],
            CHAT: [quit, accept, MessageHandler(Filters.all, chat)],
            REJECT: [quit, accept, MessageHandler(Filters.all, toggle)],
            MATCHREQUEST: [quit, accept, MessageHandler(Filters.all, match_request)],
            MSG: [quit, accept, MessageHandler(Filters.all, msg)],
            AGE: [quit, accept, MessageHandler(Filters.text, register_age)],
            GENDER: [quit, accept, MessageHandler(Filters.text, register_gender)],
            PREF: [quit, accept, MessageHandler(Filters.text, register_pref)],
            BIO: [quit, accept, MessageHandler(Filters.text, register_bio)],
        },
        fallbacks=[quit], allow_reentry=True,
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()




