from jsonschema import validate
import yaml
import logging
import json

def yaml_read(path_name):
	with open(path_name) as current_read:
		try:
			current_read_full = yaml.safe_load(current_read)
			logging.getLogger('sessions_generator').debug(f"File read ok: {path_name}")
			return current_read_full
		except yaml.YAMLError as exc:
			logging.getLogger('sessions_generator').error(f"File read failed: {path_name}\nError: {exc}")
			return None

def yaml_write(content, path_name):
	try:
		with open(path_name, 'w') as outfile:
			yaml.dump(content, outfile)
		logging.getLogger('sessions_generator').debug(f"Finally could write {content} to {path_name}")
	except Exception:
		logging.getLogger('sessions_generator').error(f"Could not write {content} to {path_name}")

def jsonr_schema_validation(jsonr_content, schema_version="v6"):
	schema=jsonr_read(f"schemas/RoyalJSONDocument.{schema_version}.json")
	try:
		validate(instance=jsonr_content, schema=schema)
		return True
	except Exception:
		logging.getLogger('sessions_generator').error(f"JSONR schema validation failed against schema version {schema_version}", exc_info=True)
		return False

def jsonr_read(path_name):
	try:
		with open(path_name) as current_read:
			current_read_full = json.load(current_read)
			logging.getLogger('sessions_generator').debug(f"File read ok: {path_name}")
			return current_read_full
	except Exception as exc:
		logging.getLogger('sessions_generator').error(f"File read failed: {path_name}\nError: {exc}")
		return None

def jsonr_write(content, path_name):
	try:
		with open(path_name, 'w') as outfile:
			json.dump(content, outfile, indent=2)
		logging.getLogger('sessions_generator').debug(f"Finally could write to {path_name}")
	except Exception:
		logging.getLogger('sessions_generator').error(f"Could not write to {path_name}")