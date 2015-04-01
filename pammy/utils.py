'''Pammy utils'''

def subnet_complement(supernet, existing_subnets):
    '''Return the complement of subnets for the given supernet and it's existing subnets'''
    for possible_subnet in supernet.subnet(supernet.prefixlen + 1):
        if any(possible_subnet in current_subnet for current_subnet in existing_subnets):
            continue
        elif any(current_subnet in possible_subnet for current_subnet in existing_subnets):
            for subnet in subnet_complement(possible_subnet, existing_subnets):
                yield subnet
        else:
            yield possible_subnet
