import time
import logging
import schedule
from core.services.ethereum_service import EthereumService
from core.services.database_service import DatabaseService


class Scheduler:
    def __init__(
        self, ethereum_service: EthereumService, database_service: DatabaseService
    ) -> None:
        """
        Initialize Scheduler class with EthereumService and DatabaseService instances.

        Args:
            ethereum_service (EthereumService): Instance of EthereumService.
            database_service (DatabaseService): Instance of DatabaseService.
        """
        self._logger = logging.getLogger(self.__class__.__name__)
        self._ethereum_service = ethereum_service
        self._database_service = database_service

    def _job(self) -> None:
        """Perform the job of updating user wallet balance."""
        self._database_service.update_wallet_balance()

    def run(self, minutes: int) -> None:
        """Run the scheduler and execute the job every 5 minutes.

        Args:
            minutes (int): Schedule minutes.
        """
        self._logger.debug(
            f"The scheduler is up and running. Intervals: {minutes} minutes."
        )

        self._job()
        schedule.every(minutes).minutes.do(self._job)

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self._logger.debug("Scheduler stopped by user.")
