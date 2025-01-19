#app/core/llm_handler.py    

import ollama
from tqdm import tqdm
import time

def ask_llm(prompt, model_name ='llama3.2:latest'):
    """ 
    Ask LLM a question and return the answer.

    Parameters:
    prompt (str): The question to ask the model.
    model_name (str): The model to use. Default is llama3.2:latest
    return (str): The answer from the model.
    """
    try:
        print(f"Generating response...(model: {model_name})")
    
        #initialize the progress bar
    
        pbar = tqdm(desc="Generating response", unit="token")

        # variable to store the response
        full_response = ""

        #generate the response with streaming enabled
        stream = ollama.generate(model=model_name, prompt=prompt, stream=True)
        for chunk in stream:
            if "response" in chunk:
                full_response += chunk["response"]
                pbar.update(1)

        pbar.close() # close the progress bar
        return full_response
    except Exception as e:
        print(f"Error: {e}")
        return None    


    # try:
    #     # Simulate a progress bar
    #     print("Processing...")
    #     for _ in tqdm(range(100)):
    #         time.sleep(0.01)
    #     print("Done!")



    #     response = ollama.generate(model=model_name, prompt=prompt)
    #     return response['response']
    # except Exception as e:
    #     print(f"Error: {e}")
    #     return None
    
    