# test_validator.py
import argparse, importlib, json, getpass, sys

CANDIDATES = ("validate_password", "check_password", "is_strong_password")

def load_validator():
    mod = importlib.import_module("validators")
    for name in CANDIDATES:
        fn = getattr(mod, name, None)
        if callable(fn):
            return fn, name
    raise AttributeError(f"No encontré ninguna función candidata en validators.py: {CANDIDATES}")

def normalize_result(result):
    if isinstance(result, dict):
        # Convención: usar "is_valid" si existe; si no, evaluar truthiness
        is_valid = bool(result.get("is_valid", True))
        return is_valid, result
    return bool(result), {"is_valid": bool(result)}

def main():
    parser = argparse.ArgumentParser(description="Probar funciones de validators.py")
    parser.add_argument("-p", "--password", help="Password a validar (si omites, se pedirá oculto)")
    args = parser.parse_args()

    pwd = args.password or getpass.getpass("Password: ")
    fn, name = load_validator()
    result = fn(pwd)
    is_valid, payload = normalize_result(result)

    print(f"Función usada: {name}")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if is_valid else 1

if __name__ == "__main__":
    sys.exit(main())
