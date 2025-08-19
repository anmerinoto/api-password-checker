from zxcvbn import zxcvbn
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def check_contraseña_politica(password):
    politicas = {
        "min_length": len(password) >= 12,
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "lowercase": bool(re.search(r'[a-z]', password)),
        "digit": bool(re.search(r'[0-9]', password)),
        "special_char": bool(re.search(r'[@$!%*?&]', password))
    }
    return politicas

@app.route("/check_contraseña", methods=["POST"])
def check_contraseña():
    data = request.get_json()
    password = data.get("password", "")

    
    analysis = zxcvbn(password)

    
    policies = check_contraseña_politica(password)

    response = {
        "password": password,
        "score": analysis["score"],  # 0 a 4
        "guesses": analysis["guesses"],
        "crack_times_display": analysis["crack_times_display"],
        "feedback": analysis["feedback"],
        "policies": policies,
        "policies_passed": all(policies.values())
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
