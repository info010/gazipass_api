import logging

logger = logging.getLogger("uvicorn.error")

def setup_logging():
    root = logging.getLogger()
    if root.hasHandlers():
        root.handlers.clear()

    handler_console = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler_console.setFormatter(fmt)
    root.addHandler(handler_console)
    root.setLevel(logging.INFO)
    logging.info("Console logging initialised")