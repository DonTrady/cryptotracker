import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QLabel, QPushButton, QSpinBox, QTabWidget, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt
from binance.client import Client
from threading import Thread
import time
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Initialize the Binance API client
api_key = "aC7RxFA3lmL4PRjVMHXFA3P5N2wa4XslcqDWWF8547EueQCerJSoB94VGsIKKJ7w"
api_secret = "LGF1uV5A9mJdGIj9NMSYandHpTevxoHC3bsoNCM1NHDIxoWzNq4mPNVlTZbq58Bs"
client = Client(api_key, api_secret)

# Load the sounds
buy_sound = pygame.mixer.Sound('buy_sound.mp3')
sell_sound = pygame.mixer.Sound('sell_sound.mp3')

# Create a new mixer channel for each sound
buy_channel = pygame.mixer.Channel(0)
sell_channel = pygame.mixer.Channel(1)

# Create a dictionary to store the box labels and volume thresholds
boxes = {
    'Bitcoin': {'label': None, 'volume_threshold': 15000, 'symbol': 'BTCUSDT'},
    'Ethereum': {'label': None, 'volume_threshold': 15000, 'symbol': 'ETHUSDT'},
    'BNB': {'label': None, 'volume_threshold': 15000, 'symbol': 'BNBUSDT'}
}

# Create the QApplication instance
app = QApplication(sys.argv)

# Define the checkbox layout as a global variable
checkbox_layout = None

# Define the tracker function
def track_crypto(symbol, box):
    while True:
        trades = client.get_recent_trades(symbol=symbol, limit=1)
        for trade in trades:
            trade_value = float(trade['price']) * float(trade['qty'])
            if trade_value > boxes[symbol]['volume_threshold']:
                if not trade['isBuyerMaker']:  # If buyer is the taker
                    box.setStyleSheet("background-color: green;")
                    buy_channel.play(buy_sound)  # Play the buy sound on its channel
                else:
                    box.setStyleSheet("background-color: red;")
                    sell_channel.play(sell_sound)  # Play the sell sound on its channel
        time.sleep(1)

# Create the main window
window = QMainWindow()
window.setWindowTitle('Crypto Tracker')
window_layout = QVBoxLayout(window)

# Create a tab widget
tab_widget = QTabWidget()

# Create Tab 6
tab6 = QWidget()
tab6_layout = QVBoxLayout(tab6)
tab_widget.addTab(tab6, "Tab 6")

# Create a container widget for checkboxes and boxes
container = QWidget()

# Initialize the checkbox layout
checkbox_layout = QVBoxLayout(container)

# Initialize the box layout
box_layout = QVBoxLayout()

# Add checkboxes for each cryptocurrency
def create_checkbox(symbol):
    global checkbox_layout  # Use the global variable

    checkbox = QCheckBox(symbol)
    checkbox.setChecked(False)
    checkbox_layout.addWidget(checkbox)
    checkbox.stateChanged.connect(lambda state, s=symbol: on_checkbox_state_changed(state, s))

def on_checkbox_state_changed(state, symbol):
    if state == Qt.Checked:
        # Create a box for this cryptocurrency
        box = QLabel(symbol)
        box.setStyleSheet("background-color: red;")  # Initial fill color
        box_layout.addWidget(box)
        boxes[symbol]['label'] = box

        # Start the tracker thread for this cryptocurrency
        thread = Thread(target=track_crypto, args=(boxes[symbol]['symbol'], box))
        thread.start()
        boxes[symbol]['thread'] = thread
    else:
        # Remove the box for this cryptocurrency
        for i in reversed(range(box_layout.count())):
            widget = box_layout.itemAt(i).widget()
            if widget.text() == symbol:
                widget.deleteLater()
                break

        # Stop the tracker thread for this cryptocurrency
        if symbol in boxes:
            thread = boxes[symbol]['thread']
            if thread is not None:
                thread.join()

# Add checkboxes for each cryptocurrency
create_checkbox('Bitcoin')
create_checkbox('Ethereum')
create_checkbox('BNB')

# Add the container widget and box layout to the tab layout
tab6_layout.addWidget(container)
tab6_layout.addLayout(box_layout)

# Add the tab widget to the main window layout
window_layout.addWidget(tab_widget)

# Show the main window
window.show()

# Start the QApplication event loop
sys.exit(app.exec())
