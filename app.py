import os
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import google.generativeai as genai

# Config API Gemini
API_KEY = "AIzaSyCsW9Dw7RKzI8fwn1VIuroksc-_biFi2Sw"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-flash")

app = Flask(__name__)

def extract_seo_data_from_html_content(html_content):
    """
    Traite le contenu HTML/textuel, génère tags et description SEO.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    content_text = soup.get_text(separator=" ", strip=True)

    prompt_tags = f"""Voici un contenu : "{content_text}"
    Donne-moi une liste de mots-clés (tags) pertinents, séparés par des virgules, sans phrases."""
    tags_text = model.generate_content(prompt_tags).text.strip()

    prompt_desc = f"""Voici un contenu : "{content_text}"
    Génère une description courte, accrocheuse et optimisée pour le référencement, en 150 caractères maximum."""
    description_text = model.generate_content(prompt_desc).text.strip()

    return tags_text, description_text

@app.route("/", methods=["GET", "POST"])
def index():
    tags = None
    description = None
    error_message = None

    if request.method == "POST":
        input_html = request.form.get("htmlcontent", "")
        if input_html.strip() == "":
            error_message = "Le contenu ne peut pas être vide."
        else:
            try:
                tags, description = extract_seo_data_from_html_content(input_html)
            except Exception as e:
                error_message = f"Erreur lors du traitement : {e}"
                print(error_message)

    return render_template("index.html", tags=tags, description=description, error=error_message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)