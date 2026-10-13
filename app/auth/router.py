from app.crypto.encryption import blind_index # Додай цей імпорт нагорі

# ... всередині def register(...):
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Username вже зайнятий")

    # Шифротекст Fernet щоразу різний → шукаємо за сліпим індексом (HMAC)
    if db.query(User).filter(User.email_index == blind_index(user_data.email)).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Email вже зареєстровано")