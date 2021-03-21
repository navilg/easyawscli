#!/usr/bin/python3

from os import system, name
import boto3
from botocore.exceptions import ClientError
import getpass

def mainmenu():
    print("AWS CLI Interface\n")
    print("0. Exit\n1. Start EC2 instance\n2. Stop EC2 instance\n3. Tag an instance\n4. Add IP in SG\n5. Remove an IP from SG\n6. Autoscaling Group suspend process")
    mainmenu_choice = int(input("Choose from above (0 to 5): "))
    
    return(mainmenu_choice)

def startEC2():
    print("\n\n---Start EC2 Instance---\n")
    print("Enter below details")
    tagname = str(input("Enter tag name: "))
    tagvalue = str(input("Enter tag value: "))
    region = str(input("Enter instance region: ")).lower()
    key = str(input("Enter AWS access key: "))
    try: 
        secret = getpass.getpass(prompt='Enter AWS secret: ') 
    except Exception as error: 
        print('ERROR', error)

    print("Starting instance with tag","'"+tagname+":", tagvalue+"'","in region", region)

def stopEC2():
    print("stopEC2")

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
    try:
        choice = mainmenu()
        print(choice)

        if choice == 1:
            startEC2()
        elif choice == 2:
            stopEC2()
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
    except:
        print("\nExiting")
        exit(2)

