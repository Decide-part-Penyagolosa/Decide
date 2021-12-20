import logging
import json
import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,ConversationHandler
from utilities import global_vars
import os

API_DECIDE = 'http://localhost:8000/'
BOT_TOKEN = '5061816889:AAFSjO0WEToxu2gGVvN47pVdTFDfju71fEg'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

LOGIN, STORE, VOTINGS, VOTING, SAVE_VOTE  = range(5)


def get_token(credentials):

    r = requests.post(API_DECIDE + "authentication/login/", credentials)

    return r


def get_votings(id):

    r = requests.get(API_DECIDE + "voting/user/?id="+str(id))
    return r


def get_user(token):
    data = {'token': token}
    r = requests.post(API_DECIDE + "authentication/getuser/", data)
    return r

def save_vote_data(data_dict):
    
    headers = {"Authorization": "Token " + data_dict['token'],
                "Content-Type": "application/json"}
    
    r = requests.post(API_DECIDE + "store/", json=data_dict, headers = headers)

    print(r.status_code)
    return r



def login(update, context):
    user = update.message.from_user
    logger.info("%s  %s", user.first_name, update.message.text)
    update.message.reply_text("Indique su nombre de usuario y tu contraseña de la siguiente forma. \nUsername \nContraseña",
                              reply_markup=ReplyKeyboardRemove())
    return STORE

def store(update, context):
    credentials = {}
    next_state = ConversationHandler.END
    for index, i in enumerate(update.message.text.split("\n")):
        if index == 0:
            credentials["username"] = i
        else:
            credentials["password"] = i

    response = get_token(credentials)
    if response.status_code == 200:
        global_vars.token = json.loads(response.text)["token"]
        username = credentials['username']
        update.message.reply_text("¡Ya has iniciado sesión, " + username + "!")
        user = update.message.from_user
        logger.info("Usuario  %s logged", user.first_name)
        reply_keyboard = [['Vote']]
        update.message.reply_text(update.message.text, reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True))
        next_state = VOTINGS
    else:
        update.message.reply_text(
            "Los credenciales son incorrectos, índicalos o escribe /cancel para salir")
        next_state = STORE

    return next_state

def start(update, context):
    update.message.reply_text('Hi!')
    #reply_keyboard = [['Login']]
    #update.message.reply_text(
     #   'Hi! My name is EGC_decide_bot. Lets vote',
      #  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    #return LOGIN


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! You canceled the conversation, see you later.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('An error has ocurred when you were voting, restart the voting process with "/start".',
                            reply_markup=ReplyKeyboardRemove())   

    return ConversationHandler.END









def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            LOGIN: [MessageHandler(Filters.regex('^(Login)$'), login)],

            #STORE: [MessageHandler(Filters.text, login.store)],

            #VOTINGS: [MessageHandler(Filters.regex('^(Vote)$'), votings.votings)],

            #VOTING: [MessageHandler(Filters.text, voting.voting)],

            #SAVE_VOTE: [MessageHandler(Filters.text,save_vote.save_vote)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

   # if(config.WEBHOOK):
    #    logger.info("WEBHOOK ACTIVADO")
     #   PORT = int(os.environ.get("PORT", config.PORT))
      #  updater.start_webhook(listen="0.0.0.0",
       #                       port=PORT,
        #                      url_path=config.BOT_TOKEN)
        #updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(config.HEROKU_APP_NAME, config.BOT_TOKEN))
    #else:
     #   updater.start_polling()

    updater.idle()








if __name__ == '__main__':
    main()
