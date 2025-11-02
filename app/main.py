from core.logger import logger
from tui import Biblioteca

def main():
    logger.info("Inicializando o Sistema de Biblioteca Universitária")
    Biblioteca().run()
    logger.info("Sistema de Biblioteca Universitária finalizado")

if __name__ == "__main__":
    main()
