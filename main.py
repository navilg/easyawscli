#!/usr/bin/python3

from os import system, name
from sys import exit
import login
import ec2
import asg
# from SecureString import clearmem

source_code_url = "https://github.com/navilg/easyawscli"

def mainMenu():
    print("\n\n---Main Menu---\n")
    print("0. Logout\n1. Start EC2 instance\n2. Stop EC2 instance\n3. Tag (Update tag of) an instance\n4. Add inbound rule in Security Group")
    print("5. Remove an inbound rule from Security Group\n6. Autoscaling Group suspend process\n7. Terminate an Instance")
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
            instances_started, number_of_instance_started,instance_failed_to_start, number_of_ins_failed_to_start = ec2.startEC2(region, session)
            print(number_of_instance_started, "Instance/s started", instances_started)
            print("Failed to start", number_of_ins_failed_to_start, "instance/s.", instance_failed_to_start)

        elif choice == 2:
            action_name = 'Stop EC2 instance'
            instances_stopped, number_of_instance_stopped, instance_failed_to_stop, number_of_ins_failed_to_stop = ec2.stopEC2(region, session)
            print(number_of_instance_stopped, "Instance/s stopped", instances_stopped)
            print("Failed to stop", number_of_ins_failed_to_stop, "instance/s.", instance_failed_to_stop)

        elif choice == 3:
            action_name = 'Tag an instance'
            instances_tagged, number_of_instances_tagged, instance_failed_to_tag, number_of_ins_failed_to_tag = ec2.addTag(region, session)
            print(number_of_instances_tagged, "instance/s has been tagged.", instances_tagged)
            print("Failed to tag", number_of_ins_failed_to_tag, "instance/s.", instance_failed_to_tag)

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

        elif choice == 7:
            action_name = 'Terminate an instance'
            instances_terminated, number_of_instances_terminated, instance_failed_to_terminate, number_of_ins_failed_to_terminate = ec2.terminateEc2(region, session)
            print(number_of_instances_terminated, "instance/s has been terminated.", instances_terminated)
            print("Failed to terminate", number_of_ins_failed_to_terminate, "instance/s.", instance_failed_to_terminate)

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