
# activate only if -t coschedule is assigned in oarsub

if 'coschedule' in types and not 'exclusive' in types:

    import math 
    # example scenario
    #resource_request=[([{'property': '', 'resources': [{'resource': 'network_address', 'value': '2'}, {'resource': 'cpu', 'value': '1'}]}], None)]
    
    # currently, it supports STATIC nodes characteristics
    cpus_per_node=2
    cores_per_cpu=12
 
    print("#ADMISSION RULE> Assigning half-socket per node")
   
    # currently, supports only one -l flag (no moldability)
    resources=resource_request[0][0][0]['resources']
    
    # retrieve resources and
    # convert everything to cores
    # (network_address=node) i.e.:
    # [1] element:
    # (a) if nodes: cores=nodes*cpus_per_node*cores_per_cpu
    # (b) if cpus: cores=cpus*cores_per_cpu
    # (c) if cores: cores=cores
    # [2] elements:
    # (d) if nodes and cpus: cores=nodes*cpus*cores_per_cpu
    # (e) if nodes and cores: cores=nodes*cpus_per_node*cores
    # (f) if cpus and cores: cores= cpus*cores
    # [3] elements:
    # (g) if nodes and cpus and cores: cores= nodes*cpus*cores
    cores=0
    if len(resources)==1:
        # (a)
        if resources[0]['resource']=='network_address': # aka node
            cores=int(resources[0]['value'])*cpus_per_node*cores_per_cpu
        # (b)
        elif resources[0]['resource']=='cpu':
            cores=int(resources[0]['value'])*cores_per_cpu
        # (c)
        elif resources[0]['resource']=='core':
            cores=int(resources[0]['value'])
        else:
            raise Exception("# ADMISSION RULE> Cannot spread job to half sockets. Aborting submission.")
    
    elif len(resources)==2:
        # (d)
        if resources[0]['resource']=='network_address' and resources[1]['resource']=='cpu':
            cores=int(resources[0]['value'])*int(resources[1]['value'])*cores_per_cpu
        # (e)
        elif resources[0]['resource']=='network_address' and resources[1]['resource']=='core':
            cores=int(resources[0]['value'])*cpus_per_node*int(resources[1]['value'])
        # (f)
        elif resources[0]['resource']=='cpu' and resources[1]['resource']=='core':
            cores=int(resources[0]['value'])*int(resources[1]['value'])
        else:
            raise Exception("# ADMISSION RULE> Cannot spread job to half sockets. Aborting submission.")
    
    elif len(resources)==3:
        # (g)
        if resources[0]['resource']=='network_address' and resources[1]['resource']=='cpu' and resources[2]['resource']=='core':
            cores=int(resources[0]['value'])*cpus_per_node*int(resources[1]['value'])*cpus_per_node*int(resources[2]['value'])
        else:
            raise Exception("# ADMISSION RULE> Cannot spread job to half sockets. Aborting submission.")
    
    else:
        raise Exception("# ADMISSION RULE> Cannot spread job to half sockets. Aborting submission.")
    
    # create a new request resource instance
    # logic: half socket filling
    
    # calculate how many cpus are needed
    # based on the fact that half space will be allocated
    # cores gets new value the half of them that exist in a cpu
    # round upwards
    cpus=math.ceil(cores/(cores_per_cpu/2.0))
    # even number of cores per cpu is acceptable
    cores=int(cores_per_cpu/2)
    
    # convert outcome to OAR guidelines
    resources=[{'resource': 'cpu', 'value': cpus}, {'resource': 'core', 'value': cores}]

    print(resources)
    
    # submit change
    resource_request[0][0][0]['resources']=resources
    
