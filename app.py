from flask import Flask, request, jsonify
from zxcvbn import zxcvbn
import re

app = Flask(__name__)

# --------- LÓGICA: políticas mínimas ----------
def check_contraseña_politica(password: str) -> dict:
    return {
        "longitud_minima": len(password) >= 12,
        "tiene_mayusculas": bool(re.search(r'[A-Z]', password)),
        "tiene_minusculas": bool(re.search(r'[a-z]', password)),
        "tiene_digito": bool(re.search(r'\d', password)),
        "tiene_caracter_especial": bool(re.search(r'[@$!%*?&!#%&/()=?¿¡*+.,;:_\-]', password))
    }

# --------- API: evaluación ----------
@app.post("/password/check")
def check_password():
    data = request.get_json(silent=True) or {}
    pwd = data.get("password", "")
    if not pwd:
        return jsonify({"error": "falta 'password' en JSON"}), 400

    analysis = zxcvbn(pwd)

    score_text = {0: "Muy débil", 1: "Débil", 2: "Aceptable", 3: "Fuerte", 4: "Muy fuerte"}
    politicas = check_contraseña_politica(pwd)

    resp = {
        "nivel_seguridad": score_text.get(analysis["score"], "Desconocido"),
        "score": analysis["score"],
        "tiempo_estimado_crackeo": analysis["crack_times_display"]["offline_fast_hashing_1e10_per_second"],
        "sugerencias": analysis["feedback"]["suggestions"],
        "advertencia": analysis["feedback"]["warning"],
        "politicas": politicas,
        "cumple_politicas": all(politicas.values())
    }
    return jsonify(resp)

# --------- UI: HTML sencillo servido desde una función ----------
@app.get("/")
def index():
    return """
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Validador de Contraseñas</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  body{font-family:system-ui,Arial,sans-serif;margin:0;background:#0f172a;color:#e5e7eb}
  .box{max-width:680px;margin:40px auto;padding:24px;background:#111827;border:1px solid #1f2937;border-radius:12px}
  h1{margin:0 0 12px;font-size:1.3rem}
  label{display:block;margin:8px 0 6px;color:#9ca3af}
  input,button{font:inherit}
  input[type=password]{width:100%;padding:10px 12px;border-radius:8px;border:1px solid #374151;background:#0b1220;color:#e5e7eb}
  .row{display:flex;gap:8px;align-items:center;margin-top:10px}
  button{padding:10px 14px;border:0;border-radius:8px;background:#60a5fa;color:#0b1220;font-weight:700;cursor:pointer}
  button:disabled{opacity:.6;cursor:not-allowed}
  .small{color:#9ca3af;font-size:.9rem;margin-top:6px}
  .card{margin-top:14px;padding:12px;border:1px solid #1f2937;border-radius:10px;background:#0b1220}
  .k{color:#9ca3af;font-size:.9rem}
  .v{font-family:ui-monospace,Consolas,monospace}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  ul{margin:6px 0 0 18px}
  .pill{display:inline-block;padding:4px 8px;border-radius:999px;font-weight:700;margin-top:6px}
  .ok{background:#064e3b;color:#a7f3d0}
  .warn{background:#78350f;color:#fde68a}
  .bad{background:#7f1d1d;color:#fecaca}
  .list{list-style:none;padding:0;margin:6px 0 0}
  .list li{margin:4px 0}
</style>
</head>
<body>
  <div class="box">
    <h1>🔐 Validador de Contraseñas</h1>
    <label for="pwd">Contraseña</label>
    <input id="pwd" type="password" placeholder="Escribe tu contraseña..." autocomplete="new-password">
    <div class="row">
      <button id="show">👁 Mostrar</button>
      <button id="check">Evaluar</button>
      <span class="small">La evaluación se hace en este servidor (no se envía a terceros).</span>
    </div>

    <div id="out" class="card" style="display:none">
      <div><span class="k">Nivel:</span> <span id="nivel" class="pill warn">—</span></div>
      <div class="grid" style="margin-top:8px">
        <div><div class="k">Score (0–4)</div><div class="v" id="score">—</div></div>
        <div><div class="k">Crackeo (offline rápido)</div><div class="v" id="crack">—</div></div>
      </div>

      <div class="grid" style="margin-top:8px">
        <div>
          <div class="k">Cumple políticas</div>
          <div id="okpol" class="pill">—</div>
        </div>
        <div>
          <div class="k">Políticas</div>
          <ul class="list" id="pols"></ul>
        </div>
      </div>

      <div style="margin-top:8px">
        <div class="k">Sugerencias</div>
        <ul id="sugs"></ul>
      </div>

      <pre id="raw" class="card" style="white-space:pre-wrap;margin-top:10px"></pre>
    </div>
  </div>

<script>
const $ = (id)=>document.getElementById(id);
$("show").onclick = () => {
  $("pwd").type = $("pwd").type === "password" ? "text" : "password";
  $("show").textContent = $("pwd").type === "password" ? "👁 Mostrar" : "🙈 Ocultar";
};

$("check").onclick = async () => {
  const password = $("pwd").value || "";
  if (!password) { alert("Ingresa una contraseña"); return; }

  $("check").disabled = true;
  try{
    const res = await fetch("/password/check", {
      method:"POST",
      headers:{ "Content-Type":"application/json" },
      body: JSON.stringify({ password })
    });
    const data = await res.json();

    // Render sencillo
    const nivel = data.nivel_seguridad || "—";
    const score = data.score ?? "—";
    const crack = data.tiempo_estimado_crackeo || "—";
    const passed = !!data.cumple_politicas;
    const pol = data.politicas || {};
    const sugs = data.sugerencias || [];

    $("out").style.display = "block";
    $("nivel").textContent = nivel;
    $("nivel").className = "pill " + (score>=3 ? "ok" : (score==2 ? "warn" : "bad"));
    $("score").textContent = score;
    $("crack").textContent = crack;

    const okpol = $("okpol");
    okpol.textContent = passed ? "Sí" : "No";
    okpol.className = "pill " + (passed ? "ok" : "bad");

    $("pols").innerHTML = "";
    const map = {
      longitud_minima: "Mínimo 12 caracteres",
      tiene_mayusculas: "Incluye MAYÚSCULAS",
      tiene_minusculas: "Incluye minúsculas",
      tiene_digito: "Incluye dígitos",
      tiene_caracter_especial: "Incluye símbolo"
    };
    Object.keys(map).forEach(k=>{
      const li = document.createElement("li");
      li.textContent = (pol[k] ? "✔ " : "✖ ") + map[k];
      $("pols").appendChild(li);
    });

    $("sugs").innerHTML = "";
    if (!sugs.length) {
      const li = document.createElement("li"); li.textContent = "Sin sugerencias. ¡Bien!";
      $("sugs").appendChild(li);
    } else {
      sugs.forEach(s => { const li = document.createElement("li"); li.textContent = s; $("sugs").appendChild(li); });
    }

    // útil para depurar
    $("raw").textContent = JSON.stringify(data, null, 2);

  } catch(e){
    alert("Error consultando la API: " + e);
  } finally{
    $("check").disabled = false;
  }
};
</script>
</body>
</html>
    """

if __name__ == "__main__":
    # Ejecuta: python app.py -> abre http://127.0.0.1:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
