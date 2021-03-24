#!/usr/bin/python3

from os import system, name
import boto3
from botocore.exceptions import ClientError
import getpass
#from SecureString import clearmem

def mainmenu():
    print("AWS CLI Interface\n")
    print("0. Exit\n1. Start EC2 instance\n2. Stop EC2 instance\n3. Tag an instance\n4. Add IP in SG\n5. Remove an IP from SG\n6. Autoscaling Group suspend process")
    mainmenu_choice = int(input("Choose from above (0 to 5): "))
    
    return mainmenu_choice

def submenu():
    print("\n0. Exit\n1. Repeat\n2. Main Menu")
    subchoice = int(input("Choose from above (0 to 2): "))

    return subchoice

def login():
    print("\n\n---Login---\n")
    region = str(input("Enter instance region: ")).lower()
    key = str(input("Enter AWS access key: "))
    try: 
        secret = getpass.getpass(prompt='Enter AWS secret: ') 
    except Exception as error: 
        print('ERROR', error)
        exit(1)
    
    try:
        session = boto3.Session(
        aws_access_key_id = key,
        aws_secret_access_key = secret,
        region_name = region
        )
        #clearmem(secret)
    except ClientError as e:
        print(e.response['Error']['Message'])
        #clearmem(secret)
        exit(1)
    
    print("Validating your credentials...")
    sts = session.client('sts')
    try:
        sts.get_caller_identity()
    except ClientError as e:
        print(e.response['Error']['Message'])
        print("Login failed")
        exit(1)
    
    return region,session

def listEC2(region,state,tagname,tagvalue,session):
    print("Searching instances with tag","'"+tagname+":", tagvalue+"'","in region", region)
    ec2_instances = []
    ec2_obj = session.resource('ec2',region_name=region)
    filters = [{'Name': 'instance-state-name','Values': [state]},{'Name': 'tag:'+tagname,'Values': [tagvalue]}]

    for instance in ec2_obj.instances.filter(Filters=filters):
        ip = instance.private_ip_address
        state_name = instance.state['Name']
        print("ip:{}, state:{}".format(ip,state_name))
        ec2_instances.append(instance)

    return ec2_instances

def startEC2(region,session):
    print("\n\n---Start EC2 Instance---\n")
    print("Active region:",region)
    tagname = str(input("Enter tag name: "))
    tagvalue = str(input("Enter tag value: "))
    ec2_instances = listEC2(region,'stopped',tagname,tagvalue,session)
    print("Instances to start: ",ec2_instances)

    if ec2_instances is None:
        print("No stopped instances to start.")
        return [],0

    confirm = str(input("Do you confirm ? (Type 'confirm'): "))
    if confirm != 'confirm':
        print("You seem to be confused.")
        return [],0
    
    print("Starting Instances...")
    instance_state_changed = 0
    instances_started = []

    for instance in ec2_instances:
        print("Starting instance ",instance)
        try:
            instance.start()
            instances_started.append(instance)
            instance_state_changed += 1
        except ClientError as e:
            print(e.response['Error']['Message'])
    
    return instances_started,instance_state_changed

def stopEC2(region,session):
    print("\n\n---Stop EC2 Instance---\n")
    print("Active region:",region)
    tagname = str(input("Enter tag name: "))
    tagvalue = str(input("Enter tag value: "))
    ec2_instances = listEC2(region,'running',tagname,tagvalue,session)
    print("Instances to stop: ",ec2_instances)

    if ec2_instances is None:
        print("No running instances to stop.")
        return [],0

    confirm = str(input("Do you confirm ? (Type 'confirm'): "))
    if confirm != 'confirm':
        print("You seem to be confused.")
        return [],0
    
    print("Stopping Instances...")
    instance_state_changed = 0
    instances_stopped = []

    for instance in ec2_instances:
        print("Stopping instance ",instance)
        try:
            instance.stop()
            instances_stopped.append(instance)
            instance_state_changed += 1
        except ClientError as e:
            print(e.response['Error']['Message'])
    
    return instances_stopped,instance_state_changed

def tagInstance():
    print("tagInstance")

def addIPinEC2():
    print("addIPinEC2")

def removeIPfromEC2():
    print("removeIPfromEC2")

def suspendProcess():
    print("suspendProcess")

def clear():
    print("Clear")
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

if __name__ == "__main__":
    choice = mainmenu()
    print(choice)

    region,session = login()
    print("Login successful")

    while True:

        if choice == 1:
            instances_started,number_of_instance_started = startEC2(region,session)
            print(number_of_instance_started, "Instances started", instances_started)
        elif choice == 2:
            instances_stopped,number_of_instance_stopped = stopEC2(region,session)
            print(number_of_instance_stopped, "Instances stopped", instances_stopped)
        elif choice == 3:
            tagInstance()
        elif choice == 4:
            addIPinEC2()
        elif choice == 5:
            removeIPfromEC2()
        elif choice == 6:
            suspendProcess()
        elif choice == 0:
            exit(0)
        else:
            print("Wrong choice")
            exit(1)
        
        subchoice = submenu()
        if subchoice == 0:
            exit(0)
        elif subchoice == 1:
            continue
        elif subchoice == 2:
            choice = mainmenu()
        else:
            print("Wrong choice")
            exit(1)


