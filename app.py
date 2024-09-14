from flask import Flask
from models import db, MateriaPrima, ProdutoAcabado, consumo


app = Flask(__name__)
app.config.from_object('config.Config')

# Inicializar o SQLAlchemy com a aplicação
db.init_app(app)

# Importar modelos para registrar com o SQLAlchemy
from routes.main_routes import main as main_blueprint
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() # Cria as tabelas no banco de dados
    app.run(debug=True)