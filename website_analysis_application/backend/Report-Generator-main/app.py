import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from src.config.settings import get_settings
from src.logger.logger import get_logger
from src.routers import router_generator

settings = get_settings()
logger = get_logger(__file__)


ascii_art = """

░░      ░░░        ░░░░░░░░░      ░░░        ░░   ░░░  ░░        ░░       ░░░░      ░░░        ░░░      ░░░       ░░
▒  ▒▒▒▒  ▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒    ▒▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒▒▒▒  ▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒
▓  ▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓   ▓▓      ▓▓▓▓  ▓  ▓  ▓▓      ▓▓▓▓       ▓▓▓  ▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓  ▓▓       ▓▓
█        █████  ███████████  ████  ██  ████████  ██    ██  ████████  ███  ███        █████  █████  ████  ██  ███  ██
█  ████  ██        █████████      ███        ██  ███   ██        ██  ████  ██  ████  █████  ██████      ███  ████  █
                                                                                                                    

"""
app = FastAPI(
    title="AI Report Generator API App",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allows all origins, you can also specify a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

logger.info(f"Starting App : \n {ascii_art}")

logger.info("App Ready")
app.include_router(router_generator.router)


@app.get("/", response_class=PlainTextResponse)
async def root():
    return ascii_art


if __name__ == "__main__":
    try:
        uvicorn.run(
            app,
            port=8002,
            host="0.0.0.0",
        )
    except KeyboardInterrupt as ki:
        logger.info("Turning Server Off ...")
        logger.info("server Off")
    except Exception as e:
        logger.critical(f"Critical Error occured in app : {e}")
