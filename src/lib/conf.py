from lib.file import yaml_read
import logging
import os

def load_conf():

	conf_files = ["vcenter.yml", "gcp.yml", "azure.yml"]
	conf_loaded = {}

	for conf_file in conf_files:

		if not os.path.isfile(f"conf/{conf_file}"):
			continue # jump to next iteration

		current_conf_loaded = yaml_read(f"conf/{conf_file}")
		current_conf_main_key = list(current_conf_loaded.keys())[0]
		conf_loaded[current_conf_main_key] = current_conf_loaded[current_conf_main_key]
		logging.getLogger('ssh_conn_generator').debug(f"Conf loaded from file: {conf_file}")
	
	return conf_loaded