import logging

from web3 import Web3
from sqlalchemy.orm import Session
from core.models import Wallet

from core.utils.database_connetion import DatabaseConnection
from core.services.ethereum_service import EthereumService


class DatabaseService:
    def __init__(
        self, ethereum_service: EthereumService, db_connection: DatabaseConnection
    ) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._ethereum_service = ethereum_service
        self._db_connection = db_connection

    def _update_wallet_balance(self, wallet: Wallet, session: Session) -> None:
        try:
            balance = self._ethereum_service.get_token_balance(
                Web3.to_checksum_address(str(wallet.address))
            )

            if balance is not None:
                wallet.balance = balance
                is_modified = session.is_modified(wallet)
                if is_modified:
                    self._logger.info(
                        f'The balance of wallet "{wallet.address}" has been updated'
                    )
                session.commit()
        except Exception as exc:
            self._logger.error(
                f"Failed to update balance for wallet {wallet.address}: {str(exc)}"
            )
            raise exc

    def update_wallet_balance(self) -> None:
        with self._db_connection as db_connection:
            session = db_connection.session
            wallets = session.query(Wallet).all()

            if not wallets:
                self._logger.error("No wallets found")
                return

            for wallet in wallets:
                try:
                    self._update_wallet_balance(wallet, session)
                except Exception as exc:
                    logging.error(
                        f"Failed to update wallet balance for {wallet.id}: {str(exc)}"
                    )
                    session.rollback()
