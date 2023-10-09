from aws_cdk import (
    # Duration,
    aws_ec2 as ec2,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        # vpc = ec2.Vpc(self, "ArgoVPC")
        vpc = ec2.Vpc(self, "CustomVPC",
            max_azs=2,
            subnet_configuration=[
            ec2.SubnetConfiguration(
                name="PublicSubnet",
                subnet_type=ec2.SubnetType.PUBLIC,  # This ensures instances get a public IP
        ),
        # ... other subnet configurations ...
    ]
)
        # Define security group for our EC2
        sg = ec2.SecurityGroup(self, "ArgoSG", vpc=vpc)

        # Allow inbound traffic on port 8086 (InfluxDB) and 3000 (Grafana) and 22 (ssh)
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8086))
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(3000))
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443))
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80))
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22))


        # Create the EC2 instance
        ec2.Instance(self, "ArgoEC2",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.lookup(
                name="ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*",
                owners=["099720109477"]  # Canonical's owner ID for public Ubuntu images
            ),
            vpc=vpc,
            security_group=sg,
            key_name="Ec2KeyPair"  # Replace with your EC2 key pair name
        )
