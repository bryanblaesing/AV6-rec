from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

pontuacoes = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    player_name = request.form['player_name']
    return redirect(url_for('jogo', nome=player_name))

@app.route('/jogo/<nome>')
def jogo(nome):
    return render_template('jogo.html', nome=nome, pontuacoes=pontuacoes)

@app.route('/submit_score', methods=['POST'])
def submit_score():
    player_name = request.form['player_name']
    score = int(request.form['score'])
    pontuacoes.append({'nome': player_name, 'pontuacao': score})
    return 'Pontuação enviada com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)
