# Operational Instructions: Distributed Financial Ledger System
**Lead Engineer:** Syed Saad Bin Irfan

## 1. Environment Verification
Ensure your environment is running Python 3.10 or higher. Install the table formatting dependency:
```bash
pip install -r requirements.txt
```
## 2. Running the System
Execute the central coordinator test script to run through transactions under standard and failure scenarios:

```Bash
python main.py
```
## 3. Operational Outcomes
Watch the log output to see the system process multi-node financial entries using the two-phase commit protocol.

Monitor how the validation layer automatically catches and rolls back transactions if a ledger node votes to abort.