from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import openai

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API OpenAI depuis le fichier .env
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_code', methods=['POST'])
def generate_code():
    description = request.form['description']
    model = request.form['model']  # ex : gpt-4, gpt-3.5-turbo
    creativity = float(request.form['creativity'])  # Niveau de température (0.0 à 1.0)
    code = generate_code_from_description(description, model, creativity)
    return render_template('result.html', code=code)

def generate_code_from_description(description, model, creativity):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a code generation assistant."},
                {"role": "user", "content": description}
            ],
            max_tokens=1000,
            temperature=creativity,
            n=1
        )

        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['message']['content'].strip()
        else:
            return "Erreur : aucune réponse générée."

    except openai.OpenAIError as e:
        print(f"Erreur OpenAI : {e}")
        return "Erreur lors de la génération du code."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
