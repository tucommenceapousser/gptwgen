from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Liste des clés OpenAI
openai_keys = [
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
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
