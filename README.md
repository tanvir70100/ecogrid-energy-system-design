# EcoGrid Energy Prototype

## How to Run the Prototype

### 1. Create a virtual environment

bash
python -m venv venv

### 2. Activate the virtual environment

For macOS/Linux:

source venv/bin/activate

For Windows:

bash
venv\Scripts\activate

### 3. Install required packages
bash
pip install -r requirements.txt

### 4. Run the prototype
bash
python src/main.py


Expected output should show:

=== Completed Trades ===
TradeCompleted event details

=== Completed Settlements ===
SettlementCompleted event details

=== Event Log ===
MeterReadingReceived
TradeCompleted
SettlementCompleted
## How to Run Pytest

Run this command from the project root folder:

bash
pytest


Expected result:

bash
2 passed


The tests verify that:

bash
1. a meter reading with surplus energy creates a trade and settlement;
2. a meter reading without surplus energy does not create a trade.
