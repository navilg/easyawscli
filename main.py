#!/usr/bin/python3

from os import system, name
from sys import exit
import boto3
from botocore.exceptions import ClientError
import login
import ec2
import asg
# from SecureString import clearmem

source_code_url = "https://github.com/navilg/easyawscli"

def mainMenu():
    print("\n\n---Main Menu---\n")
    print("0. Logout\n1. Start EC2 instance\n2. Stop EC2 instance\n3. Tag an instance\n4. Add inbound rule in Security Group")
    print("5. Remove an inbound rule from Security Group\n6. Autoscaling Group suspend process")
    main_menu_choice = int(input("Choose from above (0 to 6) >> "))
    
    return main_menu_choice


def subMenu(action_name=""):
    print("\n\n---Sub Menu---\n")
    print("\n0. Logout\n1. Repeat '" + str(action_name) + "'\n2. Main Menu")
    subchoice = int(input("Choose from above (0 to 2) >> "))

    return subchoice


def clear():
    print("Clear")
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


if __name__ == "__main__":
    print("\t\t----------------")
    print("\t\t| Easy AWS CLI |")
    print("\t\t----------------")
    print(source_code_url)
    region,session = login.login()
    print("Login successful")

    choice = mainMenu()
    print(choice)
    if choice == 0:
        print("Exiting...")
        exit(0)

    while True:

        if choice == 1:
            action_name = 'Start EC2 instance'
            instances_started, number_of_instance_started = ec2.startEC2(region, session)
            print(number_of_instance_started, "Instances started", instances_started)
        elif choice == 2:
            action_name = 'Stop EC2 instance'
            instances_stopped, number_of_instance_stopped = ec2.stopEC2(region, session)
            print(number_of_instance_stopped, "Instances stopped", instances_stopped)
        elif choice == 3:
            action_name = 'Tag an instance'
            ec2.addTag()
        elif choice == 4:
            action_name = 'Add inbound rule to a security group'
            sg_updated = ec2.addInboundRuleInSg(region, session)
            if sg_updated != "":
                print("Security Group", sg_updated, "updated.")
        elif choice == 5:
            action_name = 'Remove inbound rule from a security group'
            sg_updated = ec2.removeInboundRuleFromSg(region, session)
            if sg_updated != "":
                print("Security Group", sg_updated, "updated.")
        elif choice == 6:
            action_name = 'Suspend autoscaling process'
            asg.suspendProcess()
        elif choice == 0:
            exit(0)
        else:
            print("Wrong choice")
            exit(1)

        subchoice = subMenu(action_name)
        if subchoice == 0:
            exit(0)
        elif subchoice == 1:
            continue
        elif subchoice == 2:
            choice = mainMenu()
        else:
            print("Wrong choice")
            exit(1)


