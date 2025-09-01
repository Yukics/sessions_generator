from lib.file import yaml_write
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl, vim
import logging
import atexit
import json
import uuid

def vcenter_get_info(vcenter_conf):
	"""
	Retrieves and processes VM information from multiple vCenter instances.
	For each vCenter configuration in `vcenter_conf`, this function:
	- Logs into the vCenter using provided credentials.
	- Fetches all virtual machines (VMs) from the vCenter.
	- Extracts and cleans relevant VM details such as name, template status, guest OS, notes, power state, IP address, guest tools status, and folder path.
	- Logs the cleaned VM information for debugging and tracking.
	- Writes the cleaned VM inventory to a YAML file named after the vCenter URL.
	Args:
		vcenter_conf (list): A list of dictionaries, each containing vCenter login configuration and root folder information.
	Returns:
		None
	"""

	for vcenter_login_conf in vcenter_conf:

		# login  
		logging.getLogger('ssh_conn_generator').info(f"About to login vcenter: {vcenter_login_conf['url']}")
		vcenter_logged_in = vcenter_login(vcenter_login_conf)

		# fetch
		children = vcenter_get_all_vms(vcenter_logged_in)
		logging.getLogger('ssh_conn_generator').info(f"Retrieved {len(children)} VM from vCenter {vcenter_login_conf['url']}")
		
		#transformation
		vcenter_vm_info_clean = []
		# for vm in children[0:50]: # Uncomment to limit to first 5 VMs for testing
		for vm in children:
			vm_folder_path = vcenter_get_folder_path(vm)
			summary = vm.summary
			vm_cleaned = {
				'uuid': summary.config.instanceUuid,
				'name': summary.config.name,
				'template': summary.config.template,
				'guest': summary.config.guestFullName,
				'note': summary.config.annotation,
				'power_state': str(summary.runtime.powerState),
				'ip': summary.guest.ipAddress if summary.guest else 'unknown',
				'guest_tools': str(summary.guest.toolsStatus) if summary.guest else 'unknown',
				'path': vm_folder_path
			}
			logging.getLogger('ssh_conn_generator').debug(f"Generated JSON:\n{json.dumps(vm_cleaned, indent=2)}")
			vcenter_vm_info_clean.append(vm_cleaned)
			logging.getLogger('ssh_conn_generator').info(f"Appending to clean VM state {summary.config.name}")

		logging.getLogger('ssh_conn_generator').info(f"Created full vcenter {vcenter_login_conf['url']} inventory")
		yaml_write(vcenter_vm_info_clean,f"tmp/{vcenter_login_conf['url']}.yml")

def vcenter_get_folder_path(obj, root_folders=['Datacenters', 'vm']):
	"""
	Retrieves the folder path for a given vSphere object by traversing its parent hierarchy.

	Args:
		obj: The vSphere object (typically a VM or Folder) whose folder path is to be determined.
		root_folders (set or list): A collection of Managed Object IDs (moId) representing root folders.
	
	Returns:
		list: The folder path as a list of folder names from the root to the object's folder.

	Logs:
		Information about the object and its resolved folder path using the 'ssh_conn_generator' logger.

	Note:
		The function assumes that the object and its parents have a 'name' attribute and a '_moId' property.
	"""
	logging.getLogger('ssh_conn_generator').info(f"Getting folder path for: {obj.summary.config.name}")

	paths = []
	if isinstance(obj, vim.Folder):
		logging.getLogger('ssh_conn_generator').debug(f"{obj.name} matched as a Folder so it is appended to the path")
		paths.append(obj.name)

	thisobj = obj
	while hasattr(thisobj, 'parent'):
		thisobj = thisobj.parent
		try:
			moid = thisobj._moId
			logging.getLogger('ssh_conn_generator').debug(f"Trying to get parent from {thisobj.name} with moid {moid}")
		except AttributeError:
			moid = None
		logging.getLogger('ssh_conn_generator').debug(f"{moid} trying to match against {root_folders}")
		if moid in root_folders:
			break
		logging.getLogger('ssh_conn_generator').debug(f"{thisobj.name} trying to match against {root_folders}")
		if thisobj.name in root_folders:
			break
		if isinstance(thisobj, vim.Folder):
			paths.append(thisobj.name)
	

	logging.getLogger('ssh_conn_generator').debug(f"Paths generated for {obj.summary.config.name} {str(paths)}")
	paths.reverse()
	logging.getLogger('ssh_conn_generator').debug(f"Reversed paths generated for {obj.summary.config.name} {str(paths)}")

	if paths is not None:
		logging.getLogger('ssh_conn_generator').info(f"Folder path for {obj.summary.config.name} in {'/'.join(paths)}")

	return paths

def vcenter_get_all_vms(vcenter_logged_in):
		"""
		Retrieves all virtual machines from a connected vCenter instance.

		Args:
			vcenter_logged_in: An authenticated vCenter connection object from pyVmomi.

		Returns:
			list: A list of vim.VirtualMachine objects representing all VMs in the vCenter.

		Note:
			The returned objects are not deep copies; they are references to the actual VM objects in vCenter.
		"""
		container = vcenter_logged_in.rootFolder  # starting point to look into "Datacenter/vm"
		view_type = [vim.VirtualMachine]  # object types to look for
		recursive = True  # whether we should look into it recursively
		container_view = vcenter_logged_in.viewManager.CreateContainerView(container, view_type, recursive)
		all_vms = container_view.view
		container_view.Destroy()

		return all_vms

def vcenter_login(vcenter_login_conf):
	"""
	Establishes a connection to a vCenter server using the provided configuration.
	Args:
		vcenter_login_conf (dict): A dictionary containing vCenter login parameters.
			Expected keys:
				- 'url' (str): The hostname or IP address of the vCenter server.
				- 'user' (str): The username for authentication.
				- 'password' (str): The password for authentication.
	Returns:
		vim.ServiceInstanceContent: The content object retrieved from the vCenter service instance.
	Side Effects:
		Registers a disconnect handler to cleanly close the vCenter connection upon program exit.
	Raises:
		vim.fault.InvalidLogin: If authentication fails.
		Exception: For other connection-related errors.
	"""

	service_instance = SmartConnect(
		host=vcenter_login_conf['url'],
		user=vcenter_login_conf['user'],
		pwd=vcenter_login_conf['password'],
		port='443',
		disableSslCertValidation=True)

	# Ensure vCenter connection is closed cleanly on program exit
	atexit.register(Disconnect, service_instance)
	 
	vcenter_logged_in = service_instance.RetrieveContent()
	 
	return vcenter_logged_in
