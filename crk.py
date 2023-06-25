import streamlit as st
import streamlit.components.v1 as components
import time
import requests
import speech_recognition as sr
import datetime
import pygame
import threading
import os
import mysql.connector
import tkinter as tk
import webview
import speedtest
import sqlite3
import pyttsx3
import spacy
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.gui.sudoku_gui import GUI

st.set_page_config(page_title="Cleo 🧠", page_icon="sphere.png")
st.markdown('<h1 class="cleo">Cleo 🧠</h1>', unsafe_allow_html=True)

nlp = spacy.load("en_core_web_sm")

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Set the voice ID to a female voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# Set up the mysql connection
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="jai25"
)
# Create a cursor object to execute mysql commands
cursor = mydb.cursor()

# Create a connection to the sqlite database
conn = sqlite3.connect('todo_lists.db')

# Create a cursor object to execute sqlite commands
curz = conn.cursor()

url = "https://openai80.p.rapidapi.com/chat/completions"



# Function to run on click recognition
def run_tes():
    global tes_running
    if not tes_running:
        tes_running = True
        os.system("streamlit run tes.py")
        tes_running = False

# Function to speak out text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define the function to play a sound
def ps():
    pygame.init()
    sound = pygame.mixer.Sound('dark-church-organ-trap-melody_80bpm_B_minor.wav')
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)



# Define the function to open the app
def open_app(app_name):
    try:
        os.startfile(app_name)
    except FileNotFoundError:
        response += f"Could not find {app_name}."



# Define the function to check the internet speed
def check_internet_speed():
    try:
        st = speedtest.Speedtest()
        return "Your download speed is: "+str(round(st.download() / 1000000, 3))+"Mbps! \n Your upload speed is: "+str(round(st.upload() / 1000000, 3))+"Mbps! \n Woww, Pretty fast!"
    except:
        return "Couldn't check the speed."


# Define the function to set a timer
def set_timer(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        time.sleep(1)
    response = "Time's up!"
    ps()


def play_sound():
    # Play the alarm sound
    pygame.mixer.init()
    pygame.mixer.music.load("rnme.wav")
    pygame.mixer.music.play()

def set_reminder(duration, reminder_message):
    # Calculate reminder time by adding duration to the current time
    reminder_time = time.time() + duration * 60
    while True:
        current_time = time.time()
        if current_time >= reminder_time:
            # Print the reminder message and play the alarm sound in a separate thread
            response = reminder_message
            threading.Thread(target=play_sound).start()
            break

def set_alarm(alarm_time):
    try:
        while True:
            current_time = time.strftime('%H:%M:%S')
            if current_time == alarm_time:
                response = "Time's up!"
                pygame.mixer.init()
                pygame.mixer.music.load("alarm_sound.mp3")
                pygame.mixer.music.play()
                break
    except KeyboardInterrupt:
        response += "Couldn't set the alarm."

# Define the function to create a sudoku puzzle
def sudoku():
    root = tk.Tk()
    root.geometry("1690x845")
    root.configure(background='#c6c8df')
    root.title("Sudoku Puzzle")

    Game = GUI(root)
    Game.generate_sudoku_board()
    Game.right_side_option_block()

    root.mainloop()


# Define a function to create a new to-do list
def create_todo_list(name):
    # Create a new table for the to-do list
    curz.execute(f"CREATE TABLE {name} (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, status TEXT)")
    conn.commit()
    return f"New to-do list '{name}' created successfully!"


# Define a function to add a task to a to-do list
def add_task(todo_list, task):
    # Insert the new task into the specified to-do list
    curz.execute(f"INSERT INTO {todo_list} (task, status) VALUES (?, ?)", (task, 'incomplete'))
    conn.commit()
    return f"Task '{task}' added to '{todo_list}' successfully!"


# Define a function to edit a task in a to-do list
def edit_task(todo_list, task_id, new_task):
    # Update the specified task in the specified to-do list
    curz.execute(f"UPDATE {todo_list} SET task=? WHERE id=?", (new_task, task_id))
    conn.commit()
    response = f"Task {task_id} updated to '{new_task}' in '{todo_list}' successfully!"


# Define a function to delete a task from a to-do list
def delete_task(todo_list, task_id):
    # Delete the specified task from the specified to-do list
    curz.execute(f"DELETE FROM {todo_list} WHERE id=?", (task_id,))
    conn.commit()
    return f"Task {task_id} deleted from '{todo_list}' successfully!"


# Define a function to delete a to-do list
def delete_todo_list(name):
    # Delete the specified to-do list
    curz.execute(f"DROP TABLE {name}")
    conn.commit()
    return f"To-do list '{name}' deleted successfully!"


# Define a function to view all the to-do lists
def show_todo_lists():
    # Show all the to-do lists
    curz.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = curz.fetchall()
    resp = " \n"
    for table in tables:
        resp+= "- " + table[0]+"\n "
    print(resp)
    return resp


# Define a function to view all the tasks in a to-do list
def show_tasks(list_name):
    curz.execute(f"SELECT * FROM {list_name}")
    tasks = curz.fetchall()
    resp = f"Tasks in {list_name}: \n"
    for task in tasks:
        resp += "- " + str(task[0])+"\n "
    print(resp)
    return resp


# Define the function to create a mysql database
def create_database(database_name):
    try:
        # Use the cursor to execute a mysql command to create the database
        cursor.execute(f"CREATE DATABASE {database_name}")
        # Close the cursor and mysql connection
        cursor.close()
        mydb.close()
        return f"Database {database_name} created successfully"
    except:
        return "Failed to create database"
        pass


# Define the function to create a mysql table
def create_table(database_name, table_name):
    try:
        cursor.execute(f"USE {database_name}")
        # Use the cursor to execute a mysql command to create the table
        cursor.execute(f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT)")
        return f"Table {table_name} created successfully in database {database_name}"
        # Close the cursor and mysql connection
        cursor.close()
        mydb.close()

    except mysql.connector.Error as error:
        return f"Failed to create table: {error}"

# Define the function to insert a record into a mysql table
# Function to execute commands
def execute_command(command):
    try:
        # Split command
        command_parts = command.split()

        # Extract table name and data
        table_name = command_parts[2]
        data = command.split("set ")[1]
        data = data.replace("'", "")
        data = data.split(",")
        data = [x.strip() for x in data]

        # Create query
        query = f"UPDATE {table_name} SET "
        for item in data:
            item_parts = item.split("=")
            query += f"{item_parts[0]} = '{item_parts[1]}', "
        query = query[:-2] # remove the last comma and space
        query += f" WHERE {command_parts[4]} = '{command_parts[6]}'"

        # Execute query
        cursor.execute(query)
        mydb.commit()

        return f"Record updated successfully in table {table_name}"

    except Exception as e:
        return f"Failed to update record: {e}"

def transcribe_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source) 
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)


with open("steal.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def show_messages(text):
    # display chat history
    messages_str = [
    f'<div class="chat-message {"user" if _["role"]=="user" else "system"}"><div class="chat-message-content">{_["content"]}</div></div><br>' for _ in st.session_state["messages"][1:]]
    chat_history = f'<div id="chat-history" class="chat-history">{" ".join(messages_str)}</div><br>'
    text.markdown(chat_history, unsafe_allow_html=True)



BASE_PROMPT = [{"role": "system", "content": "You are a helpful assistant."}]

if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT

#st.header("Cleo 🧠")
text = st.empty()
show_messages(text)

tes_running = False

prompt = st.text_input("",placeholder="Enter your message here..." )

response = ""

if st.button("Ayeeee"):
        prompt = transcribe_audio()
if prompt:
    with st.spinner("Generating response..."):
        st.session_state["messages"] += [{"role": "user", "content": prompt}]

        # Check if the prompt is a question
        st.session_state["messages"] += [{"role": "system", "content": "Hmm... Let me think.."}]
        show_messages(text)
        time.sleep(1)

        # Check if the command is to open an app
        # Check if the prompt contains the word "open" and an application name
        if "op:" in prompt:
            app_name = prompt.split("op: ")[1]
            response += "Opening " + app_name + "..."
            open_app(app_name)

        # Check if the prompt is to set a reminder
        elif "rem:" in prompt:
            response += "Setting up reminder..."
            reminder_prompt = prompt.split("rem: ")[1]
            reminder_parts = reminder_prompt.split(" at ")
            if len(reminder_parts) == 2:
                reminder_str, time_str = reminder_parts
                set_reminder(time_str, reminder_str)
            else:
                response += "Invalid reminder format. Please provide a reminder and time."

        # Check if the prompt is to set a timer
        elif "tim:" in prompt:
            response += "Setting up timer..." 
            duration_str = entities[entities.index("timer") + 1]
            duration = int(duration_str)
            set_timer(duration)

        # Check if the prompt is to search on Google, YouTube, Spotify, or Wikipedia
        elif "surf:" in prompt:
            response += "Searching on Google..."
            search_str = prompt.split("surf: ")[1]
            search_url = "https://www.google.com/search?q=" + search_str
            # open the URL in a new tab
            webbrowser.open_new_tab(search_url)
        elif "vid:" in prompt:
            response += "Searching on YouTube..."
            search_str = prompt.split("vid: ")[1]
            search_url = "https://www.youtube.com/results?search_query=" + search_str
            # open the URL in a new tab
            webbrowser.open_new_tab(search_url)
        elif "sp:" in prompt:
            response += "Searching on Spotify..."
            search_str = prompt.split("sp: ")[1]
            search_url = "https://open.spotify.com/search/" + search_str
            # open the URL in a new tab
            webbrowser.open_new_tab(search_url)
        elif "wiki:" in prompt:
            response += "Searching on Wikipedia..."
            search_str = prompt.split("wiki: ")[1]
            search_url = "https://en.wikipedia.org/wiki/" + search_str
            # open the URL in a new tab
            webbrowser.open_new_tab(search_url)
        elif "play:" in prompt:
            split_prompt = prompt.split(": ")
            if len(split_prompt) == 2:
                media_type = split_prompt[1].split()[0]
                search_str = split_prompt[1].split()[1:]
                search_str = " ".join(search_str)

                if media_type == "song":
                    response += "Playing it on Spotify..."
                    # Add code to play the song on Spotify using the search_str
                    
                    # Initialize Spotipy client credentials
                    client_credentials_manager = SpotifyClientCredentials(client_id='your_client_id', client_secret='your_client_secret')
                    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
                    
                    # Search for the song on Spotify
                    results = sp.search(q=search_str, type='track', limit=1)
                    if results['tracks']['items']:
                        song_uri = results['tracks']['items'][0]['uri']
                        # Add code to play the song using the song_uri
                
                elif media_type == "video":
                    response = "Playing it on YouTube..."

                    # Search for the video on YouTube
                    search_url = "https://www.youtube.com/results?search_query=" + search_str

                    # Open the URL in a new tab
                    webbrowser.open_new_tab(search_url)
                else:
                    response = "Invalid media type. Please specify 'video/song'."
            else:
                response = "Invalid prompt format. Please use 'play: <media_type> <search_string>'."

        elif "sudoku" in prompt:
            response += "Opening the game..."
            sudoku()

        # Check if the prompt is to perform a speed test
        elif "speedtest" in prompt:
            response = check_internet_speed()

        else:
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Cleo, a helpful cat assistant, created by Jaideep!"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": "a8a6c43cfdmsh303fe224450a8cbp1e6c35jsnc06fa427c031",
                "X-RapidAPI-Host": "openai80.p.rapidapi.com"
            }

            response = requests.post(url, json=payload, headers=headers).json()["choices"][0]["message"]["content"]

        st.session_state["messages"][-1]["content"] = response
        show_messages(text)

if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
'''
        # Check if the prompt is to use a to-do list
        elif "td" in prompt:
            if "tdcte:" in prompt:
                todo_list_name = entities[entities.index("named") + 1]
                response += create_todo_list(todo_list_name)
            elif "tdadd:" in prompt:
                todo_list_name = entities[entities.index("to") + 1]
                todo_item = entities[entities.index("add") + 1]
                response += add_task(todo_list_name, todo_item)
            elif "delete" in actions:
                if "from" in entities:
                    todo_list_name = entities[entities.index("from") + 1]
                    todo_item = int(entities[entities.index("delete") + 1])
                    response += delete_task(todo_list_name, todo_item)
                else:
                    todo_item = int(entities[entities.index("delete") + 1])
                    response += delete_todo_list(todo_item)
            elif "show" in actions:
                if "from" in entities:
                    todo_list_name = entities[entities.index("from") + 1]
                    response += show_tasks(todo_list_name)
                else:
                    response += show_todo_lists()
            elif "edit" in actions and "from" in entities:
                todo_list_name = entities[entities.index("from") + 1]
                todo_item = int(entities[entities.index("edit") + 1])
                new_item = entities[entities.index("to") + 1]
                edit_task(todo_list_name, todo_item, new_item)
        # Check if the prompt is to create a MySQL database or table
        if any(entity in entities for entity in ["database", "table"]):
            if "create" in actions:
                # Check if the prompt is to create a table
                if "table" in entities:
                    database_name = entities[entities.index("database") + 1]
                    table_name = entities[entities.index("table") + 1]
                    response += create_table(database_name, table_name)
                # Check if the prompt is to create a database
                elif "database" in entities:
                    database_name = entities[entities.index("database") + 1]
                    response += create_database(database_name)
            elif any(entity in entities for entity in ["show", "all"]):
                # Check if the prompt is to show all databases or tables
                if "database" in entities:
                    cursor.execute("SHOW DATABASES")
                    ctr = 0
                    response += "Showing all databases...\n"
                    for ctr, x in enumerate(cursor, start=1):
                        response += "Database {} {}\n".format(ctr, x[0])
                elif "tables" in entities:
                    database_name = entities[entities.index("from") + 1]
                    cursor.execute("USE {}".format(database_name))
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()

                    # Printing the output
                    response += "Tables in {} database:\n".format(database_name)
                    response += "{:<20}{}\n".format("Table Name", "Rows")
                    for table in tables:
                        cursor.execute("SELECT COUNT(*) FROM {}".format(table[0]))
                        row_count = cursor.fetchone()[0]
                        response += "{:<20}{}\n".format(table[1], row_count)
            elif "delete" in actions:
                # Check if the prompt is to delete a database or table
                if "database" in entities:
                    cursor.execute("DROP DATABASE " + entities[entities.index("database") + 1])
                    response = "Database deleted successfully!"
                elif "table" in entities:
                    database_name = entities[entities.index("database") + 1]
                    table_name = entities[entities.index("table") + 1]
                    cursor.execute("DROP TABLE IF EXISTS " + database_name + "." + table_name)
                    response = "Table deleted successfully!"
            elif "edit" in actions:
                # Check if the prompt is to edit a database or table
                if "database" in entities:
                    database_name = entities[entities.index("database") + 1]
                    new_database_name = entities[entities.index("to") + 1]
                    cursor.execute("ALTER DATABASE " + database_name + " RENAME TO " + new_database_name)
                    response = "Database edited successfully!"
                elif "table" in entities:
                    table_name = entities[entities.index("table") + 1]
                    new_table_name = entities[entities.index("to") + 1]
                    database_name = entities[entities.index("database") + 1]
                    cursor.execute(f"USE {database_name}")
                    cursor.execute("ALTER TABLE " + table_name + " RENAME TO " + new_table_name)
                    response = "Table edited successfully!"
            elif "insert" in actions:
                # Extract database name, table name, and data from prompt
                database_name = entities[entities.index("database") + 1]
                table_name = entities[entities.index("table") + 1]
                data = prompt.split("values (")[1].split(")")[0].split(",")
                data = tuple([x.strip().replace("'", "") for x in data])

                # Use the database
                cursor.execute(f"USE {database_name}")

                # Execute the SQL query to insert data
                quer = f"INSERT INTO {table_name} VALUES {data}"
                cursor.execute(quer)

                # Commit the changes to the database
                mydb.commit()

                # Print success message
                response = "{} record(s) inserted. Data inserted successfully!".format(cursor.rowcount)
            elif "select" in actions:
                # The prompt is to select data from a table
                database_name = entities[entities.index("database") + 1]
                table_name = entities[entities.index("from") + 1]
                data = entities[entities.index("data") + 1]
                data = data.replace("'", "").replace(" ", "").split(",")
                data = tuple([x.strip() for x in data])

                cursor.execute(f"USE {database_name}")
                cursor.execute("SELECT * FROM " + table_name + " WHERE " + data[0] + " = " + data[1])

                result = cursor.fetchall()
                response = "Showing data from table {}...\n".format(table_name)
                for x in result:
                    response += str(x) + "\n"
            elif "update" in actions:
                response = execute_command(prompt)'''
        


        