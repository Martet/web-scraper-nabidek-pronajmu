from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import config
from offers_storage import OffersStorage

templates = Jinja2Templates(directory="src/templates")
clients: set[WebSocket] = set()

def create_web_ui() -> FastAPI:
    app = FastAPI()
    storage = OffersStorage(config.found_offers_file)

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request):
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "offers": storage.get_offers(),
                "offset": 25
            },
        )

    @app.get("/offers")
    def get_offers(limit: int = 25, offset: int = 0):
        slice_ = storage.get_offers(limit, offset)

        html = ""
        for o in slice_:
            html += templates.get_template("offer.html").render(offer=o)
        html += templates.get_template("loader.html").render(offset=offset + limit)

        return HTMLResponse(html)

    
    @app.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket):
        await ws.accept()
        clients.add(ws)

        try:
            while True:
                await ws.receive_text()
        except:
            clients.remove(ws)
    
    return app


async def broadcast_offer(offer):
    dead = []

    for ws in clients:
        try:
            await ws.send_text(
                templates.get_template("offer.html").render(offer=offer, new=True)
            )
        except:
            dead.append(ws)

    for d in dead:
        clients.remove(d)
