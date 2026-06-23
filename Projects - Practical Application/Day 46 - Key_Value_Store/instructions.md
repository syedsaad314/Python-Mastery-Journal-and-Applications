# Operational Instructions: Reconciled Key-Value Store System
**Lead Engineer:** Syed Saad Bin Irfan

## 1. Dependency Configuration
Ensure you have Python 3.10 or higher installed. Run the command below to install terminal table formatting tools:
pip install -r requirements.txt

## 2. Code Execution
Run the orchestrator script to simulate network splits, conflicting log branches, and automatic leader reconciliation:
python main.py

## 3. Operational Outcomes
* Watch the cluster metrics panel step-by-step to see how it catches data mismatches across nodes.
* Observe how the leader backtracks to find where logs match, trims off conflicting entries, and synchronizes the cluster safely.