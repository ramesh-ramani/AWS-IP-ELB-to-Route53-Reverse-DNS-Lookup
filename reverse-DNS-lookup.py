import boto3
import os
import sys

##Below lines will connect to the AWS Route53 Client##


def sgcheck(i,client,input,ip_or_cname):
  print("*************",i,"*************")
  paginate_hosted_zones = client.get_paginator('list_hosted_zones')
  paginate_resource_record_sets = client.get_paginator('list_resource_record_sets')

  domains = [domain.lower().rstrip('.') for domain in sys.argv[1:]]

  for zone_page in paginate_hosted_zones.paginate():
     for zone in zone_page['HostedZones']:
        if domains and not zone['Name'].lower().rstrip('.') in domains:
            continue

        for record_page in paginate_resource_record_sets.paginate(HostedZoneId = zone['Id']):
            for record in record_page['ResourceRecordSets']:
                if record.get('ResourceRecords'):
                    for target in record['ResourceRecords']:
                        if record['Type'] == ip_or_cname and input in target['Value']:
                           print((zone['Id'].split("/"))[2], "Zone is: ", zone['Name'], " URL is: ",record['Name'],str(ip_or_cname)," Record is: ",target['Value'], ". Account is: ", i) 
                elif record.get('AliasTarget'):
                     if record['Type'] == ip_or_cname and input in target['Value']:
                        print((zone['Id'].split("/"))[2], "Zone is: ", zone['Name'], " URL is: ",record['Name'],str(ip_or_cname)," Record is: ", record['AliasTarget']['DNSName'], ". Account is: ", i)
                else:
                    raise Exception('Unknown record type: {}'.format(record))


def account_check(account,ELB,ip_or_cname):
   lst = [] ##Add Name(s) of account as defined in your AWS creds file
   if not account:
      for i in lst:
         session = boto3.Session(profile_name=i,region_name='eu-central-1')
         client = session.client('route53')
         check=sgcheck(i,client,ELB,ip_or_cname)
   else: 
       session = boto3.Session(profile_name=account,region_name='eu-central-1') 
       client = session.client('route53')
       check=sgcheck(account,client,ELB,ip_or_cname) 
      

while True:
   user_input=input("ELB or IP?: ")
   if user_input=="ELB" or user_input=="IP": break
user_inp_account=input("Account?: ")
if user_input=="ELB": 
   ELB=input("Enter ELB: ")
   ip_or_cname="CNAME"
   if not user_inp_account: 
      print("\n*****No Account input entered and hence checking all accounts*****\n") 
      account_check(user_inp_account,ELB,ip_or_cname)
   else: account_check(user_inp_account,ELB,ip_or_cname)
elif user_input=="IP": 
   IP=input("Enter IP: ")
   ip_or_cname="A"
   if not user_inp_account:
      print("\n*****No Account input entered and hence checking all accounts*****\n") 
      account_check(user_inp_account,IP,ip_or_cname)
   else: 
       account_check(user_inp_account,IP,ip_or_cname)

#if check != 1: print("This is not added as a Record in Route 53 in the ") 
   
