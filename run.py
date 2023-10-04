from logging.config import fileConfig

from core import Application
from constants import PROVIDER, CONTRACT_ADDRESS, DATABASE_URL


if __name__ == "__main__":
    fileConfig(fname="logging.conf")
    scheduler = Application(PROVIDER, CONTRACT_ADDRESS, DATABASE_URL).setup_scheduler()
    scheduler.run(minutes=5)
