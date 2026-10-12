import bleach

def sanitize_input(text: str | None) -> str | None:
    """Видаляє будь-які HTML-теги та скрипти з введеного користувачем тексту."""
    if not text:
        return text
    # Видаляємо всі теги, залишаємо лише чистий текст
    return bleach.clean(text, tags=[], attributes={}, strip=True)