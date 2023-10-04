import logging

from web3 import Web3

from .utils import Scheduler, DatabaseConnection
from .services import DatabaseService, EthereumService


class Application:
    def __init__(self, provider: str, contract_address: str, database_url: str) -> None:
        """Initialize the Application.

        Args:
            provider (str): Ethereum provider URL.
            contract_address (str): Ethereum contract address.
            database_url (str): URL for the database connection.
        """
        self._logger = logging.getLogger(self.__class__.__name__)
        self._w3 = self._web3_connect(provider)
        
        self._ethereum_service = EthereumService(self._w3, Web3.to_checksum_address(contract_address))
        self._database_connection = DatabaseConnection(database_url)
        self._database_service = DatabaseService(self._ethereum_service, self._database_connection)

    def _web3_connect(self, provider: str) -> Web3:
        """Connect to the Ethereum provider.

        Args:
            provider (str): Ethereum provider URL.

        Returns:
            Web3: An instance of Web3 connected to the specified provider.
        """
        w3 = Web3(Web3.HTTPProvider(provider))

        if not w3.is_connected():
            self._logger.critical(f"Provider {provider} is not available")
            raise ConnectionError(f"Provider {provider} is not available")

        return w3

    def setup_scheduler(self) -> Scheduler:
        """Set up the EthereumService, DatabaseService, and Scheduler.

        Returns:
            Scheduler: An instance of the Scheduler class.
        """
        scheduler = Scheduler(self._ethereum_service, self._database_service)
        return scheduler
