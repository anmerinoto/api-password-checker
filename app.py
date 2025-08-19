from zxcvbn import zxcvbn
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def check_contraseña_politica(password):
    politicas = {
        "longitud_minima": len(password) >= 12,
        "tiene_mayusculas": bool(re.search(r'[A-Z]', password)),
        "tiene_minusculas": bool(re.search(r'[a-z]', password)),
        "tiene_digito": bool(re.search(r'[0-9]', password)),
        "tiene_caracter_especial": bool(re.search(r'[@$!%*?&]', password))
    }
    return politicas

@app.route("/password/check", methods=["POST"])
def check_password():
    data = request.get_json()
    password = data.get("password", "")

    # Análisis con zxcvbn
    analysis = zxcvbn(password)
    policies = check_contraseña_politica(password)

    # Traducción de score
    score_text = {
        0: "Muy débil",
        1: "Débil",
        2: "Aceptable",
        3: "Fuerte",
        4: "Muy fuerte"
    }

    # Respuesta simplificada en español
    response = {
        "contraseña": password,
        "nivel_seguridad": score_text.get(analysis["score"], "Desconocido"),
        "tiempo_estimado_crackeo": analysis["crack_times_display"]["offline_fast_hashing_1e10_per_second"],
        "sugerencias": analysis["feedback"]["suggestions"],
        "advertencia": analysis["feedback"]["warning"],
        "politicas": policies,
        "cumple_politicas": all(policies.values())
    }

    return jsonify(response)
@app.route('/api/info')
def info():
    return jsonify({
        'nombre': 'Microservicio Base - Tratamiento de Datos Paralelo A',
        'version': '1.0.0',
        'descripcion': 'Este microservicio realiza validaciones de contraseñas para sitios web',
        'autor': 'GRUPO 11'
    })

if __name__ == "__main__":
    app.run(debug=True)
