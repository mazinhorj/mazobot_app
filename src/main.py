from flask import Flask, request, jsonify, render_template
import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import YoutubeLoader
from youtube_transcript_api._errors import NoTranscriptFound

app = Flask(__name__, template_folder='templates')

api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

# Função para gerar a resposta do bot
def resposta_do_bot(mensagens, documento):
    sys_msg = 'Você é um assistente amigável chamado MazoBot. Utilize estas informações para resumir conteúdos de diferentes fontes: {informacoes}.'
    msg_model = [('system', sys_msg)]
    msg_model += mensagens
    template = ChatPromptTemplate.from_messages(msg_model)
    chat = ChatGroq(model='llama-3.3-70b-versatile')
    chain = template | chat
    resposta = chain.invoke({'informacoes': documento}).content
    return resposta

# Funções para resumir conteúdos de diferentes fontes
def resumo_site(url_site):
    loader = WebBaseLoader(url_site)
    lista_docs = loader.load()
    documento = ''
    for doc in lista_docs:
        documento += doc.page_content
    return documento

def resumo_pdf(caminho_ou_url):
    if caminho_ou_url.startswith('http://') or caminho_ou_url.startswith('https://'):
        if not caminho_ou_url.lower().endswith('.pdf'):
            raise ValueError('URL inválida. A URL deve terminar com .pdf.')
    else:
        if not (os.path.exists(caminho_ou_url) and os.path.isfile(caminho_ou_url) and caminho_ou_url.lower().endswith('.pdf')):
            raise ValueError('Caminho inválido ou não é um arquivo PDF.')

    loader = PyPDFLoader(caminho_ou_url)
    lista_docs = loader.load()
    documento = ''
    for doc in lista_docs:
        documento += doc.page_content
    if not documento:
        raise ValueError('Nenhum conteúdo encontrado no PDF.')
    return documento

def resumo_video(url_video):
    try:
        loader = YoutubeLoader.from_youtube_url(
            url_video,
            language=['pt']
        )
        lista_docs = loader.load()
        documento = ''
        for doc in lista_docs:
            documento += doc.page_content
        if not documento:
            raise ValueError('Nenhuma legenda encontrada para o vídeo no idioma português.')
        return documento
    except NoTranscriptFound:
        raise ValueError('Não foi possível encontrar legendas para este vídeo no idioma português.')
    except Exception as e:
        raise ValueError(f'Ocorreu um erro ao tentar carregar as legendas do vídeo: {e}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    source_type = data.get('source_type')
    source_input = data.get('source_input')
    
    documento = ''
    try:
        if source_type == 'site':
            documento = resumo_site(source_input)
        elif source_type == 'pdf':
            documento = resumo_pdf(source_input)
        elif source_type == 'video':
            documento = resumo_video(source_input)
        else:
            return jsonify({'response': 'Tipo de fonte inválido.'}), 400
    except ValueError as e:
        return jsonify({'response': str(e)}), 400

    # Aqui você precisará gerenciar o histórico de mensagens para o chatbot
    # Por simplicidade, vamos apenas usar a última mensagem do usuário e o documento
    mensagens = [('user', user_message)]
    resposta = resposta_do_bot(mensagens, documento)
    
    return jsonify({'response': resposta})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

