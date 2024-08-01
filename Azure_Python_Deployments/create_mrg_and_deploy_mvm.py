from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import HardwareProfile, StorageProfile, OSProfile, NetworkProfile, VirtualMachine, NetworkInterfaceReference
from azure.mgmt.network.models import NetworkInterface, NetworkInterfaceIPConfiguration, VirtualNetwork, Subnet, PublicIPAddress, PublicIPAddressSku, NetworkSecurityGroup, SecurityRule
from azure.core.exceptions import HttpResponseError

# Define your Azure subscription ID
subscription_id = '17356c73-f9cc-4e4d-a9be-7a7466852b24'

# Define the location
location = 'centralus'

# Define the lists of resource groups and VM names
resource_group_names = ['DEV_RG', 'SIT_RG', 'UAT_RG']
vm_names = ['DEV-VM', 'SIT-VM', 'UAT-VM']

# Define other parameters
vm_size = 'Standard_B1s'
username = 'testuser'
password = 'testuser@123'  # In a real application, use a secure way to handle passwords
image_publisher = 'OpenLogic'
image_offer = 'CentOS'
image_sku = '8_2-gen2'

# Authentication using DefaultAzureCredential
credentials = DefaultAzureCredential()

# Initialize clients
resource_client = ResourceManagementClient(credentials, subscription_id)
network_client = NetworkManagementClient(credentials, subscription_id)
compute_client = ComputeManagementClient(credentials, subscription_id)

for resource_group_name, vm_name in zip(resource_group_names, vm_names):
    vnet_name = f'{resource_group_name}-vnet'
    subnet_name = f'{resource_group_name}-subnet'
    nic_name = f'{resource_group_name}-nic'
    public_ip_name = f'{resource_group_name}-publicip'
    nsg_name = f'{resource_group_name}-nsg'

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

        # Create Network Security Group with rules
        nsg_params = NetworkSecurityGroup(
            location=location,
            security_rules=[
                SecurityRule(
                    name='allow-ssh',
                    priority=1000,
                    direction='Inbound',
                    access='Allow',
                    protocol='Tcp',
                    source_port_range='*',
                    destination_port_range='22',
                    source_address_prefix='*',
                    destination_address_prefix='*'
                ),
                SecurityRule(
                    name='allow-8080',
                    priority=1001,
                    direction='Inbound',
                    access='Allow',
                    protocol='Tcp',
                    source_port_range='*',
                    destination_port_range='8080',
                    source_address_prefix='*',
                    destination_address_prefix='*'
                )
            ]
        )
        async_nsg_creation = network_client.network_security_groups.begin_create_or_update(
            resource_group_name,
            nsg_name,
            nsg_params
        )
        nsg_result = async_nsg_creation.result()
        print(f'Network Security Group {nsg_name} created successfully.')

        # Create Network Interface with NSG
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
            ],
            network_security_group={'id': nsg_result.id}  # Associate the NSG with the NIC
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
                admin_username=username,
                admin_password=password
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
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
