from iota import Iota
from iota import Address
from iota import Transaction
from iota import TryteString

# Import json library
import json

# Import datetime libary
import datetime

# Import from PrettyTable
from prettytable import PrettyTable

# Define IOTA address where all transactions (cleaning records) are stored, replace with your own address.
address = [Address(b'NYZBHOVSMDWWABXSACAJTTWJOQRPVVAWLBSFQVSJSWWBJJLLSQKNZFC9XCRPQSVFQZPBJCJRANNPVMMEZQJRQSVVGZ')]

# Define full node to be used when retrieving cleaning records
iotaNode = "https://nodes.devnet.iota.org:443"

# Create an IOTA object
api = Iota(iotaNode)

# Create PrettyTable object
x = PrettyTable()

# Specify column headers for the table
x.field_names = ["Product", "Brand", "Location", "Date"]

# Find all transacions for selected IOTA address
result = api.find_transactions(addresses=address)
    
# Create a list of transaction hashes
myhashes = result['hashes']

# Print wait message
print("Please wait while retrieving cleaning records from the tangle...")

# Loop trough all transaction hashes
for txn_hash in myhashes:
    
    # Convert to bytes
    txn_hash_as_bytes = bytes(txn_hash)

    # Get the raw transaction data (trytes) of transaction
    gt_result = api.get_trytes([txn_hash_as_bytes])
    
    # Convert to string
    trytes = str(gt_result['trytes'][0])
    
    # Get transaction object
    txn = Transaction.from_tryte_string(trytes)
    
    # Get transaction timestamp
    timestamp = txn.timestamp
    
    # Convert timestamp to datetime
    clean_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    # Get transaction message as string
    txn_data = str(txn.signature_message_fragment.decode())
    
    # Convert to json
    json_data = json.loads(txn_data)
    
    # Check if json data has the expected json tag's
    if all(key in json.dumps(json_data) for key in ["tagID","hotel","room_number"]):
        # Add table row with json values
        x.add_row([json_data['tagID'], json_data['hotel'], json_data['room_number'], clean_time])

# Sort table by cleaned datetime
x.sortby = "Date"

# Print table to terminal
print(x)