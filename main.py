import google.generativeai as genai
from bs4 import BeautifulSoup

# === Étape 1 : Configuration de l'API Gemini ===
API_KEY = "AIzaSyCsW9Dw7RKzI8fwn1VIuroksc-_biFi2Sw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# === Étape 2 : Lire le fichier HTML source ===
filename = "index.html"
with open(filename, "r", encoding="utf-8") as f: 
    soup = BeautifulSoup(f, "html.parser")

# === Étape 3 : Extraire le texte visible pour générer les tags ===
content_text = soup.get_text(separator=" ", strip=True)

# === Étape 4 : Générer les tags avec Gemini ===
prompt = f"""
Voici un contenu : "{content_text}"

Donne-moi une liste de mots-clés (tags) pertinents, séparés par des virgules, sans phrases.
"""
response = model.generate_content(prompt)
tags_text = response.text.strip()

# === Étape 5 : Créer une description courte (150 caractères) ===
description_text = content_text[:150]

# === Étape 6 : Ajouter les balises SEO dans <head> ===

# Ajouter <meta name="description">
if not soup.find("meta", attrs={"name": "description"}):
    meta_desc = soup.new_tag("meta", attrs={"name": "description", "content": description_text})
    soup.head.append(meta_desc)

# Ajouter <meta name="keywords">
if not soup.find("meta", attrs={"name": "keywords"}):
    meta_keywords = soup.new_tag("meta", attrs={"name": "keywords", "content": tags_text})
    soup.head.append(meta_keywords)

# === Étape 7 : Réécrire le fichier index.html avec référencement ===
with open(filename, "w", encoding="utf-8") as f:
    f.write(str(soup))

# === Étape 8 : Affichage dans la console ===
print("\n🎯 Tags générés :")
print(tags_text)