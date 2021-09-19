import boto3
from botocore.exceptions import ClientError
import getpass

def login():
    print("\n\n---Login---\n")
    region = setRegion()
    if region == "":
        exit(0)

    key = str(input("Enter AWS access key >> "))
    try: 
        secret = getpass.getpass(prompt='Enter AWS secret (Input text will NOT be visible) >> ')
    except Exception as error: 
        print('ERROR', error)
        exit(1)

    try:
        session = boto3.Session(aws_access_key_id=key, aws_secret_access_key=secret, region_name=region)
        # clearmem(secret)
    except ClientError as e:
        print(e.response['Error']['Message'])
        # clearmem(secret)
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

def setRegion():
    print("Choose one region from list below.")
    print("------------------------------------------------------------------------------------------------------------"
          "-------------------------------------")
    print("|  1.  us-east-1 (N. Virginia)\t\t2.  us-east-2 (Ohio)\t\t3.  us-west-1 (N. California)\t\t4.  us-west-2 ("
          "Oregon)\t\t|")
    print("|  5.  af-south-1 (Cape Town)\t\t6.  ap-east-1 (Hong Kong)\t7.  ap-south-1 (Mumbai)\t\t\t8.  "
          "ap-northeast-3 ( "
          "Osaka)\t|")
    print("|  9.  ap-northeast-2 (Seoul)\t\t10. ap-southeast-1 (Singapore)\t11. ap-southeast-2 (Sydney)\t\t12. "
          "ap-northeast-1 (Tokyo)\t|")
    print("|  13. ca-central-1 (Canada/Central)\t14. eu-central-1 (Frankfurt)\t15. eu-west-1 (Ireland)\t\t\t16. "
          "eu-west-2 (London)\t\t|")
    print("|  17. eu-south-1 (Milan)\t\t18. eu-west-3 (Paris)\t\t19. eu-north-1 (Stockholm)\t\t20. me-south-1 ("
          "Bahrain)\t|")
    print("|  21. sa-east-1 (Sao Paulo)\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t|")
    print("------------------------------------------------------------------------------------------------------------"
          "-------------------------------------\n")

    while True:
        try:
            region_name = int(input("Choose a region from above (1 to 21). Type 0 to exit: "))
        except ValueError as e:
            print('Invalid choice')
            continue
        except Exception as e:
            print("Error:", e)
            return ""

        if region_name == 1:
            return "us-east-1"
        elif region_name == 2:
            return "us-east-2"
        elif region_name == 3:
            return "us-west-1"
        elif region_name == 4:
            return "us-west-2"
        elif region_name == 5:
            return "af-south-1"
        elif region_name == 6:
            return "ap-east-1"
        elif region_name == 7:
            return "ap-south-1"
        elif region_name == 8:
            return "ap-northeast-3"
        elif region_name == 9:
            return "ap-northeast-2"
        elif region_name == 10:
            return "ap-southeast-1"
        elif region_name == 11:
            return "ap-southeast-2"
        elif region_name == 12:
            return "ap-northeast-1"
        elif region_name == 13:
            return "ca-central-1"
        elif region_name == 14:
            return "eu-central-1"
        elif region_name == 15:
            return "eu-west-1"
        elif region_name == 16:
            return "eu-west-2"
        elif region_name == 17:
            return "eu-south-1"
        elif region_name == 18:
            return "eu-west-3"
        elif region_name == 19:
            return "eu-north-1"
        elif region_name == 20:
            return "me-south-1"
        elif region_name == 21:
            return "sa-east-1"
        elif region_name == 0:
            return ""
        else:
            print("Invalid choice.")

