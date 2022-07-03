from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from sql import *

TOKEN = "<your TOKEN>"  # Dont forget input your token here
bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def start(update, context):
    arg = context.args
    if not arg:
        context.bot.send_message(update.effective_chat.id, """Hello, it's your to-do list. To use it enter the 
        command. Choose an action: 
        "/add (name), (description)" to add a new task 
        "/del (id of task to delete)" to delete the task 
        "/done (id of task to complete)" to mark the task as completed 
        "/show" to show tasks""")


def print_data(update, context):
    user_id = update.message.from_user.id
    data = get_data(user_id)
    if bool(data):
        for i in data:
            text = 'Task №{0}\nName: {1}\nDescription: {2}\nStatus: {3}'.format(i[0], i[1], i[2], i[3])
            context.bot.send_message(update.effective_chat.id, text)
    else:
        context.bot.send_message(update.effective_chat.id, 'You have no task. To add task enter "/add (name), '
                                                           '(description)"')


def info(update, context):
    context.bot.send_message(update.effective_chat.id, """Choose an action:
    "/add (name), (description)" to add a new task
    "/del (id of task to delete)" to delete the task
    "/done (id of task to complete)" to mark the task as completed
    "/show" to show tasks""")


def add_task(update, context):
    user_text = update.message.text
    if ", " in user_text:
        user_id = update.message.from_user.id
        name = user_text[5: user_text.find(',')]
        description = user_text[user_text.find(',') + 2:]
        db(str(user_id))
        add_info_bd(name, description, user_id)
        context.bot.send_message(update.effective_chat.id, "Task successfully added")
    else:
        context.bot.send_message(update.effective_chat.id, "Incorrect format. Use '/add (name), (description)'")


def change_status(update, context):
    user_text = update.message.text[6:]
    if str(user_text).isdigit():
        user_id = update.message.from_user.id
        if id_exists(user_id, user_text):
            update_status(user_text, user_id)
            context.bot.send_message(update.effective_chat.id, "Task status changed")
        else:
            context.bot.send_message(update.effective_chat.id, "There isn't this id")
    else:
        context.bot.send_message(update.effective_chat.id, "Error: <Enter id in number format>")


def del_task(update, context):
    user_text = update.message.text[5:]
    if str(user_text).isdigit():
        user_id = update.message.from_user.id
        if id_exists(user_id, user_text):
            del_data(user_text, user_id)
            context.bot.send_message(update.effective_chat.id, "Task deleted")
            if bool(max_id(user_id)):
                for i in range(int(user_text), max_id(user_id)):
                    conn.execute(f"UPDATE user{user_id} SET task_num = {i} WHERE task_num = {i + 1}")
                    conn.commit()
        else:
            context.bot.send_message(update.effective_chat.id, "There isn't this id")
    else:
        context.bot.send_message(update.effective_chat.id, "Error: <Enter id in number format>")


def message(update, context):
    text = update.message.text
    if text.lower() == 'привет':
        context.bot.send_message(update.effective_chat.id, "Hello, i don't understand Russian, use English please")
    else:
        context.bot.send_message(update.effective_chat.id, "I don't understand you. Enter /info to get command list")
    db_logs(update.message.from_user.id, None, f"incorrect input: {text}")


def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, f"There isn't such command. Enter /info to get command list")


start_handler = CommandHandler('start', start)
complete_handler = CommandHandler('done', change_status)
del_handler = CommandHandler('del', del_task)
add_task_handler = CommandHandler('add', add_task)
info_handler = CommandHandler('info', info)
show_handler = CommandHandler('show', print_data)

message_handler = MessageHandler(Filters.text, message)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(del_handler)
dispatcher.add_handler(complete_handler)
dispatcher.add_handler(show_handler)
dispatcher.add_handler(add_task_handler)
dispatcher.add_handler(unknown_handler)
dispatcher.add_handler(message_handler)

print('server started')
updater.start_polling()
updater.idle()
