from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import HardwareProfile, StorageProfile, OSProfile, NetworkProfile, VirtualMachine, NetworkInterfaceReference
from azure.mgmt.network.models import NetworkInterface, NetworkInterfaceIPConfiguration, VirtualNetwork, Subnet, PublicIPAddress, PublicIPAddressSku
from azure.core.exceptions import HttpResponseError

# Define your Azure subscription ID
subscription_id = '17356c73-f9cc-4e4d-a9be-7a7466852b24'

# Define the location
location = 'australia east'

# Define the lists of resource groups, VM names, and their configurations
resource_group_names = ['Dev_RG', 'SIT_RG']

# VM configurations for each resource group
vm_configurations = [
    {
        'vm_name': 'Dev-VM',
        'vm_size': 'Standard_B1s',
        'image_publisher': 'OpenLogic',
        'image_offer': 'CentOS',
        'image_sku': '8_2-gen2',
        'admin_username': 'azureuser',
        'admin_password': 'yourPassword123!'
    },
    {
        'vm_name': 'SIT-VM',
        'vm_size': 'Standard_D2s_v3',
        'image_publisher': 'canonical',
        'image_offer': 'ubuntu-24_04-lts',
        'image_sku': 'server',
        'admin_username': 'azureadmin',
        'admin_password': 'anotherPassword123!'
    }
]

# Authentication using DefaultAzureCredential
credentials = DefaultAzureCredential()

# Initialize clients
resource_client = ResourceManagementClient(credentials, subscription_id)
network_client = NetworkManagementClient(credentials, subscription_id)
compute_client = ComputeManagementClient(credentials, subscription_id)

for resource_group_name, vm_config in zip(resource_group_names, vm_configurations):
    vm_name = vm_config['vm_name']
    vm_size = vm_config['vm_size']
    image_publisher = vm_config['image_publisher']
    image_offer = vm_config['image_offer']
    image_sku = vm_config['image_sku']
    admin_username = vm_config['admin_username']
    admin_password = vm_config['admin_password']

    vnet_name = f'{resource_group_name}-vnet'
    subnet_name = f'{resource_group_name}-subnet'
    nic_name = f'{resource_group_name}-nic'
    public_ip_name = f'{resource_group_name}-publicip'

    try:
        # Create the resource group
        resource_group_params = {'location': location}
        resource_client.resource_groups.create_or_update(resource_group_name, resource_group_params)
        print(f'Resource Group {resource_group_name} created successfully.')

        # Create Virtual Network
        vnet_params = VirtualNetwork(
            location=location,
            address_space={'address_prefixes': ['10.0.0.0/16']}
        )
        async_vnet_creation = network_client.virtual_networks.begin_create_or_update(
            resource_group_name,
            vnet_name,
            vnet_params
        )
        vnet_result = async_vnet_creation.result()
        print(f'Virtual Network {vnet_name} created successfully.')

        # Verify Virtual Network
        vnet_result_check = network_client.virtual_networks.get(resource_group_name, vnet_name)
        print(f'Verified Virtual Network: {vnet_result_check.name}')

        # Create Subnet
        subnet_params = Subnet(address_prefix='10.0.0.0/24')
        async_subnet_creation = network_client.subnets.begin_create_or_update(
            resource_group_name,
            vnet_name,
            subnet_name,
            subnet_params
        )
        subnet_result = async_subnet_creation.result()
        print(f'Subnet {subnet_name} created successfully.')

        # Create Public IP Address
        public_ip_params = PublicIPAddress(
            location=location,
            public_ip_allocation_method='Dynamic',
            sku=PublicIPAddressSku(name='Basic')
        )
        async_public_ip_creation = network_client.public_ip_addresses.begin_create_or_update(
            resource_group_name,
            public_ip_name,
            public_ip_params
        )
        public_ip_result = async_public_ip_creation.result()
        print(f'Public IP Address {public_ip_name} created successfully.')

        # Create Network Interface
        nic_params = NetworkInterface(
            location=location,
            ip_configurations=[
                NetworkInterfaceIPConfiguration(
                    name=f'{nic_name}-ipconfig',
                    primary=True,
                    private_ip_allocation_method='Dynamic',
                    subnet={'id': subnet_result.id},
                    public_ip_address={'id': public_ip_result.id}
                )
            ]
        )
        async_nic_creation = network_client.network_interfaces.begin_create_or_update(
            resource_group_name,
            nic_name,
            nic_params
        )
        nic_result = async_nic_creation.result()
        print(f'Network Interface {nic_name} created successfully.')

        # Define the VM parameters
        vm_parameters = VirtualMachine(
            location=location,
            hardware_profile=HardwareProfile(vm_size=vm_size),
            storage_profile=StorageProfile(
                image_reference={
                    'publisher': image_publisher,
                    'offer': image_offer,
                    'sku': image_sku,
                    'version': 'latest'
                }
            ),
            os_profile=OSProfile(
                computer_name=vm_name,
                admin_username=admin_username,
                admin_password=admin_password
            ),
            network_profile=NetworkProfile(
                network_interfaces=[
                    NetworkInterfaceReference(id=nic_result.id)
                ]
            )
        )

        # Create the VM
        async_vm_creation = compute_client.virtual_machines.begin_create_or_update(
            resource_group_name,
            vm_name,
            vm_parameters
        )
        vm_result = async_vm_creation.result()
        print(f'VM {vm_name} created successfully.')

    except HttpResponseError as e:
        print(f'Error in creating resources for {resource_group_name}: {e.message}')
