from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Liste de clés OpenAI
openai_keys = [
    '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',
    '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',
    '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'
]

# Configuration de l'API OpenAI avec la première clé
openai.api_key = openai_keys[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_code', methods=['POST'])
def generate_code():
    description = request.form['description']
    model = request.form['model']  # Récupérer le modèle sélectionné
    creativity = float(request.form['creativity'])  # Récupérer le niveau de créativité
    code = generate_code_from_description(description, model, creativity)
    return render_template('result.html', code=code)


def generate_code_from_description(description, model, creativity):
    # Essayer chaque clé jusqu'à ce qu'une fonctionne
    for key in openai_keys:
        try:
            # Configuration de l'API OpenAI avec la clé actuelle
            openai.api_key = key

            # Utilisation de l'API OpenAI GPT pour générer du code à partir de la description
            response = openai.ChatCompletion.create(
                model=model,  # Utiliser le modèle sélectionné
                messages=[
                    {"role": "system", "content": "You are a code generation assistant."},
                    {"role": "user", "content": description}
                ],
                max_tokens=1000,             # Limite de tokens pour la réponse
                temperature=creativity,      # Contrôle la créativité de la réponse
                n=1,                        # Nombre de réponses à générer
                stop=None                   # Condition pour arrêter la génération de texte
            )

            # Récupérer le code généré à partir de la réponse
            if 'choices' in response and len(response['choices']) > 0:
                generated_code = response['choices'][0]['message']['content'].strip()
            else:
                generated_code = "Erreur lors de la génération du code."

            # Si aucune exception n'est levée, retourner le code généré
            return generated_code

        except openai.OpenAIError as e:
            print(f"Erreur avec la clé {key}: {e}")

    # Si aucune clé ne fonctionne, retourner un message d'erreur
    return "Impossible de générer le code avec les clés fournies."

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)