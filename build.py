#!/usr/bin/env python3
"""
Script para compilar el ejecutable de Abrir Caja
"""
import os
import sys
import subprocess
import shutil

# Configurar encoding seguro para consola en Windows (evita UnicodeEncodeError con emojis)
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

def main():
    print("🚀 Iniciando compilación de Abrir Caja...")
    
    # Asegurar que estamos en el directorio correcto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Verificar archivos necesarios
    if not os.path.exists("abrir_caja.py"):
        print("❌ Error: abrir_caja.py no encontrado")
        return

    # Instalar dependencias necesarias
    print("📦 Verificando dependencias...")
    try:
        import PySide6
        print("✅ PySide6 encontrado")
    except ImportError:
        print("📦 Instalando PySide6...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PySide6"], check=True)

    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI y Uvicorn encontrados")
    except ImportError:
        print("📦 Instalando FastAPI y Uvicorn...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn[standard]"], check=True)

    try:
        import requests
        print("✅ requests encontrado")
    except ImportError:
        print("📦 Instalando requests...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)

    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("📦 Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    # Compilar usando el archivo .spec si existe, o comando directo
    if os.path.exists("abrir_caja.spec"):
        print("📄 Usando archivo abrir_caja.spec existente...")
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "--noconfirm", "abrir_caja.spec"]
    else:
        print("⚙️ Generando comando directo de PyInstaller...")
        sep = ";" if os.name == "nt" else ":"
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=AbrirCajon",
            "--icon=app_icon_bg.ico",
            "--clean",
            "--noconfirm",
            "--hidden-import=PySide6.QtCore",
            "--hidden-import=PySide6.QtWidgets",
            "--hidden-import=PySide6.QtGui",
            "--hidden-import=uvicorn.logging",
            "--hidden-import=uvicorn.loops",
            "--hidden-import=uvicorn.loops.auto",
            "--hidden-import=uvicorn.protocols",
            "--hidden-import=uvicorn.protocols.http",
            "--hidden-import=uvicorn.protocols.http.auto",
            "--hidden-import=uvicorn.protocols.websockets",
            "--hidden-import=uvicorn.protocols.websockets.auto",
            "--hidden-import=uvicorn.lifespan",
            "--hidden-import=uvicorn.lifespan.on",
            "--hidden-import=requests",
            "--hidden-import=win32api",
            "--hidden-import=win32print",
            "--hidden-import=win32con",
            "--add-data", f"app_icon_bg.ico{sep}.",
            "--add-data", f"app_icon_bg.png{sep}.",
            "--add-data", f"app_icon.png{sep}.",
            "abrir_caja.py"
        ]

    print(f"🔨 Ejecutando PyInstaller: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print("✅ ¡Ejecutable generado con éxito!")

        # Crear carpeta dist si no existe
        os.makedirs("dist", exist_ok=True)
        if os.path.exists("dist/AbrirCajon") and not os.path.exists("dist/AbrirCajon.exe"):
            shutil.copy2("dist/AbrirCajon", "dist/AbrirCajon.exe")
        print("📁 Ubicación: dist/AbrirCajon.exe")

        # Copiar archivos auxiliares necesarios a dist/
        archivos_a_copiar = [
            "config.json",
            "cloudflared.exe",
            "app_icon_bg.ico",
            "app_icon_bg.png",
            "app_icon.png"
        ]

        # Asegurar cloudflared.exe en la raíz o en dist/
        cloudflared_dist = os.path.join("dist", "cloudflared.exe")
        if not os.path.exists("cloudflared.exe") and not os.path.exists(cloudflared_dist):
            print("🌐 Descargando cloudflared.exe oficial para Windows...")
            try:
                import urllib.request
                url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
                urllib.request.urlretrieve(url, "cloudflared.exe")
                print("✅ cloudflared.exe descargado exitosamente.")
            except Exception as e:
                print(f"⚠️ No se pudo descargar cloudflared.exe automáticamente: {e}")

        for archivo in archivos_a_copiar:
            if os.path.exists(archivo):
                shutil.copy2(archivo, os.path.join("dist", archivo))
                print(f"📋 Copiado a dist/: {archivo}")

        # Asegurar config.json por defecto en dist/ si no existe
        if not os.path.exists("dist/config.json"):
            import json
            default_config = {
                "usuario": "",
                "pin": "",
                "impresora": ""
            }
            with open(os.path.join("dist", "config.json"), "w", encoding="utf-8") as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            print("📋 Archivo dist/config.json creado por defecto")

        print("\n🎉 ¡Compilación finalizada!")
        print("📁 Revisa la carpeta dist/:")
        if os.path.exists("dist"):
            for item in os.listdir("dist"):
                print(f"   - {item}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la compilación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
