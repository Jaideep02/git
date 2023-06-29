import streamlit as st
import streamlit.components.v1 as components
import time
import requests
import speech_recognition as sr
import pygame
import threading
import os
import mysql.connector
import tkinter as tk
import speedtest
import sqlite3
import pyttsx3
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.gui.sudoku_gui import GUI

st.set_page_config(page_title="Cleo 🧠", page_icon="sphere.png")
st.markdown('<h1 class="cleo">Cleo 🧠</h1>', unsafe_allow_html=True)

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://images.unsplash.com/photo-1687560466164-1eeddb3b119b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_bg_hack_url()
# Initialize the pyttsx3 engine
engine = pyttsx3.init()
# Set the voice ID to a female voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


if "disabled" not in st.session_state:
    st.session_state["disabled"] = False


# Set up the mysql connection
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="jai25",
        database="cleo",
)
# Create a cursor object to execute mysql commands
cursor = mydb.cursor()

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



#                                  ''' ### Opening app ### '''
# Define the function to open the app
def open_app(app_name):
    try:
        os.startfile(app_name)
    except FileNotFoundError:
        response = f"Could not find {app_name}."




#                                  ''' ### Speedtest ### '''
# Define the function to check the internet speed
def check_internet_speed():
    try:
        st = speedtest.Speedtest()
        return "Your download speed is: "+str(round(st.download() / 1000000, 3))+"Mbps! \n Your upload speed is: "+str(round(st.upload() / 1000000, 3))+"Mbps! \n Woww, Pretty fast!"
    except:
        return "Couldn't check the speed."




#                                  ''' ### Timer ### '''
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



#                                  ''' ### Reminder ### '''
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





#                                  ''' ### Sudoku ### '''
# Define the function to create a sudoku puzzle
def sudoku_thread():
    root = tk.Tk()
    root.geometry("1690x845")
    root.configure(background='#c6c8df')
    root.title("Sudoku Puzzle")

    Game = GUI(root)
    Game.generate_sudoku_board()
    Game.right_side_option_block()

    root.mainloop()

def sudoku():
    threading.Thread(target=sudoku_thread).start()




#                                  ''' ###Todo LISTS### '''

# Define a function to create a new todo list
def create_todo_list(name):
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()

        # Check if the table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,))
        existing_table = cursor.fetchone()

        if existing_table:
            return f"Todo list '{name}' already exists."
        else:
            # Create a new table for the todo list
            cursor.execute(f"CREATE TABLE {name} (id INTEGER PRIMARY KEY, task TEXT)")
            conn.commit()
            conn.close()
            return f"Todo list '{name}' created successfully."
    except:
        return f"Please try again later... Server unreachable"
# Define a function to add a task to a todo list
def add_task(todo_list, task):
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()

        # Insert the task into the specified todo list
        cursor.execute(f"INSERT INTO {todo_list} (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
        return f"Task '{task}' added to '{todo_list}'."
    except:
        return f"Please try again later... Server unreachable"
# Define a function to edit a task in a todo list
def edit_task(todo_list, task_id, new_task):
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()

        # Update the specified task in the specified todo list
        cursor.execute(f"UPDATE {todo_list} SET task=? WHERE id=?", (new_task, task_id))
        conn.commit()
        conn.close()
        return f"Task '{task_id}' in '{todo_list}' updated successfully."
    except:
        return f"Please try again later... Server unreachable"
# Define a function to delete a task from a todo list
def delete_task(todo_list, task_id):
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()

        # Delete the specified task from the specified todo list
        cursor.execute(f"DELETE FROM {todo_list} WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        return f"Task '{task_id}' deleted from '{todo_list}'."
    except:
        return f"Please try again later... Server unreachable"
# Define a function to delete a todo list
def delete_todo_list(name):
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()

        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,))
        existing_table = cursor.fetchone()

        if existing_table:
            # Delete the todo list table
            cursor.execute(f"DROP TABLE {name}")
            conn.commit()
            conn.close()
            return f"Todolist '{name}' deleted successfully."
        else:
            conn.close()
            return f"Todolist '{name}' does not exist."
    except:
        return f"Please try again later... Server unreachable"
# Define a function to show all the todo lists
def show_todo_lists():
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()

        # Get all table names in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        if tables:
            todo_lists = [table[0] for table in tables]
            conn.close()
            return "Todo lists: " + ", ".join(todo_lists)
        else:
            conn.close()
            return "No todo lists found."
    except:
        return "Please try again later... Server unreachable"
# Define a function to show all the tasks in a todo list
def show_tasks(list_name):
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()

        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (list_name,))
        existing_table = cursor.fetchone()

        if existing_table:
            # Retrieve and display all tasks in the specified todo list
            cursor.execute(f"SELECT id, task FROM {list_name}")
            tasks = cursor.fetchall()
            conn.close()

            if tasks:
                task_list = [f"ID: {task[0]}, Task: {task[1]}" for task in tasks]
                return "\n".join(task_list)
            else:
                return "No tasks found in the todo list."
        else:
            conn.close()
            return f"Todo list '{list_name}' does not exist."
    except:
        return "Please try again later... Server unreachable"


#                                  ''' ### Audio ### '''
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


text = st.empty()
show_messages(text)
# Create an empty placeholder for the input box
input_placeholder = st.empty()

tes_running = False

prompt = st.text_input("Purr:", key="input_text",
    disabled=st.session_state.disabled)

response = ""

if st.button("Ayeeee"):
        prompt = transcribe_audio()
if prompt:
    input_placeholder.empty()
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
            duration_str = prompt.split("tim: ")
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
        elif "vid: " in prompt:
            response = "Playing it on YouTube..."
            # Search for the video on YouTube
            search_str = prompt.split("vid: ")[1]
            search_url = "https://www.youtube.com/results?search_query=" + search_str
            # Open the URL in a new tab
            webbrowser.open_new_tab(search_url)



        elif "sudoku" in prompt:
            response += "Opening the game..."
            sudoku()



        # Check if the prompt is to perform a speed test
        elif "speedtest" in prompt:
            response = check_internet_speed()




        # Check if the prompt is to use a to-do list
        elif "td: " in prompt:
            if "td: create " in prompt:
                todo_list_name = prompt.split("td: create ")[1]
                response += create_todo_list(todo_list_name)
            elif "td: add " in prompt:
                task = prompt.split("add")[1].split("to")[0].strip()
                todo_list_name = prompt.split("to")[1].strip()
                response += add_task(todo_list_name, task)
            elif "td: del " in prompt:
                if "fr" in prompt:
                    task = prompt.split("del")[1].split("fr")[0].strip()
                    todo_list_name = prompt.split("fr")[1].strip()
                    response += delete_task(todo_list_name, task)
                else:
                    todo_item = prompt.split("del")[1].strip()
                    response += delete_todo_list(todo_item)
            elif "td: show" in prompt:
                if "lst" in prompt:
                    todo_list_name = prompt.split("lst")[1].strip()
                    response += show_tasks(todo_list_name)
                else:
                    response += show_todo_lists()
            elif "td: edit " in prompt:
                # Extract the task, new task, and todo list name
                task = prompt.split("edit")[1].split("to")[0].strip()
                new_task = prompt.split("to")[1].split("in")[0].strip()
                todo_list_name = prompt.split("in")[1].strip()
                edit_task(todo_list_name, task, new_task)


        elif "mysql:" in prompt:
            query = prompt.split("mysql: ")[1]
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                mydb.commit()
                response = result
            except mysql.connector.Error as error:
                response = f"Error executing MySQL query: {error}"



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