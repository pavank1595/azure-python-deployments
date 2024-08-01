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

# Function to stop and deallocate a VM
def stop_and_deallocate_vm(resource_group_name, vm_name):
    try:
        # Begin the stop (deallocate) operation
        async_vm_stop = compute_client.virtual_machines.begin_deallocate(resource_group_name, vm_name)
        # Wait for the operation to complete
        async_vm_stop.result()
        print(f'The VM "{vm_name}" in resource group "{resource_group_name}" has been successfully stopped and deallocated.')
    except HttpResponseError as e:
        print(f'An error occurred while stopping and deallocating VM "{vm_name}" in resource group "{resource_group_name}": {e.message}')

# Stop and deallocate all VMs in the list
for vm_info in vm_list:
    if vm_info['resource_group'] == "Bicep_RG":
        pass
    else:
        stop_and_deallocate_vm(vm_info['resource_group'], vm_info['vm_name'])
