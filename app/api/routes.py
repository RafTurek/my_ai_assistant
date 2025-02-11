# app/api/routes.py

from flask import Flask, request, jsonify, render_template
from app.core.llm_handler import ask_llm
import ollama
import json
import os
from os import path


CHAT_HISTORY_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'chat_history.json')

def load_chat_history():
    """ 
    Load chat history from a file and ensure consistent structure.
    """
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # If the data is a dictionary, ensure that all values are lists
            if isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], dict):  # If the value is a dictionary, convert it to a list
                        data[key] = list(data[key].values())[0] if data[key] else []
                    elif not isinstance(data[key], list):  # If the value is not a list, convert it to a list
                        data[key] = []
                return data
            elif isinstance(data, list):  # If the data is a list, return it as the default chat history
                return {'default': data}
            else:  # In case the data is not a list or a dictionary, return an empty chat history
                return {'default': []}
        except json.JSONDecodeError:
            print("Error: chat_history.json is not a valid JSON file.")
            return {'default': []}
    else:
        print("Chat history file not found. Creating a new one.")
        return {'default': []}


def save_chat_history(chat_history):
    """ 
    Save chat history to a file.
    """
    try:
        os.makedirs(path.dirname(CHAT_HISTORY_FILE), exist_ok=True)
        # Upewnij się, że chat_history jest słownikiem, a każdy klucz ma listę jako wartość
        if not isinstance(chat_history, dict):
            chat_history = {'default': chat_history}
        for key in chat_history:
            if not isinstance(chat_history[key], list):
                chat_history[key] = []
        with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(chat_history, f, ensure_ascii=False, indent=4)
        print(f"Chat history saved: {chat_history}")  # Debugging
    except Exception as e:
        print(f"Error saving chat history: {e}")



def create_routes(app):
    """ 
    Function to refactor the routes in the app.
    
    """
    global chat_history
    chat_history = load_chat_history()  # Load chat history at the start of each session
    
    @app.route('/')
    def home():
        """
        Home page with webinterface.
        """
        global chat_history
        chat_history = load_chat_history()  # Ładujemy historię przy każdej sesji

        #Fetch list of models
        models = ollama.list()['models']
        model_names = [model['name'] for model in models]

        #Debug chat_history 
        print("Chat history:", chat_history)


        chat_topics = list(chat_history.keys())

        print("Loaded chat history:", chat_history)  # Debugowanie

        return render_template(
                            'index.html',
                            models=model_names,
                            chat_history=chat_history,
                            chat_topics=chat_topics,
                            message = None
                            ) # Render the index.html template
    



    @app.route('/ask', methods=['POST'])
    def ask():
        """ 
        Endpoint to ask the model a question.
        """    
        global chat_history # Use the global chat history
        chat_history = load_chat_history()  # Ensure chat history is loaded

        data = request.json
        prompt = data.get('prompt')
        model_name = data.get('model_name', 'llama3.2:latest') # Default model
        chat_topic = data.get('chat_topic', 'default') # Default chat topic
        
        if not prompt:
            return jsonify({'error': 'Prompt is required.'}), 400
        
        # Create a new chat topic if it doesn't exist
        if chat_topic not in chat_history:
            chat_history[chat_topic] = []
        
        # Add the user's question to the chat history
        chat_history[chat_topic].append({
            'role': 'user',
            'content': prompt,
            'model': model_name
            })
        
        # Get the model's response
        try:
            print(f"Sending prompt to model: {model_name}") # Debugging
            response = ask_llm(prompt, model_name)
            print(f"Model response: {response}") # Debugging
        except Exception as e:
            print(f"Error asking model: {e}") # Debugging
            return jsonify({'error': str(e)}), 500

        # Add the model's response to the chat history
        chat_history[chat_topic].append({
            'role': 'assistant',
            'content': response,
            'model': model_name
            })
        

        # Save the chat history
        save_chat_history(chat_history)



        return jsonify({
            'response': response,
            'chat_history': chat_history[chat_topic],
            'chat_topic': chat_topic
            })
    
    @app.route('/clear_history', methods=['POST'])
    def clear_history():
        """ 
        Endpoint to clear the chat history.
        """
        global chat_history # Use the global chat history
        chat_history = load_chat_history()  # Ensure chat history is loaded
        chat_topic = request.json.get('chat_topic', 'default') # Default chat topic

        if chat_topic in chat_history:
            chat_history[chat_topic] = [] # Remove the chat topic
            save_chat_history(chat_history) # Save the chat history
        
        return jsonify({'status': 'success', 'message' : f'Chat history for {chat_topic} cleared.'})
    
    @app.route('/switch_chat', methods=['POST'])
    def switch_chat():
        """
        Endpoint to switch the chat topic.
        """
        global chat_history
        chat_history = load_chat_history()  # Ensure chat history is loaded
        chat_topic = request.json.get('chat_topic', 'default') # Default chat topic


        # Fetch the chat history for the chat topic
        history = chat_history.get(chat_topic, [])

        return jsonify({
            'chat_history': history,
            'chat_topic': chat_topic
            })

        # return jsonify({'message': 'Chat history cleared.'})