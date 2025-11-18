from flask import Flask, render_template, request
import pdfplumber
from openai import OpenAI
import os

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

def classify_with_gpt(text):
    prompt = f"""Você é um assistente especializado em classificar emails para uma empresa do setor financeiro.

Sua tarefa é classificar o email em EXATAMENTE uma destas categorias:

**PRODUTIVO**: Emails que requerem ação, resposta ou acompanhamento da empresa:
- Solicitações de serviços financeiros (abertura de conta, empréstimos, cartões)
- Dúvidas sobre produtos financeiros ou serviços da empresa
- Problemas técnicos com sistemas, apps ou plataformas
- Reclamações legítimas sobre serviços prestados
- Solicitação de suporte, atendimento ou esclarecimentos
- Consultas sobre faturas, cobranças ou transações
- Pedidos de cancelamento, alteração ou atualização de dados

**IMPRODUTIVO**: Emails que NÃO requerem ação da empresa:
- SPAM (propaganda não solicitada, ofertas suspeitas, phishing)
- Mensagens de felicitações, agradecimentos genéricos
- Emails enviados por engano ou para destinatário errado
- Correntes, piadas, conteúdo pessoal não relacionado
- Marketing de outras empresas ou produtos não relacionados
- Emails vazios ou sem conteúdo relevante
- Notificações automáticas de outras plataformas
- Assuntos completamente fora do escopo financeiro

Email para classificar:
\"\"\"
{text}
\"\"\"

INSTRUÇÕES IMPORTANTES:
1. Analise o conteúdo COMPLETO do email
2. Considere se o email está relacionado aos serviços da empresa financeira
3. Verifique se há uma solicitação legítima ou necessidade de resposta
4. Identifique sinais de spam (links suspeitos, ofertas milagrosas, formatação estranha)
5. Responda APENAS com uma palavra: "Produtivo" ou "Improdutivo"

Resposta:"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    
    raw = response.output_text.strip().lower()
    
    # Análise mais rigorosa da resposta
    if "improdutivo" in raw:
        return "Improdutivo"
    elif "produtivo" in raw and "improdutivo" not in raw:
        return "Produtivo"
    else:
        # Se a resposta for ambígua, aplica filtro adicional
        return apply_spam_filter(text)

def apply_spam_filter(text):
    """Filtro adicional para detectar spam e conteúdo irrelevante"""
    text_lower = text.lower()
    
    # Indicadores fortes de spam/improdutivo
    spam_indicators = [
        "ganhe dinheiro rápido", "clique aqui", "oferta imperdível",
        "parabéns você ganhou", "prêmio", "loteria", "herança",
        "príncipe nigeriano", "transferência internacional urgente",
        "viagra", "remédio", "emagrecer", "dieta milagrosa",
        "trabalhe em casa", "renda extra garantida", "sem investimento",
        "bitcoin grátis", "criptomoeda grátis", "dólar grátis"
    ]
    
    spam_count = sum(1 for indicator in spam_indicators if indicator in text_lower)
    
    # Se encontrar 2 ou mais indicadores de spam
    if spam_count >= 2:
        return "Improdutivo"
    
    # Indicadores de emails produtivos legítimos
    productive_indicators = [
        "minha conta", "não consigo acessar", "problema com",
        "gostaria de solicitar", "preciso de ajuda", "dúvida sobre",
        "como faço para", "não recebi", "cobrança indevida",
        "atualizar cadastro", "cancelar", "contratar", "consultar saldo"
    ]
    
    productive_count = sum(1 for indicator in productive_indicators if indicator in text_lower)
    
    # Se tiver indicadores produtivos, classifica como produtivo
    if productive_count >= 1:
        return "Produtivo"
    
    # Em caso de dúvida, verifica tamanho e estrutura
    # Emails muito curtos (menos de 20 caracteres) tendem a ser improdutivos
    if len(text.strip()) < 20:
        return "Improdutivo"
    
    # Default mais conservador: improdutivo
    return "Improdutivo"

def reply_with_gpt(category, text):
    prompt = f"""Você está ajudando uma empresa do setor financeiro a responder emails.

Categoria do email: {category}

Email original:
\"\"\"
{text}
\"\"\"

Gere uma resposta automática profissional em português do Brasil adequada à categoria:

- Se for PRODUTIVO: 
  * Responda de forma cordial e profissional
  * Reconheça o pedido/problema mencionado no email
  * Informe que a solicitação está sendo analisada
  * Dê uma estimativa genérica de prazo (ex: "em breve", "nas próximas 48h")
  * Ofereça canal de contato caso necessário

- Se for IMPRODUTIVO:
  * Agradeça brevemente pela mensagem
  * Seja educado mas objetivo
  * Não prolongue a resposta

REGRAS IMPORTANTES:
- Use tom profissional mas amigável
- NÃO invente: números de protocolo, dados pessoais, prazos específicos
- Seja conciso (máximo 4-5 linhas)
- Use parágrafos curtos
- Assine como "Equipe de Atendimento"

Resposta:"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return response.output_text.strip()

def classify_email(text):
    """Usa o GPT para classificar o email com fallback melhorado"""
    try:
        return classify_with_gpt(text)
    except Exception as e:
        print("Erro ao classificar com GPT:", e)
        # Em caso de erro, usa o filtro de spam
        return apply_spam_filter(text)

def suggest_reply(category, text):
    """Usa o GPT para sugerir resposta automática"""
    try:
        return reply_with_gpt(category, text)
    except Exception as e:
        print("Erro ao gerar resposta com GPT:", e)
        if category == "Produtivo":
            return (
                "Olá!\n\n"
                "Recebemos sua mensagem e nossa equipe já está analisando sua solicitação. "
                "Retornaremos em breve com uma resposta.\n\n"
                "Atenciosamente,\n"
                "Equipe de Atendimento"
            )
        else:
            return (
                "Olá!\n\n"
                "Agradecemos seu contato.\n\n"
                "Atenciosamente,\n"
                "Equipe de Atendimento"
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
    app.run(debug=True)
