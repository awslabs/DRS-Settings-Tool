# DRS Settings Tool

## Description
This tool was created to help change settings in bulk for multiple Elastic Disaster Recovery Service(DRS) Source Servers.

## Prerequisites

- Basic understanding of JSON formatting. Some of the fields that are editable, are presented in JSON format. If they are not formatted correctly, this could cause failures in the tool.
- Install [Python 3](https://www.python.org/downloads/). This tool was created and tested with Python 3.12.3.
- Install [pip](https://pip.pypa.io/en/stable/installation/#get-pip-py)
- Install [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) 
- Active Source Servers in AWS Elastic Disaster Recovery Service
- Connectivity to the following endpoints for the API calls to succeed:
    - drs.`<region>`.amazonaws.com
    - kms.`<region>`.amazonaws.com
    - iam.`<region>`.amazonaws.com
    - ec2.`<region>`.amazonaws.com
- IAM user(s) that has the appropriate permissions noted below:

**For single account use, use the IAM permissions below for the DRS Settings Tool user:**
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "drs:UpdateReplicationConfiguration",
                "drs:UpdateLaunchConfiguration",
                "drs:GetLaunchConfiguration",
                "drs:GetReplicationConfiguration",
                "drs:DescribeSourceServers",
                "ec2:DescribeInstances",
                "ec2:DescribeLaunchTemplateVersions",
                "ec2:DescribeSecurityGroups",
                "ec2:CreateLaunchTemplateVersion",
                "ec2:DescribeImages",
                "ec2:ModifyLaunchTemplate",
                "ec2:DescribeSubnets",
                "ec2:DescribeKeyPairs",
                "ec2:CreateSecurityGroup",
                "ec2:DescribeInstanceTypeOfferings",
                "ec2:CreateTags",
                "iam:GetInstanceProfile",
                "kms:DescribeKey",
                "kms:CreateGrant",
                "ec2:GetEbsDefaultKmsKeyId"
            ],
            "Resource": "*"
        }
    ]
}
```

**For extended account use, use the IAM permissions below for the DRS Settings Tool users:**

Staging Account User Permissions:
	
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "drs:GetReplicationConfiguration",
                "kms:DescribeKey",
                "kms:CreateGrant",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "drs:UpdateReplicationConfiguration",
                "ec2:CreateSecurityGroup",
                "ec2:CreateTags",
		"ec2:GetEbsDefaultKmsKeyId"
            ],
            "Resource": "*"
        }
    ]
}
```

Extended/Target Account User Permissions:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "drs:DescribeSourceServers",
		"drs:GetLaunchConfiguration",
                "ec2:DescribeLaunchTemplateVersions",
                "ec2:DescribeInstanceTypeOfferings",
                "ec2:DescribeInstances",
                "ec2:DescribeKeyPairs",
                "ec2:DescribeImages",
                "iam:GetInstanceProfile",
                "drs:UpdateLaunchConfiguration",
                "ec2:CreateLaunchTemplateVersion",
                "ec2:DescribeLaunchTemplateVersions",
                "ec2:ModifyLaunchTemplate",
                "ec2:CreateTags"
            ],
            "Resource": "*"
        }
    ]
}
```
**PLEASE NOTE**: If you have a mix of extended and non-extended servers, it is best to apply the whole policy to each user for the "single account use" guidance above. The above is just an example of minimum required permissions in a basic scenario.

- The AWS credentials + config file should be updated to have profiles which are named after the account number of each staging and target account. 
    - The credentials and config file are located in the following locations:
        - Windows: ```C:\Users\<username>\.aws```
        - Linux: ```~/.aws/```
    - Example of the entries you should have:
      
credentials file:
```
[<Staging-Account-ID>]
aws_access_key_id = <Access-Key>
aws_secret_access_key = <Secret-Key>

[<Target-Account-ID>]
aws_access_key_id = <Access-Key>
aws_secret_access_key = <Secret-Key>
```

config file:
```
[profile <Staging-Account-ID>]
region = us-east-1
output = json

[profile <Target-Account-ID>]
region = us-east-1
output = json 
```

**PLEASE NOTE**: The scripts will fail if you do not setup your AWS credentials and config file as noted above, as it relies on this configuration to make API calls to the respective accounts for each setting. For single account use, you can have just one credentials profile and one config entry.


## Installation
- Clone or download the desired file format locally on the computer in which you have the AWS credentials file configured, and ensure AWS Endpoint connectivity for API calls. 

## Usage
1. Ensure you configured your AWS credentials file and are pointing to the correct region. You can do this by setting the appropriate region in your credentials profile specific config settings (noted in the pre-requisites).
2. Run the "get_settings.py" file. You will be prompted to enter the "Target Account ID". The "Target Account" will be the account in which your source servers would launch into during recovery. For single account use, use that single account number. For accounts with DRS source servers that are extended, use the account number where the servers are extended to. This script will create two files in the directory named "DRS_Settings.csv" and "DRS_Settings_DO_NOT_EDIT.csv". **NOTE** Everytime you would like to edit the settings, please ensure you generate the LATEST CSV's by running the "get_settings.py" file.
3. Open the "DRS_Settings.csv" file in the CSV file editor of choice(Microsoft Excel for example), and make all the desired changes for each source server. **NOTE** It is important that you do NOT modify the "DRS_Settings_DO_NOT_EDIT.csv" file as we will use this as a comparison to limit AWS API calls being made for servers that have not been changed.
4. Run the "update_settings.py" file to update the settings for all your Source Servers in DRS.
5. A log will be generated in the directory named "DRS-Update-Tool.log", for troubleshooting purposes.

## Available Settings for each field
- **Right Sizing**
    - `NONE | BASIC | IN_AWS`
- **Copy Private IP**
    - `True | False`
- **Copy Tags**
    - `True | False`
- **Launch Disposition**
    - `STOPPED | STARTED`
- **Launch Into Instance**
    - `<instance-id>` (For example, i-1234abcde567fg)
- **BYOL**
    - `True | False`
- **Target Key Pair**
    - `<key-pair>` (This is whatever the name of your Key Pair is)
- **Target Instance Type**
    - `<instance-type>` (For example, t2.medium)
- **Target AMI ID**
    - `<ami-id>` (For example, ami-123abc456def)
- **Target Network Settings**
    - **Notes:**
        - **DeviceIndex:** Do not change or edit this field.
        - **Adding additional network interfaces:** Note that the EC2 launch template only supports two network interfaces. If you require more than two network interfaces, you will need to define them after the test or cutover instance has been launched. This can be done through a post-launch action
    -
        ```
        [
            {
                'AssociatePublicIpAddress': True|False,
                'DeleteOnTermination': True|False,
                'Description': 'string',
                'DeviceIndex': 123,
                'Groups': [
                    'string',
                ],
                'InterfaceType': 'string',
                'Ipv6AddressCount': 123,
                'Ipv6Addresses': [
                    {
                        'Ipv6Address': 'string'
                    },
                ],
                'NetworkInterfaceId': 'string',
                'PrivateIpAddress': 'string',
                'PrivateIpAddresses': [
                    {
                        'Primary': True|False,
                        'PrivateIpAddress': 'string'
                    },
                ],
                'SecondaryPrivateIpAddressCount': 123,
                'SubnetId': 'string',
                'PrimaryIpv6': True|False,
            },
        ]

- **Target Disk Settings**
    - **Notes**:
        - **DeviceName:** Do not change or edit this field
        - **VolumeSize:** Do not change or edit this field
        - **Iops & Throughput:** Set the number of I/O operations per second that the volume can support. You can select any number as long as it matches the [EBS guidelines](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html).
    - 
        ```
        [
            {
                'DeviceName': 'string',
                'Ebs': {
                    'Encrypted': True|False,
                    'DeleteOnTermination': True|False,
                    'Iops': 123,
                    'KmsKeyId': 'string',
                    'VolumeSize': 123,
                    'VolumeType': 'standard'|'io1'|'io2'|'gp2'|'sc1'|'st1'|'gp3',
                    'Throughput': 123
                },
            },
        ]
- **Target Instance Profile Role Name**
    - `<iam-role-name>` (For exmaple, AmazonSSMRoleForInstancesQuickSetup)
- **Target Instance Tags**
    -   ```
        [
            {
                'Key': 'string',
                'Value': 'string'
            },
        ]
- **Target Volume Tags**
    -   ```
        [
            {
                'Key': 'string',
                'Value': 'string'
            },
        ]
- **Use Default Replication Security Group**
    - `True | False`
- **Auto Replicate New Disks**
    - `True | False`
- **Bandwidth Throttling**
    - `123` (Provide an integer value (Mbps))
- **Create Public IP for Replication Server**
    - `True | False`
- **Use Private IP for Data Replication**
    - `PRIVATE_IP | PUBLIC_IP`
- **Default Large Staging Disk Type**
    - `GP2 | GP3 | ST1 | AUTO`
- **PIT Retention Setting(Days)**
    - `1-365` (Integer value between 1-365)
- **Replication Server Instance Type**
    - `<instance-type>` (For example, t2.medium)
- **Staging Disk Settings**
    - **Notes**:
        - **DeviceName:** Do not change or edit this field
        - **isBootDisk:** Do not change or edit this field
        - **Iops & Throughput:** Set the number of I/O operations per second that the volume can support. You can select any number as long as it matches the [EBS guidelines](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html).
    - ```
        [
            {
                'deviceName': 'string',
                'iops': 123,
                'isBootDisk': True|False,
                'optimizedStagingDiskType': 'AUTO'|'GP2'|'GP3'|'IO1'|'SC1'|'ST1'|'STANDARD',
                'stagingDiskType': 'AUTO'|'GP2'|'GP3'|'IO1'|'SC1'|'ST1'|'STANDARD',
                'throughput': 123
            },
        ]
- **Staging Disk Encryption**
    - `DEFAULT | CUSTOM | NONE`
- **Staging Disk Encryption Key Arn**
    - `<ebs-encryption-key-arn>` (For example, arn:aws:kms:<Region>:<account-ID>:key/mrk-abcd1234efgh5678ijkl9101112)
- **Replication Server Security Groups**
    - `<security-group-id>` (For example, sg-123abc456def. If you have more than one, you can separate them with commas. For example, sg-123abc456def, sg-456abc789def)
- **Staging Subnet**
    - `<subnet-id>` (For example, subnet-123abc456def)
- **Use Dedicated Replicator**
    - `True | False`
- **Replication Tags**
    - ```
        {
            'Key': 'Value',
            'Key': 'Value'
        }


## Authors and acknowledgment

**Author**
Tim Hall

**Contributers**
Diego Valverde
Pritam Bhalerao 



