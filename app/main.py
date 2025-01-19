#app/main.py

from app.core.llm_handler import ask_llm
import ollama

def choose_model():
    """ 
    Choose a model to use for the chatbot.
    
    """

    # Get a list of available models
    models = ollama.list()['models']
    if not models:
        print("No models available.")
        return None

# Print the available models
    print("Available models:")
    for model in models:
        print(f" - {model['name']}")

# Ask the user to choose a model
    while True:
        try:
            choice = int(input("Choose a model (1, 2, 3, ...): "))
            if 1 <= choice <= len(models):
                return models[choice - 1]['name']
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid choice. Please try again.")



def main():
    print("Welcome to the LLM Chatbot!")
    model_name = choose_model() # Choose a model
    print(f"Using model: {model_name}")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        response = ask_llm(user_input)
        print(f"LLM: {response}")


if __name__ == "__main__":
    main()