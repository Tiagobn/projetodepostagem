from shutil import posix

#with app.app_context():  # criando o banco de dados
#    database.create_all()


# with app.app_context():
#     usuario = Usuario(username="Tiago", email='tiago@gmail.com', senha="654321")
#     usuario2 = Usuario(username="joao",email="joao@gmail.com",senha="123456")
#
#     database.session.add(usuario)
#     database.session.add(usuario2)
#
#     database.session.commit()
#

# with app.app_context():
#     usuario_teste = Usuario.query.filter_by(email="joao@gmail.com").first()
#     print(usuario_teste)
#     print(usuario_teste.posts)

# with app.app_context():
#     meu_post = Post(titulo="meu primeiro  post" , corpo="estou fazendo um  teste de postagem " , id_usuario=2)
#     database.session.add(meu_post)
#     database.session.commit()

# with app.app_context():
#     post = Post.query.first()
#     print(post)
#     print(post.autor.email)
#     print(post.titulo)


# deleting and creating the test database again

# with app.app_context():
#     database.drop_all()
#     database.create_all()
#

