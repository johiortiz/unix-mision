"""Misión 5 · Automatízalo. Pruébalo con:  bash comprobar.sh python"""
import os
import subprocess


def ejecutar(comando, env=None):
    """Ejecuta un comando de terminal y devuelve (salida, codigo_de_salida)."""
    print(f"ejecuto: {comando}")
    resultado = subprocess.run(
        ["bash", "-c", comando], capture_output=True, text=True,   # siempre bash, también en Windows
        env=env if env is not None else os.environ.copy(),
    )
    salida = (resultado.stdout + resultado.stderr).strip()
    if salida:
        print("   " + salida.replace("\n", "\n   ")[:400])
    return salida, resultado.returncode


def resolver():
    fragmentos = []

    # Fragmento 1: find + cat (carpeta oculta en proyecto/datos)
    salida, codigo = ejecutar(
        "find proyecto/datos -type f -name 'fragmento1.txt'"
    )
    if codigo != 0 or not salida:
        raise RuntimeError("No encontré fragmento1.txt")

    ruta_f1 = salida.splitlines()[0]
    f1, codigo = ejecutar(f"cat '{ruta_f1}'")
    if codigo != 0:
        raise RuntimeError("No pude leer fragmento1.txt")
    fragmentos.append(f1)

    # Fragmento 2: grep en proyecto/logs/app.log
    salida, codigo = ejecutar(
        "find proyecto -type f -path '*/logs/app.log'"
    )
    if codigo != 0 or not salida:
        raise RuntimeError("No encontré logs/app.log")

    ruta_log = salida.splitlines()[0]
    f2, codigo = ejecutar(
        f"grep -o 'fragmento2=[A-Z0-9]*' '{ruta_log}' | cut -d= -f2"
    )
    if codigo != 0 or not f2:
        raise RuntimeError("No encontré fragmento2 en el log")
    fragmentos.append(f2)

    # Fragmento 3: mkdir + mv en proyecto/descargas,
    # luego ejecutar('bash ../comprobar.sh orden')
    salida, codigo = ejecutar("find proyecto -type d -name descargas")
    if codigo != 0 or not salida:
        raise RuntimeError("No encontré la carpeta descargas")

    descargas = salida.splitlines()[0]
    ejecutar(
        f"mkdir -p '{descargas}/imagenes' "
        f"'{descargas}/documentos' "
        f"'{descargas}/datos'"
    )

    # `|| true` evita que falle si no hay archivos de una extensión
    ejecutar(
        f"cd '{descargas}' && "
        "mv *.jpg *.png imagenes/ 2>/dev/null || true"
    )
    ejecutar(
        f"cd '{descargas}' && "
        "mv *.pdf *.txt documentos/ 2>/dev/null || true"
    )
    ejecutar(
        f"cd '{descargas}' && "
        "mv *.csv *.json datos/ 2>/dev/null || true"
    )

    f3, codigo = ejecutar("bash ../comprobar.sh orden")
    if codigo != 0 or not f3:
        raise RuntimeError("No conseguí el fragmento 3")
    fragmentos.append(f3)

    # Fragmento 4: chmod +x y ejecutar revelar.sh con AGENTE
    salida, codigo = ejecutar(
        "find proyecto -type f -name 'revelar.sh'"
    )
    if codigo != 0 or not salida:
        raise RuntimeError("No encontré revelar.sh")

    ruta_revelar = salida.splitlines()[0]
    ejecutar(f"chmod +x '{ruta_revelar}'")

    env = {**os.environ, "AGENTE": "robot"}
    f4, codigo = ejecutar(
        f"cd proyecto && ./herramientas/revelar.sh",
        env=env,
    )
    if codigo != 0 or not f4:
        raise RuntimeError("No conseguí el fragmento 4")
    fragmentos.append(f4)

    clave = "-".join(fragmentos)
    print(f"\nCLAVE: {clave}")
    return clave


if __name__ == "__main__":
    if not os.path.isdir("proyecto"):
        print("Ejecútame desde la carpeta mision/ :  cd mision && python3 ../entrega/resolver.py   (o python)")
        raise SystemExit(1)
    resolver()
