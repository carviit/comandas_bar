from flask import Flask, request, jsonify, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:0404@localhost/comandas_bar'
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Chave secreta para a sessão

db = SQLAlchemy(app)

# Modelo de Funcionário
class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    cargo = db.Column(db.String(100))
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha_hash = db.Column(db.String(400), nullable=False)

    def __init__(self, nome, cargo, usuario, senha):
        self.nome = nome
        self.cargo = cargo
        self.usuario = usuario
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

# Modelo de Mesa
class Mesa(db.Model):
    __tablename__ = 'mesas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(100), default='aberta')
    total = db.Column(db.Float, default=0)
    data_abertura = db.Column(db.String(100), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    data_fechamento = db.Column(db.String(100), nullable=True)

    def __init__(self, numero):
        self.numero = numero
        self.status = 'aberta'

# Modelo de Produto
class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    preco = db.Column(db.Float, nullable=False)

# Modelo de Itens Consumidos
class ItensConsumidos(db.Model):
    __tablename__ = 'itens_consumidos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesas.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

# Criar tabelas no banco de dados
with app.app_context():
    db.create_all()

# Página de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    mensagem = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        funcionario = Funcionario.query.filter_by(usuario=usuario).first()

        if funcionario and funcionario.verificar_senha(senha):
            session['funcionario_id'] = funcionario.id
            return redirect(url_for('index'))
        else:
            mensagem = 'Usuário ou senha inválidos'

    return render_template('login.html', mensagem=mensagem)

# Rota de Logout
@app.route('/logout')
def logout():
    session.pop('funcionario_id', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'funcionario_id' in session:
        funcionario = Funcionario.query.get(session['funcionario_id'])
        # Filtra apenas as mesas com status "aberta"
        mesas = Mesa.query.filter_by(status='aberta').order_by(Mesa.numero).all()
        return render_template('index.html', funcionario=funcionario, mesas=mesas)
    else:
        return redirect(url_for('login'))
        
# Criar uma nova mesa
@app.route('/criar_mesa', methods=['POST'])
def criar_mesa():
    data = request.json
    nova_mesa = Mesa(numero=data['numero'])
    db.session.add(nova_mesa)
    db.session.commit()
    return jsonify({"mensagem": "Mesa criada com sucesso!", "mesa_id": nova_mesa.id})



# Excluir uma mesa
@app.route('/excluir_mesa/<int:mesa_id>', methods=['DELETE'])
def excluir_mesa(mesa_id):
    mesa = Mesa.query.get(mesa_id)
    if mesa:
        ItensConsumidos.query.filter_by(mesa_id=mesa_id).delete()  
        db.session.delete(mesa)
        db.session.commit()
        return jsonify({"mensagem": "Mesa excluída com sucesso!"})
    return jsonify({"erro": "Mesa não encontrada"}), 404

# Exibir produtos de uma mesa
@app.route('/mesa/<int:mesa_id>/produtos', methods=['GET'])
def produtos_mesa(mesa_id):
    itens = ItensConsumidos.query.filter_by(mesa_id=mesa_id).all()
    produtos = [
        {
            "id": item.produto_id,
            "quantidade": item.quantidade,
            "nome": Produto.query.get(item.produto_id).nome
        } for item in itens
    ]
    return jsonify(produtos)

# Excluir um item da mesa
@app.route('/mesa/<int:mesa_id>/remover_produto/<int:produto_id>', methods=['DELETE'])
def remover_produto_mesa(mesa_id, produto_id):
    item = ItensConsumidos.query.filter_by(mesa_id=mesa_id, produto_id=produto_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"mensagem": "Produto removido da mesa!"})
    return jsonify({"erro": "Produto não encontrado na mesa"}), 404

@app.route('/mesa/<int:mesa_id>/alterar_quantidade/<int:produto_id>', methods=['PUT'])
def alterar_quantidade(mesa_id, produto_id):
    data = request.json
    nova_quantidade = data.get("quantidade", 1) 
    item = ItensConsumidos.query.filter_by(mesa_id=mesa_id, produto_id=produto_id).first()
    
    if item:
        item.quantidade = nova_quantidade
        db.session.commit()
        return jsonify({"mensagem": "Quantidade atualizada com sucesso!"})
    
    return jsonify({"erro": "Produto não encontrado na mesa"}), 404

@app.route('/mesa/<int:mesa_id>/adicionar_produto', methods=['POST'])
def adicionar_produto_mesa(mesa_id):
    data = request.get_json()
    produto_id = data.get('produto_id')
    quantidade = data.get('quantidade', 1)

   
    item = ItensConsumidos.query.filter_by(mesa_id=mesa_id, produto_id=produto_id).first()
    
    if item:
       
        item.quantidade += int(quantidade)
    else:
       
        novo_item = ItensConsumidos(
            mesa_id=mesa_id,
            produto_id=produto_id,
            quantidade=quantidade
        )
        db.session.add(novo_item)

    db.session.commit()

    return jsonify({"mensagem": "Produto adicionado com sucesso!"})

# Rota para a página de produtos
@app.route('/produtos', methods=['GET'])
def produtos():

    if 'funcionario_id' not in session:
        return redirect(url_for('login'))
    
    funcionario = Funcionario.query.get(session['funcionario_id'])

    if funcionario.cargo != 'Gerente':
        return redirect(url_for('index'))
    
    produtos = Produto.query.order_by(Produto.nome).all()
    return render_template('produtos.html', funcionario=funcionario, produtos=produtos)
    
# Rota para cadastrar um novo produto (envia dados via POST)
@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    if 'funcionario_id' not in session:
        return redirect(url_for('login'))
    
    funcionario = Funcionario.query.get(session['funcionario_id'])
    if funcionario.cargo != 'Gerente':
        return redirect(url_for('index'))
    
    nome = request.form['nome']
    preco = request.form['preco']
    
    try:
        preco = float(preco)
    except ValueError:
        return "Preço inválido", 400
    
    novo_produto = Produto(nome=nome, preco=preco)
    db.session.add(novo_produto)
    db.session.commit()
    
    return redirect(url_for('produtos'))

@app.route('/buscar_produtos', methods=['GET'])
def buscar_produtos():
    produtos = Produto.query.all()
    lista_produtos = []
    for p in produtos:
        lista_produtos.append({
            "id": p.id,
            "nome": p.nome
        })
    return jsonify(lista_produtos)

# Rota para editar produto (via POST, sem renderizar template)
@app.route('/editar_produto/<int:produto_id>', methods=['POST'])
def editar_produto(produto_id):
    produto = Produto.query.get(produto_id)
    if not produto:
        return "Produto não encontrado", 404
        
    produto.nome = request.form['nome']
    try:
        produto.preco = float(request.form['preco'])
    except ValueError:
        return "Preço inválido", 400
    db.session.commit()
    return "Produto atualizado", 200

@app.route('/mesa/<int:mesa_id>/nota', methods=['GET'])
def nota_mesa(mesa_id):
    mesa = Mesa.query.get(mesa_id)
    if not mesa:
        return jsonify({"erro": "Mesa não encontrada"}), 404
    itens = ItensConsumidos.query.filter_by(mesa_id=mesa_id).all()
    nota_itens = []
    total = 0
    for item in itens:
        produto = Produto.query.get(item.produto_id)
        subtotal = produto.preco * item.quantidade
        total += subtotal
        nota_itens.append({
            "nome": produto.nome,
            "preco": produto.preco,
            "quantidade": item.quantidade,
            "subtotal": subtotal
        })
    return jsonify({"itens": nota_itens, "total": total, "mesa_numero": mesa.numero})

@app.route('/mesa/<int:mesa_id>/fechar', methods=['PUT'])
def fechar_mesa(mesa_id):
    mesa = Mesa.query.get(mesa_id)
    if not mesa:
        return jsonify({"erro": "Mesa não encontrada"}), 404
    mesa.status = "fechada"
    mesa.data_fechamento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.commit()
    return jsonify({"mensagem": "Mesa fechada com sucesso!"})

@app.route('/cadastrar_funcionario', methods=['POST'])
def cadastrar_funcionario():
    if 'funcionario_id' not in session:
        return redirect(url_for('login'))

    funcionario_logado = Funcionario.query.get(session['funcionario_id'])

    if funcionario_logado.cargo != 'Gerente':
        return redirect(url_for('index'))

    nome = request.form['nome']
    cargo = request.form['cargo']
    usuario = request.form['usuario']
    senha = request.form['senha']


    if Funcionario.query.filter_by(usuario=usuario).first():
        return "Usuário já existe", 400

    novo_funcionario = Funcionario(nome, cargo, usuario, senha)
    db.session.add(novo_funcionario)
    db.session.commit()

    return redirect(url_for('funcionarios'))

@app.route('/funcionarios', methods=['GET'])
def funcionarios():
    if 'funcionario_id' not in session:
        return redirect(url_for('login'))
    
    funcionario_logado = Funcionario.query.get(session['funcionario_id'])

    if funcionario_logado.cargo != 'Gerente':
        return redirect(url_for('index'))
    
    funcionarios_list = Funcionario.query.order_by(Funcionario.nome).all()
    return render_template('funcionarios.html', 
                           funcionario=funcionario_logado, 
                           funcionarios=funcionarios_list)

# Rota para a página de relatórios (acesso apenas para Gerentes)
@app.route('/relatorios', methods=['GET'])
def relatorios():
    if 'funcionario_id' not in session:
        return redirect(url_for('login'))
    
    funcionario_logado = Funcionario.query.get(session['funcionario_id'])

    if funcionario_logado.cargo != 'Gerente':
        return redirect(url_for('index'))
    
    return render_template('relatorios.html', funcionario=funcionario_logado)

@app.route('/dados_vendas', methods=['GET'])
def dados_vendas():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    from datetime import datetime, timedelta

    if start_date and end_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Formato de data inválido."}), 400


        delta = (end_dt - start_dt).days
        labels = []
        sales = []
        for i in range(delta + 1):
            current_date = start_dt + timedelta(days=i)
            labels.append(current_date.strftime('%Y-%m-%d'))
        
            sales.append(1000 + i * 100)  
    else:

        today = datetime.today()
        labels = []
        sales = []
        for i in range(5):
            current_date = today - timedelta(days=4 - i)
            labels.append(current_date.strftime('%d-%m-%y'))
            sales.append(1200 + i * 50)
            
    return jsonify({"labels": labels, "sales": sales})


if __name__ == '__main__':
    app.run(debug=True)


