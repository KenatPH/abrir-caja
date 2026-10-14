# Guía de Compilación - Abrir Caja

Para compilarlo desde tu máquina, abre una terminal y sigue estos pasos:

---

### 1. Entra a la carpeta de `abrir_caja`

```bash
cd modulos-embebidos/abrir_caja
```

*(Si usas el entorno virtual de la carpeta, actívalo con `source venv/bin/activate`)*

---

### 2. Ejecutar la compilación

Tienes dos formas:

#### Opción A (Recomendada, igual que en `comandar_server`):
```bash
python build.py
```

> Este script se encarga de verificar librerías (`PySide6`, `fastapi`, `uvicorn`, `requests`, `pyinstaller`), compilar con PyInstaller usando el `.spec`, y copiar automáticamente a la carpeta `dist/` el archivo `config.json` y los iconos necesarios.

#### Opción B (Comando directo con el archivo `.spec`):
```bash
pyinstaller abrir_caja.spec
```

---

### 3. Ubicación del resultado

Al finalizar, encontrarás el ejecutable y sus archivos de soporte en:
📁 **`abrir_caja/dist/`**
