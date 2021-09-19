import boto3
from botocore.exceptions import ClientError
from requests import get
from sys import exit

def getEc2(region,state,tagname,tagvalue,session):
    print("Searching instances with tag","'"+tagname+":", tagvalue+"'","in region", region)
    reservations = []
    ec2_obj = session.client('ec2',region_name=region)
    if state == "all":
        filters = [{'Name': 'tag:' + tagname, 'Values': [tagvalue]}]
    else:
        filters = [{'Name': 'instance-state-name','Values': [state]},{'Name': 'tag:'+tagname,'Values': [tagvalue]}]

    reservations = ec2_obj.describe_instances(Filters=filters).get("Reservations")

    return reservations,ec2_obj

def startEC2(region,session):
    print("\n\n---Start EC2 Instance---\n")
    print("Active region:",region)
    tagname = str(input("Enter tag name >> "))
    tagvalue = str(input("Enter tag value >> "))
    reservations,ec2_obj = getEc2(region,'stopped',tagname,tagvalue,session)

    # If list is empty
    if not reservations:
        print("No stopped instances to start.")
        return [],0

    print("\nBelow instances found with tag '" + tagname + "':'" + tagvalue + "'")
    print("No.\tInstance_ID\t\t" + tagname + "\t\tPrivate_IP_Address\t\tLaunch_Time")
    i = 0
    for reservation in reservations:
        for instance in reservation["Instances"]:
            i += 1
            instance_id = instance["InstanceId"]
            private_ip = instance["PrivateIpAddress"]
            launch_time = instance["LaunchTime"]
            print(str(i)+"\t"+str(instance_id)+"\t"+tagvalue+"\t\t"+str(private_ip)+"\t\t"+str(launch_time))

    print("\nChoose instances to start from above list (0 to "+str(i)+"). Separate them by commas. Just type 0 to return to submenu.")
    start_choice = input("Example: 1,3,4 >> ")
    if start_choice == '0':
        return [],0
    choice_list = start_choice.rstrip().split(",")
    print("Instances to start:", choice_list)
    confirm = str(input("Do you confirm ? (Type 'confirm') >> "))
    if confirm != 'confirm':
        print("You seem to be confused.")
        return [],0
    
    print("Starting Instances...")
    instance_state_changed = 0
    instances_started = []

    i = 0
    for reservation in reservations:
        for instance in reservation["Instances"]:
            i += 1
            if str(i) in choice_list:
                try:
                    print("Starting instance ", instance["InstanceId"])
                    ec2_obj.start_instances(InstanceIds=[instance["InstanceId"]])
                    instances_started.append(instance["InstanceId"])
                    instance_state_changed += 1
                except ClientError as e:
                    print(e.response['Error']['Message'])

    return instances_started,instance_state_changed


def stopEC2(region,session):
    print("\n\n---Stop EC2 Instance---\n")
    print("Active region:",region)
    tagname = str(input("Enter tag name >> "))
    tagvalue = str(input("Enter tag value >> "))
    reservations,ec2_obj = getEc2(region,'running',tagname,tagvalue,session)

    # If list is empty
    if not reservations:
        print("No running instances to stop.")
        return [],0

    print("\nBelow instances found with tag '" + tagname + "':'" + tagvalue + "'")
    print("No.\tInstance_ID\t\t" + tagname + "\t\tPrivate_IP_Address\t\tLaunch_Time")
    i = 0
    for reservation in reservations:
        for instance in reservation["Instances"]:
            i += 1
            instance_id = instance["InstanceId"]
            private_ip = instance["PrivateIpAddress"]
            launch_time = instance["LaunchTime"]
            print(str(i) + "\t" + str(instance_id) + "\t" + tagvalue + "\t\t" + str(private_ip) + "\t\t" + str(launch_time))

    print("\nChoose instances to stop from above list (0 to " + str(i) + "). Separate them by commas. Just type 0 to return to submenu.")
    stop_choice = input("Example: 1,3,4 >> ")
    if stop_choice == '0':
        return  [],0
    choice_list = stop_choice.rstrip().split(",")
    print("Instances to stop:", choice_list)
    confirm = str(input("Do you confirm ? (Type 'confirm') >> "))
    if confirm != 'confirm':
        print("You seem to be confused.")
        return [], 0

    print("Stopping Instances...")
    instance_state_changed = 0
    instances_stopped = []

    i = 0
    for reservation in reservations:
        for instance in reservation["Instances"]:
            i += 1
            if str(i) in choice_list:
                try:
                    print("Stopping instance ", instance["InstanceId"])
                    ec2_obj.stop_instances(InstanceIds=[instance["InstanceId"]])
                    instances_stopped.append(instance["InstanceId"])
                    instance_state_changed += 1
                except ClientError as e:
                    print(e.response['Error']['Message'])

    return instances_stopped,instance_state_changed

def addInboundRuleInSg(region,session):
    print("\n\n---Add inbound rule in Security Group---\n")
    print("Active region:", region)
    print("Enter tag name and its value to filter the EC2 instances.")
    tagname = str(input("Enter tag name >> "))
    tagvalue = str(input("Enter tag value >> "))
    reservations, ec2_obj = getEc2(region, 'all', tagname, tagvalue, session)

    # If list is empty
    if not reservations:
        print("No instances found.")
        return ""

    print("\nBelow instances found with tag '" + tagname + "':'" + tagvalue + "'")
    print("No.\tInstance_ID\t\t" + tagname + "\t\tVPC_ID\t\tPrivate_IP_Address\t\tLaunch_Time")
    i = 0
    for reservation in reservations:
        for instance in reservation["Instances"]:
            i += 1
            instance_id = instance["InstanceId"]
            private_ip = instance["PrivateIpAddress"]
            launch_time = instance["LaunchTime"]
            vpc_id = instance["VpcId"]
            print(str(i) + "\t" + str(instance_id) + "\t" + tagvalue + "\t\t" + str(vpc_id) + "\t\t" + str(private_ip) + "\t\t" + str(launch_time))


    print("\nChoose one instances from above list (0 to " + str(i) + "). 0 to return to submenu")
    instance_choice = int(input("Example: 3 >> "))

    if instance_choice == 0:
        return  ""

    print("Below Security Groups are attached to chosen instance.")
    print("No.\tSecurity_Group_ID\t\tSecurity_Group_Name")

    i = 0
    security_group_id_list = []
    security_group_name_list = []
    for reservation in reservations:
        for instance in reservation["Instances"]:
            i += 1
            if i == instance_choice:
                security_groups = instance["SecurityGroups"]
                j = 0
                for security_group in security_groups:
                    j += 1
                    security_group_name = security_group["GroupName"]
                    security_group_id = security_group["GroupId"]
                    security_group_name_list.append(security_group_name)
                    security_group_id_list.append(security_group_id)
                    print(str(j) + "\t" + str(security_group_id) + "\t\t" + security_group_name)
                break

    print("\nChoose one security group from above (0 to", j,"). Type 0 to return to submenu.")
    security_group_choice = int(input(">> "))

    if security_group_choice == 0:
        return ""

    security_group_details = ec2_obj.describe_security_groups(GroupIds=[security_group_id_list[security_group_choice - 1]])

    print("Below inbound rules are currently authorized to security group", security_group_id_list[security_group_choice - 1])
    print("No.\tPorts\t\tIP_Protocol\tSource\t\t\t\tDescription")
    i = 0
    for ip_permission in security_group_details['SecurityGroups'][0]['IpPermissions']:
        i += 1
        current_ip_protocol = ip_permission['IpProtocol']
        current_ip_ranges = ip_permission['IpRanges']
        current_cidrs = []
        current_description = []
        for current_ip_range in current_ip_ranges:
            current_cidrs.append(current_ip_range['CidrIp'])
            if 'Description' in current_ip_range:
                current_description.append(current_ip_range['Description'])
            else:
                current_description.append('')
        current_to_port = ip_permission['ToPort']
        print(str(i) + "\t" + str(current_to_port) + "\t\t" + str(current_ip_protocol) + "\t\t" + str(current_cidrs) + "\t\t\t\t" + str(current_description))

    if i == 0:
        print("No inbound rule authorized to security group", security_group_id_list[security_group_choice - 1])

    print("\nEnter below details for new inbound rule.")
    ip_protocol = str(input("Enter IP Protocol (tcp/udp) >> ")).lower()
    to_port = int(input("Enter port number >> "))
    your_public_ip = str(get('http://ipinfo.io/json').json()['ip']) + "/32"
    ip_range = str(input("Enter CIDR IP (default: {}) >> ".format(your_public_ip)))
    description = str(input("Enter description (default: '') >> "))

    if ip_range == "":
        ip_range = your_public_ip

    ip_perm = [{'IpProtocol': ip_protocol, 'ToPort': to_port,  'FromPort': to_port, 'IpRanges': [{'CidrIp': ip_range, 'Description': description}]}]

    print(ip_perm)
    confirm = str(input("Do you confirm ? (Type 'confirm') >> "))
    if confirm != 'confirm':
        print("You seem to be confused.")
        return ""

    print("Adding inbound rule", ip_perm, "to", security_group_id_list[security_group_choice - 1])
    try:
        ec2_obj.authorize_security_group_ingress(GroupId=security_group_id_list[security_group_choice - 1],IpPermissions=ip_perm)
        print("Inbound rule added to security group", security_group_id_list[security_group_choice - 1])
    except ClientError as e:
        print(e.response['Error']['Message'])
        return ""

    return str(security_group_id_list[security_group_choice - 1])


def removeInboundRuleFromSg(region,session):
    print("\n\n---Remove an inbound rule from Security Group---\n")
    print("Active region:", region)
    print("Enter tag name and its value to filter the EC2 instances.")
    tagname = str(input("Enter tag name >> "))
    tagvalue = str(input("Enter tag value >> "))
    reservations, ec2_obj = getEc2(region, 'all', tagname, tagvalue, session)

    # If list is empty
    if not reservations:
        print("No instances found.")
        return ""

    print("\nBelow instances found with tag '" + tagname + "':'" + tagvalue + "'")
    print("No.\tInstance_ID\t\t" + tagname + "\t\tVPC_ID\t\tPrivate_IP_Address\t\tLaunch_Time")
    i = 0
    for reservation in reservations:
        for instance in reservation["Instances"]:
            i += 1
            instance_id = instance["InstanceId"]
            private_ip = instance["PrivateIpAddress"]
            launch_time = instance["LaunchTime"]
            vpc_id = instance["VpcId"]
            print(str(i) + "\t" + str(instance_id) + "\t" + tagvalue + "\t\t" + str(vpc_id) + "\t\t" + str(
                private_ip) + "\t\t" + str(launch_time))

    print("\nChoose one instances from above list (0 to " + str(i) + "). 0 to return to submenu")
    instance_choice = int(input("Example: 3 >> "))

    if instance_choice == 0:
        return ""

    print("Below Security Groups are attached to chosen instance.")
    print("No.\tSecurity_Group_ID\t\tSecurity_Group_Name")

    i = 0
    security_group_id_list = []
    security_group_name_list = []
    for reservation in reservations:
        for instance in reservation["Instances"]:
            i += 1
            if i == instance_choice:
                security_groups = instance["SecurityGroups"]
                j = 0
                for security_group in security_groups:
                    j += 1
                    security_group_name = security_group["GroupName"]
                    security_group_id = security_group["GroupId"]
                    security_group_name_list.append(security_group_name)
                    security_group_id_list.append(security_group_id)
                    print(str(j) + "\t" + str(security_group_id) + "\t\t" + security_group_name)
                break

    print("\nChoose one security group from above (0 to", j, "). Type 0 to return to submenu.")
    security_group_choice = int(input(">> "))

    if security_group_choice == 0:
        return ""

    security_group_details = ec2_obj.describe_security_groups(GroupIds=[security_group_id_list[security_group_choice - 1]])

    print("Below inbound rules are authorized to security group",security_group_id_list[security_group_choice - 1])
    print("No.\tPorts\t\tIP_Protocol\tSource\t\t\t\tDescription")
    i = 0
    ip_protocol_list = []
    ip_ranges_list = []
    to_port_list = []
    for ip_permission in security_group_details['SecurityGroups'][0]['IpPermissions']:
        i += 1
        ip_protocol = ip_permission['IpProtocol']
        ip_protocol_list.append(ip_protocol)
        ip_ranges = ip_permission['IpRanges']
        ip_ranges_list.append(ip_ranges)
        cidrs = []
        description = []
        for ip_range in ip_ranges:
            cidrs.append(ip_range['CidrIp'])
            if 'Description' in ip_range:
                description.append(ip_range['Description'])
            else:
                description.append('')
        to_port = ip_permission['ToPort']
        to_port_list.append(to_port)
        print(str(i) + "\t" + str(to_port) + "\t\t" + str(ip_protocol) + "\t\t" + str(cidrs) + "\t\t\t\t" + str(description))

    if i == 0:
        print("No inbound rule authorized to security group",security_group_id_list[security_group_choice - 1])
        return ""

    print("Choose one of the rule to revoke from above(0 to",i,"). Type 0 to return to submenu.")
    inbound_rule_choice = int(input(">> "))

    if inbound_rule_choice == 0:
        return ""

    if len(ip_ranges_list[inbound_rule_choice - 1]) > 1:
        j = 0
        cidrs_list = []
        description_list = []
        print("There are multiple source/iprange in chosen inbound rule.")
        print("No.\tSource\t\t\t\tDescription")
        for ip_range in ip_ranges_list[inbound_rule_choice - 1]:
            j += 1
            if 'Description' in ip_range:
                print(str(j) + "\t" + ip_range['CidrIp'] + "\t\t\t\t" + ip_range['Description'])
                cidrs_list.append(ip_range['CidrIp'])
                description_list.append(ip_range['Description'])
            else:
                print(str(j) + "\t" + ip_range['CidrIp'] + "\t\t\t\t" + "''")
                cidrs_list.append(ip_range['CidrIp'])
                description_list.append('')

        print("\nChoose any one from above source (0 to",j,"). Type 0 to return to submenu.")
        source_choice = int(input(">> "))

        if source_choice == 0:
            return ""

        if description_list == '':
            ip_perm = [{'IpProtocol': ip_protocol_list[inbound_rule_choice - 1],
                        'ToPort': to_port_list[inbound_rule_choice - 1],
                        'FromPort': to_port_list[inbound_rule_choice - 1],
                        'IpRanges': [{'CidrIp': cidrs_list[source_choice - 1]}]}]
        else:
            ip_perm = [{'IpProtocol': ip_protocol_list[inbound_rule_choice - 1],
                        'ToPort': to_port_list[inbound_rule_choice - 1],
                        'FromPort': to_port_list[inbound_rule_choice - 1],
                        'IpRanges': [{'CidrIp': cidrs_list[source_choice - 1], 'Description': description_list[source_choice - 1]}]}]
    else:
        ip_perm = [{'IpProtocol': ip_protocol_list[inbound_rule_choice - 1], 'ToPort': to_port_list[inbound_rule_choice - 1], 'FromPort': to_port_list[inbound_rule_choice - 1], 'IpRanges': ip_ranges_list[inbound_rule_choice - 1]}]

    print(ip_perm)
    confirm = str(input("Do you confirm ? (Type 'confirm') >> "))
    if confirm != 'confirm':
        print("You seem to be confused.")
        return ""

    print("Removing inbound rule", ip_perm, "from", security_group_id_list[security_group_choice - 1])
    try:
        ec2_obj.revoke_security_group_ingress(GroupId=security_group_id_list[security_group_choice - 1],IpPermissions=ip_perm)
        print("Inbound rule removed from security group", security_group_id_list[security_group_choice - 1])
    except ClientError as e:
        print(e.response['Error']['Message'])
        return ""

    return str(security_group_id_list[security_group_choice - 1])

def addTag():
    pass
