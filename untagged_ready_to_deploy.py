import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

Topic_Arn = 'arn:aws:sns:us-east-1:342786247368:autoshutdown'
account = "AWS-ITIO"

#define the connection
ec2 = boto3.resource('ec2')
s = ""
value_null=[]

def lambda_handler(event, context):
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    filters = [
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]

    #filter the instances
    instances = ec2.instances.filter(Filters=filters)

    #locate Untagged untagged instances
    name_untaggedInstances = [instance.id for instance in instances if 'Name' not in [t['Key'] for t in instance.tags]]
    #The below line was added for debugging
    print name_untaggedInstances
    #commenting out the unwanted tags from the list of all the logs

    app_untaggedInstances = [instance.id for instance in instances if 'Application' not in [t['Key'] for t in instance.tags]]
    print app_untaggedInstances
    appown_untaggedInstances = [instance.id for instance in instances if 'ApplicationOwner' not in [t['Key'] for t in instance.tags]]
    print appown_untaggedInstances
    untaggedInstances = name_untaggedInstances + app_untaggedInstances + appown_untaggedInstances
    print 'instance Dont have value against Name tags are '
    inst=""
    print "We will get the instance list"
    for instance in instances:
#        print instance.id
        inst=get_instance_name(instance.id)
#  print inst
    #make sure there are actually instances to shut down.
    s=""
    untaggedInstances = untaggedInstances + value_null
    untaggedInstances = list(set(untaggedInstances))

    print "This will be final print before shutdown.."

    print untaggedInstances

    if len(untaggedInstances) > 0:
            #perform the shutdown
        for instance in untaggedInstances:
            s+=instance + "\n"
#        print s
#        stopInstance(ListRunningUnTaggedInstances)
#        publish_to_sns(s)
    else:
        print "Nothing to see here..!"
def stopInstance(instanceId):
#    instanceId = ['TestingID']
    ec2.instances.filter(InstanceIds=instanceId).stop()


def publish_to_sns(message):
    sns = boto3.client('sns')
    sns_message = str(message)
    response = sns.publish(TopicArn=Topic_Arn,Subject = "Instance Shutdown Notification for account " + account, Message = sns_message)

def get_instance_name(fid):
    # When given an instance ID as str e.g. 'i-1234567', return the instance 'Name' from the name tag.
    ec2instance = ec2.Instance(fid)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
            if len(instancename) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)
        if tags["Key"] == 'Application':
            application = tags["Value"]
            if len(application) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)
        if tags["Key"] == 'ApplicationOwner':
            applicationowner = tags["Value"]
            if len(applicationowner) <= 0:
                print ec2instance.id
                value_null.append(ec2instance.id)


