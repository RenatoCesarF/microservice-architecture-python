import logging

def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Formato de log
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
        )

        # Saída no console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger
