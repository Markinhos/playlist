from app.models.user import User

def insert_user(username, password):
    user = User(username, password)
    return user.save()
