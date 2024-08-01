from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import HardwareProfile, StorageProfile, OSProfile, NetworkProfile, VirtualMachine, NetworkInterfaceReference
from azure.mgmt.network.models import NetworkInterface, NetworkInterfaceIPConfiguration, VirtualNetwork, Subnet, PublicIPAddress, PublicIPAddressSku, NetworkSecurityGroup, SecurityRule

# Define your Azure subscription ID
subscription_id = '17356c73-f9cc-4e4d-a9be-7a7466852b24'

# Define the location (e.g., 'eastus', 'westus', etc.)
location = 'northeurope'

# Define the resource group and VM details
resource_group_name = 'myResourceGroup'
vm_name = 'myVM'
vm_size = 'Standard_B1s'
username = 'azureuser'
password = 'yourPassword123!'  # Use secure methods for handling passwords
image_publisher = 'OpenLogic'
image_offer = 'CentOS'
image_sku = '8_2-gen2'

# Authentication using DefaultAzureCredential
credentials = DefaultAzureCredential()

# Initialize the Resource Management Client
resource_client = ResourceManagementClient(credentials, subscription_id)

# Create the resource group
resource_group_params = {
    'location': location
}
resource_client.resource_groups.create_or_update(resource_group_name, resource_group_params)
print(f'Resource Group {resource_group_name} created successfully.')

# Initialize the Network Management Client
network_client = NetworkManagementClient(credentials, subscription_id)

# Create Virtual Network
vnet_name = 'myVnet'
subnet_name = 'mySubnet'
nic_name = 'myNic'
public_ip_name = 'myPublicIP'
nsg_name = 'myNSG'

# Define virtual network parameters
vnet_params = VirtualNetwork(
    location=location,
    address_space={'address_prefixes': ['10.0.0.0/16']}
)

# Create the virtual network
async_vnet_creation = network_client.virtual_networks.begin_create_or_update(
    resource_group_name,
    vnet_name,
    vnet_params
)
vnet_result = async_vnet_creation.result()

# Define subnet parameters
subnet_params = Subnet(
    address_prefix='10.0.0.0/24'
)

# Create the subnet
async_subnet_creation = network_client.subnets.begin_create_or_update(
    resource_group_name,
    vnet_name,
    subnet_name,
    subnet_params
)
subnet_result = async_subnet_creation.result()

# Define public IP address parameters
public_ip_params = PublicIPAddress(
    location=location,
    public_ip_allocation_method='Dynamic',
    sku=PublicIPAddressSku(name='Basic')
)

# Create the public IP address
async_public_ip_creation = network_client.public_ip_addresses.begin_create_or_update(
    resource_group_name,
    public_ip_name,
    public_ip_params
)
public_ip_result = async_public_ip_creation.result()
print(f'Public IP Address {public_ip_name} created successfully.')

# Define Network Security Group parameters
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
            name='allow-rdp',
            priority=1001,
            direction='Inbound',
            access='Allow',
            protocol='Tcp',
            source_port_range='*',
            destination_port_range='3389',
            source_address_prefix='*',
            destination_address_prefix='*'
        ),
        SecurityRule(
            name='allow-8080',
            priority=1002,
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

# Create the Network Security Group
async_nsg_creation = network_client.network_security_groups.begin_create_or_update(
    resource_group_name,
    nsg_name,
    nsg_params
)
nsg_result = async_nsg_creation.result()
print(f'Network Security Group {nsg_name} created successfully.')

# Define network interface parameters
nic_params = NetworkInterface(
    location=location,
    ip_configurations=[
        NetworkInterfaceIPConfiguration(
            name='myNicIPConfig',
            primary=True,
            private_ip_allocation_method='Dynamic',
            subnet={'id': subnet_result.id},
            public_ip_address={'id': public_ip_result.id}
        )
    ],
    network_security_group={'id': nsg_result.id}  # Associate the NSG with the NIC
)

# Create the network interface
async_nic_creation = network_client.network_interfaces.begin_create_or_update(
    resource_group_name,
    nic_name,
    nic_params
)
nic_result = async_nic_creation.result()
print(f'Network Interface {nic_name} created successfully.')

# Initialize the Compute Management Client
compute_client = ComputeManagementClient(credentials, subscription_id)

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

# Wait for the VM creation to complete
vm_result = async_vm_creation.result()
print(f'VM {vm_name} created successfully.')
