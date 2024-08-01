from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient


subscription_id = '17356c73-f9cc-4e4d-a9be-7a7466852b24'

vm_list = []

def list_all_vms():
    """Lists all VMs with their resource groups in a subscription."""

    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)
    resource_client = ResourceManagementClient(credential, subscription_id)
    
    for rg in resource_client.resource_groups.list():
        if rg == "NetworkWatcherRG":
            pass
        else:
            vm_info = {}
            for vm in compute_client.virtual_machines.list(rg.name):
                if rg.name == "NetworkWatcherRG":
                    pass
                else:
                    print(f"Resource Group: {rg.name}")
                    print(f"VM Name: {vm.name}")
                    print(f"VM Location: {vm.location}")
                    # Add more properties as needed
                    print("-" * 30)
                vm_info['resource_group'] = rg.name
                vm_info['vm_name'] = vm.name
                vm_list.append(vm_info)
    print(vm_list)
         

list_all_vms()