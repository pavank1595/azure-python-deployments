from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

subscription_id = '17356c73-f9cc-4e4d-a9be-7a7466852b24'

def list_all_vms():
    """Lists all VMs in a subscription."""

    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)

    for vm in compute_client.virtual_machines.list_all():
        print(f"VM Name: {vm.name}")
        print(f"VM Location: {vm.location}")
        print("-" * 30)
        # Add more properties as needed

list_all_vms()
