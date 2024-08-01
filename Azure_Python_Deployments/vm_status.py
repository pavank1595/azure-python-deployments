from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import InstanceViewTypes

# Define your Azure subscription ID, resource group name, and VM name
subscription_id = '17356c73-f9cc-4e4d-a9be-7a7466852b24'
resource_group_name = 'Bicep_RG'
vm_name = 'bicep-VM'

# Authenticate using DefaultAzureCredential
credential = DefaultAzureCredential()

# Create a Compute Management Client
compute_client = ComputeManagementClient(credential, subscription_id)

# Get the VM instance view to check the status
def get_vm_status(resource_group, vm_name):
    instance_view = compute_client.virtual_machines.get(resource_group, vm_name, expand=InstanceViewTypes.instance_view)
    status = instance_view.instance_view.statuses[1].display_status
    return status

# Fetch and print the VM status
status = get_vm_status(resource_group_name, vm_name)
print(f'The status of VM "{vm_name}" is: {status}')
