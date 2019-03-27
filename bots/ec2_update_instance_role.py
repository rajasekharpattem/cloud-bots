'''
## ec2_update_instance_role  
What it does: Updates an EXISTING EC2 instance role by attaching another policy to the role. This policy needs be passed in through the params.  
Usage: AUTO: ec2_update_instance_role policy_arn=<policy_arn>  
Example: AUTO: ec2_update_instance_role policy_arn=arn:aws:iam::aws:policy/AlexaForBusinessDeviceSetup  
Sample GSL: Instance where roles should have roles with [ managedPolicies contain [ name='AmazonEC2RoleforSSM' ] ]  
'''

import boto3
from botocore.exceptions import ClientError
 
def run_action(boto_session,rule,entity,params):
    text_output = ""

    iam_client = boto_session.client('iam')    

    ## Set up params. We need a policy ARN to come through in the params.
    usage = "Usage: AUTO: ec2_update_instance_role policy_arn=<policy_arn>Example: AUTO: ec2_update_instance_role policy_arn=arn:aws:iam::aws:policy/AlexaForBusinessDeviceSetup"
    if len(params) == 1:
        try:
            key_value = params[0].split("=")
            key = key_value[0]
            value = key_value[1]

            if key == "policy_arn":
                policy_arn = value
                text_output = text_output + "Policy ARN that we're attaching to the instance role: %s " % policy_arn
            
            else:
                text_output = text_output + "Params don't match expected values. Exiting." + usage
                return text_output  
        except:
            text_output = text_output + "Params handling error. Please check params and try again." + usage
            return text_output

    else:
        text_output = "Wrong amount of params inputs detected. Exiting." + usage
        return text_output

    # If the instance has an instance profile, try to update the role to have the new policy attached. It it's already attached, it'll still return a 200 so no need to worry about too much error handling. 
    if len(entity['roles']) > 0:  
        try:
            result = iam_client.attach_role_policy(
                RoleName=entity['roles'][0]['arn'].split("/")[1],
                PolicyArn=policy_arn
            )  
            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = text_output + "Unexpected error: %s " % str(result)
            else:
                text_output = text_output + "Policy successfully attached to instance role"

        except ClientError as e:
            text_output = text_output + "Unexpected error: %s " % e

    else:
        text_output = "No existing role found to attach the policy to. Please use ec2_attach_instance_role to do the initial attachment.Exiting"

    return text_output

