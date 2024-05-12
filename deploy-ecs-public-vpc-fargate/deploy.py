import boto3

cloudformation = boto3.client('cloudformation')


##Variables
ecs_security_group = "ECSSecurityGroup"
alb_security_group = "ALBSecurityGroup"

gif_api_target_group = "GifApiTargetGroup"
prime_checker_target_group = "PrimeCheckerTargetGroup"

vpc_id = "vpc-0ed7419a484c71bf0"
subnet_ids ="subnet-01e5a2c504271c633, subnet-042624b1683145840, subnet-05d12327efc80a3e8"

ecs_cluster = "ECSCluster"
capabilities = ['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM']


sec_group_stack = "multi-service-deployment-createALBAndECSSecuirityGroups"
ecs_creation_stack = "multi-service-deployment-createECS"
alb_creation_stack = "multi-service-deployment-createALB"


# ==========create two securitygroups for ecs and alb

parameters = [
    {
        'ParameterKey': 'VpcId',
        'ParameterValue': vpc_id
    },
    {
        'ParameterKey': 'ALBSecurityGroup',
        'ParameterValue': alb_security_group
    },
    {
        'ParameterKey': 'ECSSecurityGroup',
        'ParameterValue': ecs_security_group
    },
]

ecs_creation_response = cloudformation.create_stack(
    StackName=sec_group_stack,
    TemplateBody=open('securitygroups/template.yaml', 'r').read(),
    Parameters=parameters,
    Capabilities=capabilities
)

print("Creating ECS and ALB Secuirity groups")
waiter = cloudformation.get_waiter('stack_create_complete')
waiter.wait(StackName=sec_group_stack)
print(f"ECS and ECS Secuirity groups created ")



# ===========  get security group ids from the stack
sec_group_ids = cloudformation.describe_stacks(StackName=sec_group_stack)['Stacks'][0]['Outputs']
alb_security_group_id = None
ecs_security_group_id = None

for output in sec_group_ids:
    if output['ExportName'] == alb_security_group:
        alb_security_group_id = output['OutputValue']
    elif output['ExportName'] == ecs_security_group:
        ecs_security_group_id = output['OutputValue']

if(alb_security_group == None or ecs_security_group == None):
    print("Error getting security group ids")
    exit(1)

print(f" \n | ALB Security Group ID: {alb_security_group_id} |\n|ECS Security Group ID: {ecs_security_group_id} \n |")




# ============== Create the Application load balancer and listner rules ==========
parameters = [
    {
        'ParameterKey': 'VpcId',
        'ParameterValue': vpc_id
    },
    {
        'ParameterKey': 'SubnetIds',
        'ParameterValue': subnet_ids
    },
    {
        'ParameterKey': 'AlbSecurityGroupId',
        'ParameterValue': alb_security_group_id,
    }
]
alb_creation_response = cloudformation.create_stack(
    StackName= alb_creation_stack,
    TemplateBody=open('alb/template.yaml', 'r').read(),
    Parameters=parameters,
    Capabilities=capabilities
)

print("Creating ALB and Target Groups")
waiter = cloudformation.get_waiter('stack_create_complete')
waiter.wait(StackName=alb_creation_stack)
print(f"ALB and Target Groups created")


#get target group Ids
target_group_ARNS = cloudformation.describe_stacks(StackName=alb_creation_stack)['Stacks'][0]['Outputs']
gif_api_tg = None
primechecket_tg = None
for output in target_group_ARNS:
    if output['OutputKey'] == "GifApiTargetGroup":
        gif_api_tg = output['OutputValue']
    elif output['OutputKey'] == "PrimeCheckerTargetGroup":
        primechecker_tg = output['OutputValue']

if(gif_api_target_group == None or primechecker_tg == None):
    print("Error getting target group IDS")
    exit(1)

print(f" \n | GIF API Target group:{gif_api_tg}  |\n| Prime Checker Targetgroup: {primechecker_tg} |")

# Create ECS cluster and target groups
parameters = [
    {
        'ParameterKey': 'VpcId',
        'ParameterValue': vpc_id
    },
    {
        'ParameterKey': 'SubnetIds',
        'ParameterValue': subnet_ids
    },
    {
        'ParameterKey': 'ECSSecuirityGroups',
        'ParameterValue': ecs_security_group_id
    },
    {
        'ParameterKey': 'GifApiTargetGroup',
        'ParameterValue': gif_api_tg
    },

    {
        'ParameterKey': 'PrimeCheckerTargetGroup',
        'ParameterValue': primechecker_tg
    },


]
ecs_creation_response = cloudformation.create_stack(
    StackName= ecs_creation_stack,
    TemplateBody=open('ecs/template.yaml', 'r').read(),
    Parameters=parameters,
    Capabilities=capabilities
)

print("Creating ECS Cluster")
waiter = cloudformation.get_waiter('stack_create_complete')
waiter.wait(StackName=ecs_creation_stack)
print(f"ECS Cluster created")





