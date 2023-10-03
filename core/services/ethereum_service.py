import json
import logging

from pathlib import Path
from typing import Dict, Union, Any

from web3 import Web3
from eth_typing import Address, ChecksumAddress

logger = logging.getLogger("EthereumService")


class EthereumService:
    def __init__(
        self,
        w3: Web3,
        contract_address: Union[Address, ChecksumAddress],
        abi_filename: str = "contract_abi.json",
    ) -> None:
        self._contract_address = contract_address
        self._abi_filename = abi_filename
        self._abi_filepath = Path(self._abi_filename)

        self._contract_abi = self.load_contract_abi(self._abi_filepath)
        self._contract = w3.eth.contract(
            address=contract_address, abi=self._contract_abi
        )

    @staticmethod
    def load_contract_abi(filepath: Path) -> Dict[str, Any]:
        if not filepath.exists():
            raise FileNotFoundError(f"FIle {filepath} not found")

        with filepath.open("r") as file:
            return json.load(file)

    def get_token_balance(self, wallet_address: Union[Address, ChecksumAddress]) -> int:
        balance = self._contract.functions.balanceOf(wallet_address).call()
        return int(balance)
