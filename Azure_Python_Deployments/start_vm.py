from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import HttpResponseError

# Define your Azure subscription ID, resource group name, and VM name
subscription_id = '17356c73-f9cc-4e4d-a9be-7a7466852b24'
resource_group_name = 'Jenkins_RG'
vm_name = 'Jenkins-Server'

# Authenticate using DefaultAzureCredential
credential = DefaultAzureCredential()

# Create a Compute Management Client
compute_client = ComputeManagementClient(credential, subscription_id)

# Function to start a VM
def start_vm(resource_group, vm_name):
    try:
        # Begin the start operation
        async_vm_start = compute_client.virtual_machines.begin_start(resource_group, vm_name)
        # Wait for the operation to complete
        async_vm_start.result()
        print(f'The VM "{vm_name}" has been successfully started.')
    except HttpResponseError as e:
        print(f'An error occurred: {e.message}')

# Start the VM
start_vm(resource_group_name, vm_name)
