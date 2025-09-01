import logging
from datetime import datetime
from pathlib import Path

def setup_logging():
	"""
	Configures logging for the 'ssh_conn_generator' application.
	This function sets up logging to output messages to both a log file and the console.
	The log file is named with the current date and stored in the 'logs' directory.
	Log messages include the timestamp, logger name, log level, and message content.
	The logging level is set to DEBUG.
	Handlers:
		- FileHandler: Writes logs to 'logs/ssh_conn_generator-YYYYMMDD.log' in append mode with UTF-8 encoding.
		- StreamHandler: Outputs logs to the console.
	Returns:
		None
	"""
	
	logger = logging.getLogger('ssh_conn_generator')
	formatter = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
	logger.setLevel("DEBUG")

	Path("logs").mkdir(exist_ok=True)
	Path("tmp").mkdir(exist_ok=True)
	file_handler = logging.FileHandler(
		f"logs/ssh_conn_generator-{datetime.today().strftime('%Y%m%d')}.log", 
		mode="a",
		encoding="utf-8"
	)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)

	console_handler = logging.StreamHandler()
	console_handler.setFormatter(formatter)
	logger.addHandler(console_handler)	