# fast start

```bash
./start.sh
````

# setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip -r requirements.txt
python src/main.py

export PYTHONWARNINGS="ignore"
pip uninstall setuptools
pip install setuptools==80.9.0
```
# logging

## exceptions

```python
	try:
		donuts = 5
		guests = 0
		donuts_per_guest = donuts / guests
	except ZeroDivisionError:
		logging.error("DonutCalculationError", exc_info=True)
```

## basic conf

```python
logging.basicConfig(
	filename=f"logs/ssh_conn_generator-{datetime.today().strftime('%Y%m%d')}.log", 
	filemode='w', 
	filemode='a', 
	encoding="utf-8",
	format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', 
	datefmt='%m/%d/%Y %I:%M:%S %p',
	level=logging.DEBUG
)
```
