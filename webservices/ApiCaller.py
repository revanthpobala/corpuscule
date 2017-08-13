import bigchaindb_driver
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import logging

from bigchaindb_driver.exceptions import NotFoundError

"""
Class for API Caller.
"""


class ApiCaller(object):
    """
    Init method to store the root url and initialize the object.
    """

    def __init__(self):
        self.root_url = "http://localhost:9984"
        self.bdb = BigchainDB(self.root_url)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)-15s %(status)-3s %(message)s')

    """
    Submit the transaction
    
    :invoice: Invoice from the user
    :metadata: Metadata corresponding to the transaction
    
    :return : Transaction ID of the transaction.
    """

    def submit_transaction(self, invoice, metadata):
        # Generate a public/private keys. Unique for each transaction
        generate_customer_keys = generate_keypair()

        prepared_creation_tx = self.bdb.transactions.prepare(operation='CREATE',
                                                             signers=generate_customer_keys.public_key, asset=invoice,
                                                             metadata=metadata)
        fulfilled_creation_tx = self.bdb.transactions.fulfill(prepared_creation_tx,
                                                              private_keys=generate_customer_keys.private_key)
        sent_creation_tx = self.bdb.transactions.send(fulfilled_creation_tx)
        current_txid = sent_creation_tx['id']
        # Query, if the transaction is valid or not.
        i = 0
        while i < 100:
            i += 1
            try:
                if self.bdb.transactions.status(current_txid).get('status') == 'valid':
                    break
            except bigchaindb_driver.exceptions.NotFoundError:
                pass
        try:
            status = self.bdb.transactions.status(current_txid).get('status')
            if status == "valid":
                return current_txid
        except NotFoundError as e:
            # In future we can have error codes such as ERR-INVALID_TX-400 etc.
            self.logger.error('Transaction "%s" Status.',
                              current_txid,
                              extra={'status': e.status_code})
        return None

    """
    Method to retrieve the Invoice based on the transaction id.
    
    :transaction_id: The transaction ID of a user.
    
    :return The Invoice corresponding to the transaction.
    """

    def get_invoice_based_on_transaction_id(self, transaction_id):
        try:
            invoice_details = self.bdb.transactions.retrieve(transaction_id)
            if invoice_details:
                return invoice_details
        except NotFoundError as e:
            self.logger.error('The provided Transaction Hash:  "%s" is invalid.', transaction_id,
                              extra={'status': e.status_code})
            return None
