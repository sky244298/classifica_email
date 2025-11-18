from flask import Flask, render_template, request
import pdfplumber
from openai import OpenAI
import os

# Configure o cliente da OpenAI.


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


app = Flask(__name__)

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def classify_with_gpt(text):  # Envia o conteúdo do email para o modelo GPT e retorna "Produtivo" ou "Improdutivo".
    ...
    prompt = f"""
Você é um assistente que classifica emails para uma empresa do setor financeiro.

Classifique o email a seguir como exatamente uma destas opções:
- Produtivo
- Improdutivo

Email:
\"\"\"{text}\"\"\"

Responda apenas com UMA palavra: Produtivo ou Improdutivo.
"""
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    raw = response.output_text.strip()
    if "produtivo" in raw.lower():
        return "Produtivo"
    if "improdutivo" in raw.lower():
        return "Improdutivo"
    # fallback caso venha algo inesperado
    return "Produtivo"

def reply_with_gpt(category, text): # Gera uma resposta automática em português com base na categoria e no texto original. 
    prompt = f"""
Você está ajudando uma empresa do setor financeiro a responder emails.

Categoria do email: {category}

Email original:
\"\"\"{text}\"\"\"

Gere uma resposta automática profissional em português do Brasil adequada à categoria:
- Se for Produtivo: responda de forma cordial, reconhecendo o pedido e explicando que o caso será analisado ou está em andamento.
- Se for Improdutivo: responda de forma simpática, agradecendo a mensagem (por exemplo, felicitações, agradecimentos) e encerrando de forma educada.

Importante:
- Escreva em tom profissional, simples e claro.
- Não invente número de protocolo nem dados pessoais.
- Formate com parágrafos curtos.
"""
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return response.output_text.strip()

def classify_email(text):
    """
    Usa o GPT para classificar o email.
    """
    try:
        return classify_with_gpt(text)
    except Exception as e:
        print("Erro ao classificar com GPT:", e)
        text_lower = text.lower()
        keywords_produtivo = [
            "suporte", "problema", "erro", "chamado", "atualização",
            "status", "pendente", "urgente", "ajuda", "reclamação"
        ]
        for kw in keywords_produtivo:
            if kw in text_lower:
                return "Produtivo"
        return "Improdutivo"

def suggest_reply(category, text):
    """
    Usa o GPT para sugerir resposta automática.
    """
    try:
        return reply_with_gpt(category, text)
    except Exception as e:
        print("Erro ao gerar resposta com GPT:", e)
        if category == "Produtivo":
            return (
                "Olá! 👋\n\n"
                "Recebemos sua mensagem e ela já está em análise pela nossa equipe. "
                "Em breve retornaremos com uma atualização sobre o seu caso.\n\n"
                "Atenciosamente,\nEquipe de Atendimento"
            )
        else:
            return (
                "Olá! 😊\n\n"
                "Agradecemos sua mensagem. Não é necessário nenhum retorno adicional neste momento.\n\n"
                "Um abraço,\nEquipe de Atendimento"
            )

@app.route("/", methods=["GET", "POST"])
def index():
    category = None
    reply = None
    original_text = None

    if request.method == "POST":
        uploaded_file = request.files.get("file")
        email_text = request.form.get("email_text", "").strip()

        if uploaded_file and uploaded_file.filename != "":
            filename = uploaded_file.filename.lower()
            if filename.endswith(".txt"):
                original_text = uploaded_file.read().decode("utf-8", errors="ignore")
            elif filename.endswith(".pdf"):
                original_text = extract_text_from_pdf(uploaded_file)
            else:
                original_text = "Formato de arquivo não suportado. Use .txt ou .pdf."
        elif email_text:
            original_text = email_text
        else:
            original_text = ""

        if original_text:
            category = classify_email(original_text)
            reply = suggest_reply(category, original_text)

    return render_template(
        "index.html",
        category=category,
        reply=reply,
        original_text=original_text
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

