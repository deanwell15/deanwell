import telebot
from config import *
from telebot import types
from random import randint

GROUP_ID = -396165229

rndnum = -1
bet = 0
isbet = False

users = {}

bot = telebot.TeleBot('1022359618:AAG9VVhAEmSWubyQLp7OXs_TAq74t1J4D2M')

def main_menu(chat, msg):
	markup = types.ReplyKeyboardMarkup()
	game = types.KeyboardButton('/game')
	bal = types.KeyboardButton('Balance')
	markup.row(game,bal)
	bot.send_message(chat, msg, reply_markup = markup)

def make_bet(chat, bal):
	global isbet
	txt = 'Your balance is ' + str(bal) + '\nType your bet: '
	isbet = True
	bot.send_message(chat, txt)


@bot.message_handler(commands=['start','help'])
def start_help(message):
	main_menu(message.chat.id, HELLO_TEXT)


@bot.message_handler(commands=['game'])
def lalala(message):
	usr = message.from_user.id
	chat = message.chat.id
	markup = types.ReplyKeyboardRemove(selective=False)
	bot.send_message(chat, 'The number is 50', reply_markup = markup)
	global rndnum, bet, isbet
	rndnum = randint(1,100)
	make_bet(chat, users[usr]['balance'])

def betting(chat):
	markup = types.ReplyKeyboardMarkup(row_width=1)
	btn1 = types.KeyboardButton('Less')
	btn2 = types.KeyboardButton('More')
	markup.row(btn1,btn2)
	bot.send_message(chat, 'Less or more?', reply_markup = markup)

@bot.message_handler(content_types = ['text'])
def text_handler(message):
	msg = message.text
	chat = message.chat.id
	usr = message.from_user.id
	global rndnum, bet, isbet
	if isbet:
		isbet = False
		#if msg != int or int(msg) > users[usr]['balance'] or int(msg) < 0:
		#	txt = msg + 'Enter correct value:)'
		#	bot.send_message(chat, txt)
		#	make_bet(chat, users[usr]['balance'])
		bet = int(msg)
		txt = 'Okay your bet is ' + str(bet)
		bot.send_message(chat, txt)
		betting(chat)
	if (msg == 'Less' or msg == 'More') and rndnum > 0:
		txt = 'The number was ' + str(rndnum)
		markup = types.ReplyKeyboardRemove(selective=False)
		bot.send_message(chat, txt, reply_markup = markup)
		if (msg == 'Less' and rndnum > 50) or (msg == 'More' and rndnum <= 50):
			txt = 'You lost ' + str(bet) + ' :('
			users[usr]['balance'] -= bet
		else:
			txt = 'You won ' + str(bet*2) + '!'
			users[usr]['balance'] += bet*2
		txt += '\nYour balance is now ' + str(users[usr]['balance'])
		bot.send_message(chat, txt)
		rndnum = -1
		main_menu(message.chat.id, 'Exiting to main menu...')
	elif msg == 'Balance':
		txt = 'Your balance now is '+ str(users[usr]['balance'])
		markup = types.ReplyKeyboardMarkup()
		back = types.KeyboardButton('Back to main menu')
		markup.add(back)
		bot.send_message(chat, txt, reply_markup = markup)
	elif msg == 'Back to main menu':
		main_menu(chat, 'Exiting to main menu...')
	elif msg == 'name':
		if not(usr in users.keys()):
			users[usr] = {}
			users[usr]['balance'] = 100
			bot.send_message(-396165229, 'Welcome! Your balance is 100')
		else:
			txt = 'I know you! Your balance is ' + str(users[usr]['balance'])
			bot.send_message(chat, txt)




	
#d sa

# RUN 
bot.polling(none_stop = True)
