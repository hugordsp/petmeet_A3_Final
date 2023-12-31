from flask import Flask, render_template, request, url_for, redirect, session, flash
import jwt
import requests

app = Flask(__name__)
app.secret_key = '123456'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    # Envie os dados de login para a sua API usando requests
    login_url = 'http://127.0.0.1:5000/users/login'
    response = requests.post(login_url, json={'Email': email, 'Senha': senha})

    if response.ok:
        user_data = response.json()
        access_token = user_data.get('access_token')
        user_name = user_data.get('user_name')  # Adicione esta linha para obter o nome do usuário
        if access_token and user_name:
            # Restante do código...
            session['user_name'] = user_name  # Adicione este usuário à sessão
            return render_template('main.html', user_name=user_name)
        else:
            flash('Usuário ou senha incorretos', 'error')  # Flash message de erro
            return redirect(url_for('index'))  # Redirecione de volta para a página inicial

    flash('Erro ao efetuar login', 'error')  # Flash message de erro
    return redirect(url_for('index'))  # Redirecione de volta para a página inicial


# Adicione uma rota para a página 'main.html'
@app.route('/main')
def main():
    user_name = session.get('user_name')
    return render_template('main.html', user_name=user_name)

from flask import redirect, url_for

@app.route('/cadastro', methods=['POST'])
def cadastro():
    # Obtendo dados do formulário
    first_name = request.form['first_name']
    email = request.form['email']
    new_password = request.form['new_password']

    # Montando payload para enviar à API
    payload = {
        'Nome': first_name,
        'Email': email,
        'Senha': new_password,
    }

    # Enviando solicitação à API
    api_url = 'http://127.0.0.1:5000/users/create'
    response = requests.post(api_url, json=payload)

    if response.status_code == 201:
        user_data = response.json()
        user_id = user_data.get('ID')
        return redirect(url_for('index'))
    else:
        # Tratamento de erro, você pode renderizar uma página de erro, por exemplo.
        return 'Error during registration.'

    
@app.route('/logout')
def logout():
    # Limpar os dados da sessão
    session.pop('user_name', None)
    # Redirecionar de volta para a página de login
    return redirect(url_for('index'))    

if __name__ == '__main__':
    app.run(debug=True, port=8000)
