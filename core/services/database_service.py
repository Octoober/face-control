import logging
from typing import List

from web3 import Web3
from sqlalchemy.orm import Session
from core.models import Wallet, User

from core.utils.database_connetion import DatabaseConnection
from core.services.ethereum_service import EthereumService

logger = logging.getLogger("DatabaseService")


class DatabaseService:
    def __init__(
        self, ethereum_service: EthereumService, db_connection: DatabaseConnection
    ) -> None:
        self._ethereum_service = ethereum_service
        self._db_connection = db_connection

    def _get_user_wallet_parts(self, session: Session) -> List:
        try:
            return (
                session.query(User, Wallet)
                .join(Wallet, User.id == Wallet.pk_user_id)
                .all()
            )
        except Exception as exc:
            logging.error(exc)
            return []

    def _update_wallet_balance(self, user: User, wallet: Wallet, session: Session) -> None:
        try:
            balance = self._ethereum_service.get_token_balance(
                Web3.to_checksum_address(str(wallet.address))
            )
            if balance is not None:
                wallet.balance = balance
                is_modified = session.is_modified(wallet)
                if is_modified:
                    logger.info(
                        f'The balance of user "{user.username}" on wallet "{wallet.address}" has been updated'
                    )
                session.commit()
        except Exception as exc:
            logger.error(f"Failed to update balance for user {user.id}: {exc}")

    def update_user_wallet_balance(self) -> None:
        with self._db_connection as db_connection:
            session = db_connection.session
            user_wallet_parts = self._get_user_wallet_parts(session)

            if not user_wallet_parts:
                logging.error('There are no "users" with wallets in the database')
                return

            for user, wallet in user_wallet_parts:
                self._update_wallet_balance(user, wallet, session)
