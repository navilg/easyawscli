#!/usr/bin/python3

from os import system, name
import boto3
from botocore.exceptions import ClientError
import getpass
import datetime
# from SecureString import clearmem


def main_menu():
    print("\n\n---Main Menu---\n")
    print("0. Exit/Logout\n1. Start EC2 instance\n2. Stop EC2 instance\n3. Tag an instance\n4. Add IP in SG\n5. Remove an IP from SG\n6. Autoscaling Group suspend process")
    main_menu_choice = int(input("Choose from above (0 to 5): "))
    
    return main_menu_choice


def submenu():
    print("\n0. Logout\n1. Repeat\n2. Main Menu")
    subchoice = int(input("Choose from above (0 to 2): "))

    return subchoice


def login():
    print("\n\n---Login---\n")
    region = str(input("Enter instance region: ")).lower()
    key = str(input("Enter AWS access key: "))
    try: 
        secret = getpass.getpass(prompt='Enter AWS secret (Input text will NOT be visible): ')
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
    try:
        sts = session.client('sts')
        sts.get_caller_identity()
    except ClientError as e:
        print(e.response['Error']['Message'])
        print("Login failed")
        exit(1)
    except Exception as e:
        print(e, ":", type(e).__name__)
        if type(e).__name__ == "EndpointConnectionError":
            print("'"+region+"'","may not be a valid AWS region.")
        print("Login Failed")
        exit(1)
    
    return region,session


def get_ec2(region,state,tagname,tagvalue,session):
    print("Searching instances with tag","'"+tagname+":", tagvalue+"'","in region", region)
    reservations = []
    ec2_obj = session.client('ec2',region_name=region)
    filters = [{'Name': 'instance-state-name','Values': [state]},{'Name': 'tag:'+tagname,'Values': [tagvalue]}]

    reservations = ec2_obj.describe_instances(Filters=filters).get("Reservations")

    return reservations,ec2_obj

def startEC2(region,session):
    print("\n\n---Start EC2 Instance---\n")
    print("Active region:",region)
    tagname = str(input("Enter tag name: "))
    tagvalue = str(input("Enter tag value: "))
    reservations,ec2_obj = get_ec2(region,'stopped',tagname,tagvalue,session)

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

    print("\nChoose instances to start from above list (0 to "+str(i)+"). Separate them by commas.")
    start_choice = input("Example: 1,3,4: ")
    choice_list = start_choice.rstrip().split(",")
    print("Instances to start:", choice_list)
    confirm = str(input("Do you confirm ? (Type 'confirm'): "))
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
    tagname = str(input("Enter tag name: "))
    tagvalue = str(input("Enter tag value: "))
    reservations,ec2_obj = get_ec2(region,'running',tagname,tagvalue,session)

    # If list is empty
    if not reservations:
        print("No running instances to stop.")
        return [],0

    ###################################

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

    print("\nChoose instances to stop from above list (0 to " + str(i) + "). Separate them by commas.")
    start_choice = input("Example: 1,3,4: ")
    choice_list = start_choice.rstrip().split(",")
    print("Instances to stop:", choice_list)
    confirm = str(input("Do you confirm ? (Type 'confirm'): "))
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
    print("Easy AWS CLI\n")
    choice = main_menu()
    print(choice)
    if choice == 0:
        print("Exiting...")
        exit(0)
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
            choice = main_menu()
        else:
            print("Wrong choice")
            exit(1)


