import logging
from logging.config import fileConfig

from web3 import Web3



from core.utils import Scheduler, DatabaseConnection
from core.services import DatabaseService, EthereumService
from core.constants import PROVIDER, DATABASE_URL, CONTRACT_ADDRESS


fileConfig(fname="logging.conf", disable_existing_loggers=False)

logger = logging.getLogger("Main")

w3 = Web3(Web3.HTTPProvider(PROVIDER))

if not w3.is_connected():
    print("Error: Could not connect to Ethereum node.")
    exit()


def setup_scheduler() -> Scheduler:
    """Set up the EthereumService, DatabaseService and Scheduler.

    Returns:
        Scheduler: An instance of the Scheduler class.
    """
    ethereum_service = EthereumService(w3, Web3.to_checksum_address(CONTRACT_ADDRESS))
    database_connection = DatabaseConnection(DATABASE_URL)
    database_service = DatabaseService(ethereum_service, database_connection)

    scheduler = Scheduler(ethereum_service, database_service)
    return scheduler
