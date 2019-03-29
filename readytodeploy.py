import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)
value_null=[]
Key_null=[]

Topic_Arn = 'Topic_Arn'
account = "My account"
#define the connection
ec2 = boto3.resource('ec2')
s = ""
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
    for instance in instances:
        #print instance.id
        if not instance.tags:
            #print "No tags!!!"
            Key_null.append(instance.id)
        else:
            if 'Name' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
            if 'Application' not in [t['Key'] for t in instance.tags]:    
                Key_null.append(instance.id)
            if 'ApplicationOwner' not in [t['Key'] for t in instance.tags]:
                Key_null.append(instance.id)
            get_instance_name(instance.id)        
 #   print list(set(value_null))
    print "Count of instance having one or more tags missing %d" %len(list(set(Key_null)))
    print "Count of all Instances having one or more key missing  %d" %len(list(set(value_null)))
    print " "
    untaggedInstances = Key_null + value_null
    untaggedInstances = list(set(untaggedInstances))

    if len(untaggedInstances) > 0:
            #perform the shutdown
        for instance in untaggedInstances:
            s+=instance + "\n"
        print s
    #    stopInstance(untaggedInstances)
        publish_to_sns(s)
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
