from flask import Flask, render_template, request, redirect, url_for
import spacy
import database

app = Flask(__name__)

# Inicializa o banco de dados
database.init_db()

# Carrega o modelo do spaCy para português
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    import os
    os.system("python -m spacy download pt_core_news_sm")
    nlp = spacy.load("pt_core_news_sm")

# Léxico simples de polaridade para demonstração em PLN baseada em regras/features
PALAVRAS_POSITIVAS = {
    "bom", "ótimo", "excelente", "maravilhoso", "gostei", "adorei", "recomendo", 
    "perfeito", "feliz", "rápido", "atencioso", "qualidade", "satisfeito"
}
PALAVRAS_NEGATIVAS = {
    "ruim", "péssimo", "hororoso", "odiei", "lento", "caro", "problema", 
    "defeito", "insatisfeito", "pior", "atrasado", "horrível", "fraude"
}

def analisar_sentimento(texto):
    doc = nlp(texto.lower())
    pontuacao = 0.0
    tokens_uteis = 0

    for token in doc:
        # Ignora stopwords e pontuações para focar nas palavras de conteúdo
        if not token.is_stop and not token.is_punct:
            tokens_uteis += 1
            if token.lemma_ in PALAVRAS_POSITIVAS:
                pontuacao += 1.0
            elif token.lemma_ in PALAVRAS_NEGATIVAS:
                pontuacao -= 1.0

    # Normalização simples da polaridade
    if tokens_uteis > 0:
        polaridade = pontuacao / tokens_uteis
    else:
        polaridade = 0.0

    if polaridade > 0:
        sentimento = "Positivo"
    elif polaridade < 0:
        sentimento = "Negativo"
    else:
        sentimento = "Neutro"

    return sentimento, round(polaridade, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        texto_cliente = request.form.get("comentario", "").strip()
        if texto_cliente:
            sentimento, polaridade = analisar_sentimento(texto_cliente)
            database.salvar_comentario(texto_cliente, sentimento, polaridade)
        return redirect(url_for("index"))

    historico = database.listar_historico()
    return render_template("index.html", historico=historico)

if __name__ == "__main__":
    app.run(debug=False)
    