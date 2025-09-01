from lib.logs import setup_logging
from lib.conf import load_conf
from lib.vcenter import vcenter_get_info
from lib.filter import replace_dict_value_recurse
from lib.parser import royalts_parse_from_yaml

import logging
import json

if __name__ == "__main__":

	setup_logging()
	
	logging.getLogger('ssh_conn_generator').info("🚀 Starting script")
	logging.getLogger('ssh_conn_generator').info("⚙️  About to load conf")
	
	conf_loaded = load_conf()
	
	logging.getLogger('ssh_conn_generator').debug(f"Configuration loaded: {json.dumps(replace_dict_value_recurse(conf_loaded, 'password', '******'), indent=2)}")

	if not isinstance(conf_loaded, dict):
		logging.getLogger('ssh_conn_generator').error("❌ Loaded conf is not a dict or is empty")

	if 'vcenter' in conf_loaded.keys():
		vcenter_get_info(conf_loaded['vcenter'])
	
	royalts_parse_from_yaml()
