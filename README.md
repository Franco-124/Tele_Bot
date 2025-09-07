# 🤖 Tele_Bot

Bot de Telegram que se conecta con **OpenAI** para responder mensajes de forma inteligente.  
Este proyecto está diseñado en Python y usa la librería `python-telegram-bot` junto con FastAPI para exponer APIs.

---

## 🚀 Instalación

Clona el repositorio e instala las dependencias:

```sh
git clone https://github.com/Franco-124/Tele_Bot.git
cd Tele_Bot
pip install -r requirements.txt
```


## 🪛 Configuracion
Crea un archivo .env en la raíz del proyecto con tus claves:


```sh
OPENAI_API_KEY=tu_api_key_de_openai
TELEGRAM_TOKEN=tu_token_de_telegram
```

## Ejecución
Puedes correr el bot desde la api configurando el Weekhook en Telegram
O usar el modulo  services/telegram_bot y probar el bot en local sin problema


