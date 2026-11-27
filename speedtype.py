import random
import time
import math
try:
    import textsource
except ModuleNotFoundError:
    print("please install text source file for the game")
try:
    import mysql.connector as sql
except ModuleNotFoundError:
    print("please install mysql.connector module")
    exit()

while True:
    try:
        host = input("Enter mysql host to connect to: ")
        user = input("Enter mysql username: ")
        password = input("Enter mysql password: ")

        mydb = sql.connect(
            host=host,
            user = user,
            password = password
        )
        print("Connection successful")
        break
    except sql.Error:
        print("Please enter correct host, username and password")

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS TYPERACER")
mycursor.execute("USE TYPERACER")
mycursor.execute('''CREATE TABLE IF NOT EXISTS ALL_ATTEMPTS (
ATTEMPT_NUMBER int auto_increment primary key,
DATE_TIME varchar(80),
NAME varchar(80),
WORDS_PER_MINUTE float,
ACCURACY float,
WEIGHTED_WPM float)''')



date = time.ctime()


def startgame():
    def terminate():
        confirm = input("Do you want to play again? (any other input results in an end) (y/n): ")
        if confirm == "y":
            return True
        else:
            return False

    print("Welcome to Typeracer!")
    while True:

        input1 = int(input('''
        Enter
        1 to play 
        2 to check past attempts
        3 to see leaderboard
        '''))

        if input1 == 1:

            playername = input("Enter your name, game will start immediately after : ")
            selection = random.choice(list(textsource.source.items()))  # textsource is a different file containing all the paragraphs available for the game
            text = selection[1]
            source_of_text = selection[0]

            print("Type the following paragraph as fast as you can!" )
            print(text)
            start_time = time.perf_counter()
            print("Type here (press enter twice to finish):\n")
            entry = []
            while True:
                line = input()
                if line == '':
                    break
                entry.append(line)
            entry = '\n'.join(entry)
            end_time = time.perf_counter()
            total_time = round(end_time - start_time, 3)

            errors = 0
            min_len = min(len(entry.split()), len(text.split()))
            for i in range(min_len):
                if entry.split()[i] != text.split()[i]:
                    errors += 1
            errors += abs(len(entry.split())-len(text.split()))

            total_words_typed = len(entry.split())
            total_source_words = len(text.split())

            accuracy = round((1 - (errors/total_source_words)),2)
            percent_accuracy = 100*accuracy
            wpm = round((total_words_typed/total_time)*60,2)

            multi = math.sin(1.57*accuracy)**2
            weighted_wpm = round(wpm * multi)

            print(f'''Good job! You just typed a quote from {source_of_text}
            Your time was: {total_time} seconds
            You typed {wpm} words per minute on average
            Your accuracy is: {percent_accuracy}%
            Your weighted words per minute is: {weighted_wpm}
            You got {errors} words wrong!''')

            mycursor.execute(f'''INSERT INTO ALl_ATTEMPTS
             (DATE_TIME,NAME,WORDS_PER_MINUTE,ACCURACY,WEIGHTED_WPM) 
             VALUES
             ("{date}","{playername}",{wpm},{percent_accuracy},{weighted_wpm} ) ''')
            mydb.commit()

            if terminate():
                continue
            else:
                break


        elif input1 == 2:
            mycursor.execute("SELECT * FROM ALL_ATTEMPTS")
            for i in mycursor.description:
                print(i[0], end=' ')
            print()
            for i in mycursor.fetchall():
                print(i)
            if terminate():
                continue
            else:
                break


        elif input1 == 3:
            while True:
                x = str(input('Enter parameter for sorting (ACCURACY/WORDS_PER_MINUTE/WEIGHTED_WPM): '))

                if x in ["ACCURACY","WORDS_PER_MINUTE","WEIGHTED_WPM"]:
                    mycursor.execute(f'SELECT * FROM ALL_ATTEMPTS ORDER BY {x} DESC')
                    for i in mycursor.description:
                        print(i[0], end = ' ')
                    print()
                    for i in mycursor.fetchall():
                        print(i)
                    break
                else:
                    print("Please enter a valid input")
            if terminate():
                continue
            else:
                break

        else:
            print("please enter a valid input")













