from app import app
from app.mqtt.broker import start_broker
from app.mqtt.subscribe import start_sub
from threading import Thread
import asyncio
from app.views import login
from app.views.index import bp_index


app.static('/static', './app/static')
app.blueprint(bp_index)

if __name__ == "__main__":
    Thread(target=start_broker).start()
    Thread(target=start_sub).start()
    app.run(host="0.0.0.0", port=21025, debug=False)
