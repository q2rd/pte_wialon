import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter

load_dotenv()

from database.sqlite import init_db
from routs.v1.sub_route import router as r

app = FastAPI(on_startup=init_db())
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(r, prefix="/test")
app.include_router(api_v1)


if __name__ == '__main__':
    cfg = uvicorn.Config("main:app", log_level="info", host="0.0.0.0", port=8000)
    server = uvicorn.Server(config=cfg)
    server.run()
