import telebot
import lyricsgenius

#TOKENS
TOKEN = "1942025448:AAHGxLtxa1DP_G_y5Wo93vaYtECmIU64MFM"
GENIUStoken = "WywbmDXksHJO6XeM_tQO26J3IlJpS5fL5sivuCUScCpyeh7tnEVw5wzh6B9w0_6-"
genius_object = lyricsgenius.Genius(GENIUStoken)

knownUsers = []
userStep = {}

#List of commands
commands = {
    'start'        : 'Say hi to Discorama',
    'help'         : 'Gives you information about the available commands',
    'lyrics'       : "Gives you lyrics to a song, use /lyrics followed by title of song, a comma, followed by the artist. Example: '/lyrics Baby, Justin Bieber'",
    }
  
#UID setup, see who uses the app, potentially add user uid into a file
def get_user_setup(UID):
    if UID in userStep:
        return userStep[UID]
    
    else:
        knownUsers.append(UID)
        userStep[UID] = 0
        print("Please use the /start command")
        return 0
    
#Listener    
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) + "[" +str(m.chat.id) + "]:" + m.text)

#----- MAIN PROGRAM -----
bot = telebot.TeleBot(TOKEN, parse_mode=None)
bot.set_update_listener(listener)

#----- Start of Start command -----
@bot.message_handler(commands = ['start'])
def command_start(m):
    CID = m.chat.id
    #if CID not in knownUsers:
        #knownUsers.append(CID)
        #userStep[CID] = 0
    bot.send_message(CID, "Hello " + str(m.chat.first_name))
    bot.send_message(CID, "I'm Discorama Bot")
    command_help(m)
    #else:
        #bot.send_message(CID, "I have scanned you before")
#----- End of Start command -----

        
#----- Start of Help command ------
@bot.message_handler(commands = ['help'])
def command_help(m):
    CID = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:
        help_text += "/" +key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(CID, help_text)
#----- End of Help command ------

    
#----- TEST -----

#----- TEST -----


#----- Start of Lyrics command -----
@bot.message_handler(commands = ['lyrics'])
def get_lyric(message):

    CID = message.chat.id #Attain chat ID
    try:
        message_dict = message.text.split() #Turns the message into a text(.text) and splits the message into a dictionary (.split)
        comma = "," #Comma string
        res = ''    #Empty string 1
        res2 = ''   #Empty string 2

        for word in message_dict: #Loop through each word in message dictionary
            if comma in word: #Check for comma in each word in message dictionary
                index = message_dict.index(word) #Get index of the word before comma
                title_dict = message_dict[1:index+1] #Retrieve the title
                artist_dict = message_dict[index:] #Retrieve the artist name

        for word in title_dict: #Convert the title into a string
            res += word + ' '
            song = res
        
        for word in artist_dict: #Convert the artist name into a string
            res2 += word + ' '
            artist = res2
        
        song = genius_object.search_song(song, artist) #Search for the song title and artist
        try:
            lyrics = song.lyrics 
            bot.send_message(CID, lyrics) #Send lyrics
        except: #Error message
            bot.send_message(CID, "Sorry, I could not find any lyrics to this song. Please check that the spelling is correct and there is a comma after the song title")

    except:#Error message
        bot.send_message(CID, "Sorry I did not understand that, please check that all spelling is correct and that there is a comma after the song title")
#----- End of Lyrics command -----

#Polling..
bot.polling()
