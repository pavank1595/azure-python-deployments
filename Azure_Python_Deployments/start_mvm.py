from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import HttpResponseError

# Define your Azure subscription ID
subscription_id = '17356c73-f9cc-4e4d-a9be-7a7466852b24'

# List of VMs with their resource group names
vm_list = [
    {'resource_group': 'Bicep_RG', 'vm_name': 'bicep-VM'},
    {'resource_group': 'Jenkins_RG', 'vm_name': 'Jenkins-Server'},
    {'resource_group': 'Tomcat_RG', 'vm_name': 'Tomcat-Server'}
]

# Authenticate using DefaultAzureCredential
credential = DefaultAzureCredential()

# Create Compute Management Client
compute_client = ComputeManagementClient(credential, subscription_id)

# Function to start a VM
def start_vm(resource_group_name, vm_name):
    try:
        # Begin the start operation
        async_vm_start = compute_client.virtual_machines.begin_start(resource_group_name, vm_name)
        # Wait for the operation to complete
        async_vm_start.result()
        print(f'The VM "{vm_name}" in resource group "{resource_group_name}" has been successfully started.')
    except HttpResponseError as e:
        print(f'An error occurred while starting VM "{vm_name}" in resource group "{resource_group_name}": {e.message}')

# Start all VMs in the list
for vm_info in vm_list:
    start_vm(vm_info['resource_group'], vm_info['vm_name'])
