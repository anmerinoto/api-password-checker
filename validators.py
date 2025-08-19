# validators.py
import re

# Conjunto mínimo de contraseñas comunes para descartar rápido
_COMMON = {
    "123456", "12345678", "123456789", "password", "qwerty",
    "admin", "letmein", "111111", "1234567890", "abc123",
}

# Caracteres especiales aceptados
_SPECIALS = r"""!@#$%^&*()_+\-=\[\]{};':",.<>/?`~|\\"""

def _evaluate(password: str):
    """Devuelve (ok: bool, detalles: dict) con reglas evaluadas."""
    if not isinstance(password, str):
        return False, {"errors": ["El parámetro debe ser str."], "score": 0}

    errors = []
    score = 0

    # Reglas básicas
    if len(password) >= 12:
        score += 2
    elif len(password) >= 10:
        score += 1
    else:
        errors.append("Longitud mínima recomendada: 10 caracteres (ideal 12+).")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        errors.append("Debe incluir al menos una mayúscula [A-Z].")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        errors.append("Debe incluir al menos una minúscula [a-z].")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        errors.append("Debe incluir al menos un dígito [0-9].")

    if re.search("[" + re.escape(_SPECIALS) + "]", password):
        score += 1
    else:
        errors.append("Debe incluir al menos un carácter especial.")

    # Diccionario simple / patrones obvios
    lower = password.lower()
    if lower in _COMMON or "password" in lower or "qwerty" in lower:
        errors.append("Evita contraseñas comunes u obvias.")

    # Repeticiones y secuencias simples
    if re.search(r"(.)\1{2,}", password):
        errors.append("Evita repetir el mismo carácter 3+ veces seguidas.")

    if re.search(r"(1234|abcd|qwer)", lower):
        errors.append("Evita secuencias previsibles (1234, abcd, qwer).")

    ok = len(errors) == 0 and score >= 4
    detalles = {
        "score": score,            # 0–6
        "passed": ok,
        "errors": errors,
        "length": len(password),
        "has_upper": bool(re.search(r"[A-Z]", password)),
        "has_lower": bool(re.search(r"[a-z]", password)),
        "has_digit": bool(re.search(r"[0-9]", password)),
        "has_special": bool(re.search("[" + re.escape(_SPECIALS) + "]", password)),
    }
    return ok, detalles

def validate_password(password: str, return_details: bool = False):
    ok, details = _evaluate(password)
    return details if return_details else ok

def check_password(password: str, return_details: bool = False):
    ok, details = _evaluate(password)
    return details if return_details else ok

def is_strong_password(password: str, return_details: bool = False):
    ok, details = _evaluate(password)
    return details if return_details else ok

__all__ = ["validate_password", "check_password", "is_strong_password"]
