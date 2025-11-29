from app import create_app, db
from app.models.user import Usuario

app = create_app()

with app.app_context():
    username = "admin"
    password = "admin123"

    user = Usuario(
        username=username,
        role="ADMIN",
        is_active=True,
        autorizado=True
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    print("Usuario creado:", username)
