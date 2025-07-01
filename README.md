# # Datos Hardcodeados Tool 

Este es un **script personalizado de reconocimiento web** hecho en Python usando **Scrapy**, diseñado para ayudar en labores de inteligencia durante pruebas de seguridad, CTFs o laboratorios como Hack The Box.

## ¿Qué hace esta herramienta?

Permite encontrar automáticamente:
- ✉️ Correos electrónicos
- 💬 Comentarios HTML (`<!-- ... -->`)
- 🔑 API Keys / Tokens
- 🔐 Credenciales en texto plano (ej: `password=admin123`)
- 📁 Archivos interesantes (`.txt`, `.log`, `.json`, etc.)
- 🔗 URLs visitadas durante el escaneo

Todo lo encontrado se guarda automáticamente en un archivo con el nombre del dominio escaneado.


##  Requisitos previos

### Debes tener instalado:

| Herramienta | Comando |
|-------------|---------|
| Python 3.x | `sudo apt install python3` |
| pipx       | `sudo apt install pipx` |

> ⚠️ En Kali Linux 2024.4+, ya no puedes usar `pip install` globalmente. Usa `pipx` o entornos virtuales (recomendado).

---

##  Pasos para usar la herramienta

### 1. Clona este repositorio

```bash
git clone https://github.com/Sadino07/datos_hardcodeados.git
cd datos_hardcodeados
```

### 2. Crea y activa el entorno virtual, e instala fake-useragent (opcional pero recomendado)

```bash
python3 -m venv recon_env
source recon_env/bin/activate
```

### 3. Instala scrapy y fake-useragent

```bash
pip install scrapy
pip install fake-useragent
```

### 4. Ejecuta la herramienta y visualiza los resultados

```bash
python3 datos_hardcodeados.py -u http://urldeejemplo.com
cat urldeejemplo.txt
```
