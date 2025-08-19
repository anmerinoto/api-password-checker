# api-password-checker
Proyecto para analizar la fortaleza de contraseñas para sitios web. GRUPO 11
# 🔐 Password Strength Checker API

## 📌 Descripción
Esta API permite validar la fortaleza de contraseñas combinando dos enfoques:  
1. **Análisis de entropía** mediante la librería `zxcvbn`.  
2. **Validación de políticas personalizadas**, como longitud mínima, uso de mayúsculas, minúsculas, dígitos y caracteres especiales.  

Además, incluye una pequeña **interfaz web en HTML** para ingresar contraseñas y ver los resultados de forma sencilla.

---

## 🚀 Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/miusuario/password-checker-api.git
cd password-checker-api


## 2. Crear entorno virtual
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```bash 

## 3. Instalar dependencias
```
pip install flask zxcvbn

```bash

## Ejecución

Levantar la API con:
```
python app.py
```bash 

La aplicación estará disponible en:
👉 http://127.0.0.1:5000/