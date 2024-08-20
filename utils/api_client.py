import requests
from config import max_tokens

def analyze_document_with_openai(prompt):
    try:
        base_url = "http://localhost:1234/v1"
        headers = {
            "Authorization": "Bearer lm-studio",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }
        
        response = requests.post(f"{base_url}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"LM Studio API error: {str(e)}"