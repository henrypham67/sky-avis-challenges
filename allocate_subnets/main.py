from collections import defaultdict


class Subnet:
    def __init__(self, id, az, weight):
        self.id = id
        self.az = az
        self.weight = weight

    def __repr__(self):
        return f"  Subnet {self.id} (AZ: {self.az}, Weight: {self.weight})"


class NATInstance:
    def __init__(self, id, az):
        self.id = id
        self.az = az
        self.weight = 0
        self.associated_subnets = []

    def __repr__(self):
        return f"Instance {self.id} (AZ: {self.az}):"


def find_least_loaded_nat(nat_list):
    return min(nat_list, key=lambda nat: nat.weight, default=None)


class NATAllocator:
    def __init__(self):
        self.nat_instances = []
        self.subnets = []
        self.nat_by_az = defaultdict(list)

    def add_nat_instance(self, nat_instance):
        self.nat_instances.append(nat_instance)
        self.nat_by_az[nat_instance.az].append(nat_instance)

    def add_subnet(self, subnet):
        self.subnets.append(subnet)

    def allocate_subnets(self):
        for subnet in self.subnets:
            if self.nat_by_az[subnet.az]:
                selected_nat = find_least_loaded_nat(self.nat_by_az[subnet.az])
            else:
                all_available_nats = [nat for nats in self.nat_by_az.values() for nat in nats]
                selected_nat = find_least_loaded_nat(all_available_nats)

            if selected_nat:
                selected_nat.associated_subnets.append(subnet)
                selected_nat.weight += subnet.weight
            else:
                print(f"No healthy NAT instances available for subnet {subnet.id}")


# Define the NAT instances and their AZs
nat_instances = {
    1: 'us-west1-a',
    2: 'us-west1-b',
    3: 'us-west1-c'
}

# Define the subnets, their AZs, and weights
subnets = {
    1: {'az': 'us-west1-a', 'weight': 10},
    2: {'az': 'us-west1-b', 'weight': 20},
    3: {'az': 'us-west1-b', 'weight': 5},
    4: {'az': 'us-west1-c', 'weight': 15},
    5: {'az': 'us-west1-d', 'weight': 10},
    6: {'az': 'us-west1-b', 'weight': 25}
}

# Create a NAT manager and add instances and subnets
nat_allocator = NATAllocator()

for id, az in nat_instances.items():
    nat_allocator.add_nat_instance(NATInstance(id, az))

for id, info in subnets.items():
    nat_allocator.add_subnet(Subnet(id, info['az'], info['weight']))

# Allocate subnets to NAT instances
nat_allocator.allocate_subnets()

# Print the allocation results
for nat_instance in nat_allocator.nat_instances:
    print(nat_instance)
    for subnet in nat_instance.associated_subnets:
        print(subnet)
