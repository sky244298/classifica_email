-Classificador de Emails com IA

Esta aplicação web foi desenvolvida para auxiliar uma empresa do setor financeiro a automatizar a leitura de emails, classificando-os em produtivos ou improdutivos e sugerindo respostas automáticas adequadas a cada caso. A solução recebe textos digitados ou arquivos .txt e .pdf, envia o conteúdo para um modelo de linguagem (OpenAI GPT) e retorna a categoria e uma resposta pronta para uso.

A interface web é simples: o usuário seleciona um arquivo ou cola o conteúdo do email, clica em “Classificar” e visualiza a categoria atribuída e a resposta sugerida. O objetivo é reduzir o tempo gasto pela equipe com tarefas repetitivas de triagem e resposta inicial.

Tecnologias utilizadas

A aplicação foi construída em Python com Flask para o backend e HTML/CSS para a interface. O processamento de arquivos PDF é feito com a biblioteca pdfplumber. A classificação e a geração de respostas usam a API da OpenAI (modelo gpt-4.1-mini), com um pequeno mecanismo de fallback baseado em palavras-chave caso a chamada à API falhe. As dependências principais estão listadas em requirements.txt.

-Como executar localmente

Para rodar a aplicação em ambiente local é necessário ter Python instalado.

1-Clonar o repositório e entrar na pasta do projeto (onde estão app.py, requirements.txt, templates/ e static/).

2-Criar um ambiente virtual (opcional, mas recomendado) e instalar as dependências:
      pip install -r requirements.txt

3-Configurar a variável de ambiente com a chave da OpenAI:

No Windows (PowerShell):
    setx OPENAI_API_KEY "sua_chave_aqui"

4-Iniciar o servidor Flask:
    python app.py

5-Acessar o endereço exibido no terminal, em geral http://127.0.0.1:5000, em um navegador.

-Funcionamento da solução

Quando um email é enviado pela interface, o backend extrai o texto (de arquivo .txt, .pdf ou da caixa de texto), e chama a função classify_email. Essa função tenta classificar o conteúdo usando o modelo da OpenAI com o prompt preparado para retornar apenas “Produtivo” ou “Improdutivo”. Em seguida, a função suggest_reply gera uma resposta automática com tom profissional, adaptada à categoria: se o email for produtivo, a resposta reconhece o pedido e informa que o caso está em análise; se for improdutivo, agradece a mensagem e encerra de forma cordial. Caso a chamada à API falhe, o código utiliza uma lógica simples baseada em palavras-chave para decidir a categoria e fornece respostas padrão.

-Deploy na nuvem

A aplicação foi implantada no Render como um Web Service em Python 3. O serviço lê o código diretamente do repositório GitHub, instala as dependências via requirements.txt e expõe a aplicação Flask em uma URL pública. A chave da OpenAI foi configurada no painel do Render como variável de ambiente OPENAI_API_KEY, permitindo o uso da API de IA sem expor o segredo no código fonte.
Pode ser acessada aqui:
            https://classifica-email-krnh.onrender.com



-AI-Based Email Classifier

This web application was developed to help a financial-sector company automate the reading of emails by classifying them as either productive or unproductive and generating an appropriate automatic reply. The system accepts text input or .txt/.pdf files, sends the content to an OpenAI GPT model, and returns both the classification and a suggested response.

The web interface is simple: the user uploads a file or pastes the email content, clicks “Classify,” and receives the assigned category and an auto-generated response. The goal is to reduce the team’s time spent on repetitive triage and initial responses.

-Technologies Used

The application is built in Python using Flask for the backend and HTML/CSS for the interface. PDF processing is handled with the pdfplumber library. Classification and reply generation are performed via the OpenAI API (gpt-4.1-mini) with a keyword-based fallback mechanism in case the API call fails. All dependencies are listed in the requirements.txt file.

-How to Run Locally

To run the project locally, Python must be installed.

1-Clone the repository and enter the project folder (where app.py, requirements.txt, templates/, and static/ are located).

2-(Optional but recommended) Create a virtual environment and install dependencies:

            pip install -r requirements.txt


3-Set the environment variable with your OpenAI API key:

Windows (PowerShell):

            setx OPENAI_API_KEY "your_key_here"


4-Start the Flask server:

            python app.py


5-Open the displayed address in your browser (usually http://127.0.0.1:5000
).

-How the Application Works

When an email is submitted, the backend extracts the text (from a .txt/.pdf file or from the text box) and calls the classify_email function. This function attempts to classify the content using the OpenAI model with a prompt designed to return only “Produtivo” or “Improdutivo.” Then, the suggest_reply function generates a professional automatic response based on the classification. If the API request fails, the system falls back to a simple keyword-based rule and provides default responses.

-Cloud Deployment

The application was deployed on Render as a Python Web Service. Render pulls the code directly from the GitHub repository, installs the dependencies from requirements.txt, and exposes the Flask application at a public URL. The OpenAI API key was added in Render’s dashboard as the environment variable OPENAI_API_KEY, ensuring the secret is not exposed in the source code.

Live application:
https://classifica-email-krnh.onrender.com
