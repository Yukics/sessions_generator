import yaml
import logging

def yaml_read(path_name):
	with open(path_name) as current_read:
		try:
			current_read_full = yaml.safe_load(current_read)
			logging.getLogger('ssh_conn_generator').debug(f"File read ok: {path_name}")
			return current_read_full
		except yaml.YAMLError as exc:
			logging.getLogger('ssh_conn_generator').error(f"File read failed: {path_name}\nError: {exc}")
			return None

def yaml_write(content, path_name):
	try:
		with open(path_name, 'w') as outfile:
			yaml.dump(content, outfile)
		logging.getLogger('ssh_conn_generator').debug(f"Finally could write {content} to {path_name}")
	except Exception:
		logging.getLogger('ssh_conn_generator').error(f"Could not write {content} to {path_name}")