from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from models import db, MateriaPrima, ProdutoAcabado, consumo

main = Blueprint('main', __name__)

# Página Inicial
@main.route('/')
def index():
    return render_template('index.html')

# --- Rotas para Matérias-Primas ---

# Listar Matérias-Primas
@main.route('/materias_primas')
def listar_materias_primas():
    materias = MateriaPrima.query.all()
    return render_template('materias_primas/listar.html', materias=materias)

# Adicionar Matéria-Prima
@main.route('/materias_primas/adicionar', methods=['GET', 'POST'])
def adicionar_materia_prima():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        nova_materia = MateriaPrima(nome=nome, quantidade=quantidade)
        try:
            db.session.add(nova_materia)
            db.session.commit()
            flash('Matéria-Prima adicionada com sucesso!', 'success')
            return redirect(url_for('main.listar_materias_primas'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao adicionar Matéria-Prima.', 'danger')
    return render_template('materias_primas/adicionar.html')

# Editar Matéria-Prima
@main.route('/materias_primas/editar/<int:id>', methods=['GET', 'POST'])
def editar_materia_prima(id):
    materia = MateriaPrima.query.get_or_404(id)
    if request.method == 'POST':
        materia.nome = request.form['nome']
        materia.quantidade = request.form['quantidade']
        try:
            db.session.commit()
            flash('Matéria-Prima atualizada com sucesso!', 'success')
            return redirect(url_for('main.listar_materias_primas'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar Matéria-Prima', 'danger')
    return render_template('materias_primas/editar.html', materia=materia)

# Deletar Matéria-Prima

@main.route('/materias_primas/deletar/<int:id>', methods=['POST'])
def deletar_materia_prima(id):
    materia = MateriaPrima.query.get_or_404(id)
    try:
        db.session.delete(materia)
        db.session.commit()
        flash('Matéria-Prima deletada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao deletar Matéria-Prima.', 'danger')
    return redirect(url_for('main.listar_materias_primas'))

# --- Rotas para Produtos Acabados ---

# Listar Produtos Acabados 
@main.route('/produtos_acabados')
def listar_produtos_acabados():
    try:
        produtos = ProdutoAcabado.query.all()    
        
        # Criar uma lista para armazenar produtos e seus consumos
        produtos_consumo=[]

        # Iterar sobre os produtos para buscar as quantidade de matérias-primas consumidas
        for produto in produtos:
            materias_consumidas = []
            for materia in produto.materias_primas:            
                # Obter a quantidade consumida
                valor = db.session.query(consumo.c.quantidade_consumida).filter(
                    consumo.c.produto_id == produto.id,
                    consumo.c.materia_prima_id == materia.id
                ).first()[0]
                
                # Adicionar à lista de matérias-primas consumidas
                materias_consumidas.append({
                    'nome': materia.nome,
                    'quantidade_consumida': valor,
                })

            # Adicionar à lista de produtos e seus consumos
            produtos_consumo.append({
                'produto': produto, # passando o nome do produto
                'materias_consumidas': materias_consumidas
            })
        # Passar a lista de produtos seus consumos para o template
        return render_template('produtos_acabados/listar.html', produtos_consumo=produtos_consumo)
    except Exception as e:
        # Logar o erro para depuração
        print(f"Erro ao buscar produtos: {e}")
        return render_template('produtos_acabados/listar.html', produtos_consumo=[])

# Adicionar Produtos Acabado
@main.route('/produtos_acabados/adicionar', methods=['GET', 'POST'])
def adicionar_produto_acabado():
    materias = MateriaPrima.query.all()
    if request.method == 'POST':
        nome  = request.form['nome']
        quantidade = request.form['quantidade']
        materia_ids = request.form.getlist('materias_primas') # List de IDs
        quantidades_consumo = request.form.getlist('quantidades_consumo') # Lista de quantidades consumidas
        novo_produto = ProdutoAcabado(nome=nome, quantidade=quantidade)
        try:
            db.session.add(novo_produto)
            db.session.commit()
            # Adicionar relações de consumo
            for materia_id, quantidade_consumo in zip(materia_ids, quantidades_consumo):
                materia = MateriaPrima.query.get(int(materia_id))
                if materia:
                    stmt = consumo.insert().values(produto_id=novo_produto.id, materia_prima_id=materia.id, quantidade_consumida=quantidade_consumo)
                    db.session.execute(stmt)
            db.session.commit()
            flash('Produto Acabado adicionado com sucesso!', 'success')
            return redirect(url_for('main.listar_produtos_acabados'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao adicionar Produto Acabado.', 'danger')
    return render_template('produtos_acabados/adicionar.html', materias=materias)

# Editar Produto Acabado
@main.route('/produtos_acabados/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto_acabado(id):
    produto = ProdutoAcabado.query.get_or_404(id)
    materias = MateriaPrima.query.all()
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.quantidade = request.form['quantidade']
        materia_ids = request.form.getlist('materias_primas')
        quantidades_consumo = request.form.getlist('quantidades_consumo')
        try:
            # Remover relações antigas
            db.session.execute(consumo.delete().where(consumo.c.produto_id == id))
            db.session.commit()
            # Adicionar novas relações
            for materia_id, quantidade_consumo in zip(materia_ids, quantidades_consumo):
                materia = MateriaPrima.query.get(int(materia_id))
                if materia:
                    stmt = consumo.insert().values(produto_id=produto.id, materia_prima_id=materia.id, quantidade_consumida=quantidade_consumo)
                    db.session.execute(stmt) 
            db.session.commit()
            flash('Produto Acabado atualizado com sucesso!', 'success')
            return redirect(url_for('main.listar_produtos_acabados'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar Produto Acabado.', 'danger')
    # Obter as matérias-primas atualmente associadas
    materias_atual = db.session.query(consumo).filter(consumo.c.produto_id == id).all()
    return render_template('produtos_acabados/editar.html', produto=produto, materias=materias, materias_atual=materias_atual)

# Deletar Produto Acabado
@main.route('/produtos_acabados/deletar/<int:id>', methods=['POST'])
def deletar_produto_acabado(id):
    produto = ProdutoAcabado.query.get_or_404(id)
    try:
        db.session.delete(produto)
        db.session.commit()
        flash('Produto Acabado deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao deletar Produto Acabado', 'danger')
    return redirect(url_for('main.listar_produtos_acabados'))








