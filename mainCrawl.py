import requests
from bs4 import BeautifulSoup
import openai

# Configuration de l'API OpenAI
openai.api_key = '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'

# Fonction pour crawler une page web et extraire les informations pertinentes
def crawl_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Exemple d'extraction d'informations à partir des balises HTML
    names = [tag.get_text().strip() for tag in soup.find_all('span', class_='name')]
    emails = [tag.get_text().strip() for tag in soup.find_all('a', class_='email')]

    return names, emails

# Fonction pour générer une liste de mots de passe à partir des noms et adresses e-mail
def generate_passwords(names, emails):
    passwords = []
    for name, email in zip(names, emails):
        # Pour cet exemple simple, générez des mots de passe en concaténant des parties du nom et de l'e-mail
        password = name.split()[0].lower() + '123'
        passwords.append(password)
        password = email.split('@')[0] + '456'
        passwords.append(password)
    return passwords

# Fonction pour utiliser ChatGPT pour générer une liste de noms d'utilisateur
# Fonction pour utiliser ChatGPT pour générer une liste de noms d'utilisateur
def generate_usernames(names):
    # Utilisez ChatGPT pour générer des noms d'utilisateur basés sur les noms
    # Assurez-vous que la liste `names` ne contient que des noms propres et sans espaces
    prompt = "Generate usernames based on the following names:\n" + "\n".join(names)
    response = openai.Completion.create(
        engine="davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=10,
        stop=None,
        temperature=0.7
    )
    usernames = [result['text'].strip() for result in response['choices']]
    return usernames

# URL de la page à crawler
url = 'https://qanon-france.com'

# Crawler la page
names, emails = crawl_page(url)

# Générer des mots de passe et des noms d'utilisateur à partir des informations extraites
passwords = generate_passwords(names, emails)
usernames = generate_usernames(names)

# Afficher les résultats
print("Usernames generated:")
print(usernames)
print("Passwords generated:")
print(passwords)