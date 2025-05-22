from app import create_app  # importa a função create_app do __init__.py da pasta app

app = create_app()  # cria a instância da aplicação com todas as rotas, serviços e integrações

if __name__ == '__main__':
    app.run(debug=True)
