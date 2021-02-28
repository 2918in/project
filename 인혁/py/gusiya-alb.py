from troposphere import elasticloadbalancingv2 as elb

from troposphere import (
 Ref,
 GetAtt,
 ImportValue,
 Output,
 Parameter,
 Join,
 Select,
 Sub,
 Split,
 Template,
 ec2,
 Export
)

t = Template()

t.set_description("ALB for gusiya web")

t.add_resource(ec2.SecurityGroup(
 "LoadBalancerSG",
 GroupDescription="Web Load Balancer",
 VpcId=ImportValue(
  Join("-", [Select(0, Split("-", Ref("AWS::StackName"))), "cluster-vpc-id"])
 ),
 SecurityGroupIngress=[
  ec2.SecurityGroupRule(
   IpProtocol="tcp",
   FromPort="80",
   ToPort="80",
   CidrIp="0.0.0.0/0"
  )
 ]
))

t.add_resource(elb.LoadBalancer(
 "LoadBalancer",
 Scheme="internet-facing",
 Subnets=Split(",",
    ImportValue(Join("-", [Select(0, Split("-", Ref("AWS::StackName"))), "cluster-public-subnets"])
    )
 ),
 SecurityGroups=[Ref("LoadBalancerSG")],
))

t.add_resource(elb.TargetGroup(
 "TargetGroup",
 DependsOn='LoadBalancer',
 HealthCheckIntervalSeconds="20",
 HealthCheckProtocol="HTTP",
 HealthCheckTimeoutSeconds="15",
 HealthyThresholdCount="5",
 Matcher=elb.Matcher(
  HttpCode="200"),
 Port="80",
 Protocol="HTTP",
 UnhealthyThresholdCount="3",
 VpcId=ImportValue(Join("-",
   [Select(0, Split("-", Ref("AWS::StackName"))), "cluster-vpc-id"])
 )
))

t.add_resource(elb.Listener(
 "Listener",
 Port="80",
 Protocol="HTTP",
 LoadBalancerArn=Ref("LoadBalancer"),
 DefaultActions=[elb.Action(
  Type="forward",
    TargetGroupArn=Ref("TargetGroup")
 )]
))

t.add_output(Output(
 "TargetGroup",
 Description="TargetGroup",
 Value=Ref("TargetGroup"),
 Export=Export(Sub("${AWS::StackName}-target-group")),
))

t.add_output(Output(
 "URL",
 Description="Helloworld URL",
 Value=Join("", ["http://", GetAtt("LoadBalancer", "DNSName")])
))

print(t.to_json())
 
