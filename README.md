# api-password-checker
Proyecto para analizar la fortaleza de contraseñas para sitios web. GRUPO 11
#
# validators.py 
#
Dentro del proyecto api-password-checker es un módulo que permite validar la fortaleza de contraseñas y retornar resultados estandarizados. 
#
## Funciones
El módulo expone tres funciones (todas realizan la misma validación): 
- validate_password(password: str) -> dict 
- check_password(password: str) -> dict 
- is_strong_password(password: str) -> dict
#
## Cada función devuelve un diccionario con los siguientes campos: 
-  "passed": true, # True si la contraseña pasa las validaciones 
-  "errors": [], # Lista de problemas encontrados 
-  "score": 5, # Puntaje de 0 a 6 "strength": "medium", # "weak" | "medium" | "strong" 
-  "length": 9, # Longitud de la contraseña 
-  "has_upper": true, 
-  "has_lower": true, 
-  "has_digit": true, 
-  "has_special": true
#
## Reglas implementadas 
Longitud mínima: 
-  ideal ≥ 12 caracteres (2 puntos), 
-  aceptable ≥ 10 (1 punto). 
Debe incluir al menos: 
-  una mayúscula, 
-  una minúscula, 
-  un dígito 
-  y un carácter especial. 
Evitar:
-  contraseñas comunes (123456, password, qwerty, etc.). 
-  secuencias predecibles (1234, abcd, qwer). 
-  repeticiones (aaa111!!!). 
Clasificación con fuerza (strength): 
-  weak (<4), 
-  medium (4–5), 
-  strong (≥6).