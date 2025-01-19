# app/api/routes.py

from flask import Flask, request, jsonify, render_template
from app.core.llm_handler import ask_llm
import ollama


def create_routes(app):
    """ 
    Function to refactor the routes in the app.
    
    """
    print("Creating routes...")
    @app.route('/')
    def home():
        """
        Home route.
        """
        #Fetch list of models
        models = ollama.list()['models']
        model_names = [model['name'] for model in models]


        print("Home route") # Debugging
        return render_template('index.html', models=model_names)
    



    @app.route('/ask', methods=['POST'])
    def ask():
        """ 
        Endpoint to ask the model a question.
        """    
        
        data = request.json
        prompt = data.get('prompt')
        model_name = data.get('model_name', 'llama3.2:latest') # Default model
        
        if not prompt:
            return jsonify({'error': 'Prompt is required.'}), 400
        
        response = ask_llm(prompt, model_name)
        return jsonify({'response': response})