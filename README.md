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
