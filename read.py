from datetime import datetime


# Import GPIO library
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


# Import simplified version of the MFRC522 library

# Import the PyOTA library
import iota

# Import json
import json
GPIO.setwarnings(False)

# Define IOTA address where all transactions (cleaning records) are stored, replace with your own address.
# IOTA addresses can be created with the IOTA Wallet
CleaningLogAddr = b"NYZBHOVSMDWWABXSACAJTTWJOQRPVVAWLBSFQVSJSWWBJJLLSQKNZFC9XCRPQSVFQZPBJCJRANNPVMMEZQJRQSVVGZ"


# Create IOTA object, specify full node to be used when sending transactions.
# Notice that not all nodes in the field.deviota.com cluster has enabled attaching transactions to the tangle
# In this case you will get an error, you can try again later or change to a different full node.
api = iota.Iota("https://nodes.devnet.iota.org:443")





# Define static variable
hotel = "adidas"

# Create RFID reader object
reader = SimpleMFRC522()

# Main loop, executes when an RFID tag (ID card) is close to the reader
try:
    while True:
        
        # Show welcome message
        print("\nWelcome to the our project")
        print("Press Ctrl+C to exit the system")
        
        # Get room number
        room_number = input("\nPlease type your location and press Enter: ")
        
        print("\nThank you, now hold your ID card near the reader")       
        
        # Get card ID from the reader
        id, text = reader.read()
                
        # Create json data to be uploaded to the tangle
        data = {'tagID': str(id), 'hotel': hotel, 'room_number': room_number}
        
        # Define new IOTA transaction
        pt = iota.ProposedTransaction(address = iota.Address(CleaningLogAddr),
                                      message = iota.TryteString.from_unicode(json.dumps(data)),
                                      tag     = iota.Tag(b'HOTELIOTA'),
                                      value   = 0)

        # Print waiting message
        print("\nID card detected...Sending transaction...Please wait...")

        # Send transaction to the tangle
        FinalBundle = api.send_transfer(depth=3, transfers=[pt], min_weight_magnitude=9)['bundle']
    
        # Print confirmation message 
        print("\nTransaction sucessfully completed, have a nice day")
                
        
# Clean up function when user press Ctrl+C (exit)
except KeyboardInterrupt:
    print("cleaning up")
    GPIO.cleanup()