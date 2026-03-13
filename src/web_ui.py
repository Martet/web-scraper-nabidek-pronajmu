from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="src/templates")
clients: set[WebSocket] = set()

def create_web_ui(storage) -> FastAPI:
    app = FastAPI()

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request):
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "offers": storage.get_offers(),
                "target": "beforeend"
            },
        )

    @app.get("/offers", response_class=HTMLResponse)
    def get_offers(before: str | None = None):
        if before:
            idx = storage.get_index(before)
            if idx is None:
                return ""
            start = idx + 1
        else:
            start = 0

        slice_ = storage.get_offers(25, start)
        html = ""
        for o in slice_:
            html += templates.get_template("offer.html").render(offer=o, target="beforeend")

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
            await ws.send_text(templates.get_template("offer.html").render(offer=offer, target="afterbegin"))
        except:
            dead.append(ws)

    for d in dead:
        clients.remove(d)
