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
    Load chat history from a file.
    
    """
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # If the data is not list, return dictionary

        if not isinstance(data, list):
            return {'default': data}
        return data
    return {} 
            


def save_chat_history(chat_history):
    """ 
    Save chat history to a file.
    
    """
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(CHAT_HISTORY_FILE), exist_ok=True)

    #make sure the chat history is a dictionary
    if not isinstance(chat_history, dict):
        chat_history = {'default': chat_history} # Use 'default' as the key

    # Save the chat history to a file
    with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=4)

# Load chat history
chat_history = load_chat_history()
if not isinstance(chat_history, dict):
    chat_history = {'default': chat_history}



def create_routes(app):
    """ 
    Function to refactor the routes in the app.
    
    """
    
    @app.route('/')
    def home():
        """
        Home page with webinterface.
        """
        #Fetch list of models
        models = ollama.list()['models']
        model_names = [model['name'] for model in models]

        #Debug chat_history 
        print("Chat history:", chat_history)


        chat_topics = list(chat_history.keys())



        return render_template('index.html', models=model_names, chat_history=chat_history,chat_topics=chat_topics) # Render the index.html template
    



    @app.route('/ask', methods=['POST'])
    def ask():
        """ 
        Endpoint to ask the model a question.
        """    
        global chat_history # Use the global chat history

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
        chat_history.append({
            'role': 'user',
            'content': prompt,
            'model': model_name
            })
        
        # Get the model's response
        response = ask_llm(prompt, model_name)

        # Add the model's response to the chat history
        chat_history.append({
            'role': 'model',
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
        chat_topic = request.json.get('chat_topic', 'default') # Default chat topic

        if chat_topic in chat_history:
            chat_history.pop(chat_topic) # Remove the chat topic
            save_chat_history(chat_history) # Save the chat history
        
        return jsonify({'status': 'success', 'message' : f'Chat history for {chat_topic} cleared.'})
    
    @app.route('/switch_chat', methods=['POST'])
    def switch_chat():
        """
        Endpoint to switch the chat topic.
        """
        global chat_history
        chat_topic = request.json.get('chat_topic', 'default') # Default chat topic


        # Fetch the chat history for the chat topic
        history = chat_history.get(chat_topic, [])

        return jsonify({
            'chat_history': history,
            'chat_topic': chat_topic
            })

        # return jsonify({'message': 'Chat history cleared.'})