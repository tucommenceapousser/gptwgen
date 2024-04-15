from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Liste de clés OpenAI
openai_keys = [
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
    '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',
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
