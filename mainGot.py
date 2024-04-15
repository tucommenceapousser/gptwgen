import openai

# Configuration de l'API OpenAI
openai.api_key = ''

# Fonction pour générer des mots de passe cohérents avec des mots-clés spécifiques
def generate_passwords_with_keywords(keywords, num_passwords):
    passwords = []
    for keyword in keywords:
        prompt = f"Generate {num_passwords} passwords based on the keyword '{keyword}':"
        response = openai.Completion.create(
            engine="davinci-002",
            prompt=prompt,
            max_tokens=50,
            n=num_passwords,
            stop=None,
            temperature=0.7
        )
        passwords.extend([result['text'].strip() for result in response['choices']])
    return passwords

# Mots-clés fournis par l'utilisateur
keywords = ['hacker', 'pwn', 'anon', '2024']
# Nombre de mots de passe à générer pour chaque mot-clé
num_passwords_per_keyword = 5

# Générer des mots de passe cohérents avec des mots-clés spécifiques
passwords = generate_passwords_with_keywords(keywords, num_passwords_per_keyword)

# Afficher les mots de passe de manière stylisée
print("Generated Passwords:")
print("--------------------")
for password in passwords:
    print(f"| {password.ljust(20)} |")
print("--------------------")