from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Tabela de associação para a relação muitos-para-muitos com quantidade com quantidade consumida

consumo = db.Table('consumo',
    db.Column('produto_id', db.Integer, db.ForeignKey('produto_acabado.id'), primary_key=True),
    db.Column('materia_prima_id', db.Integer, db.ForeignKey('materia_prima.id'), primary_key=True),
    db.Column('quantidade_consumida', db.Float, nullable=False)
)

class MateriaPrima(db.Model):
    __tablename__ = 'materia_prima'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    quantidade = db.Column(db.Float, nullable=False) # Quantidade em estoque

    def __repr__(self):
        return f"<MateriaPrima {self.nome}>"


class ProdutoAcabado(db.Model):
    __tablename__ = 'produto_acabado'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    quantidade = db.Column(db.Float, nullable=False) # Quantidade em estoque
    materias_primas = db.relationship('MateriaPrima', secondary=consumo, backref=db.backref('produtos_acabados', lazy='dynamic'))

    def __repr__(self):
        return f"<ProdutoAcabado {self.nome}>"