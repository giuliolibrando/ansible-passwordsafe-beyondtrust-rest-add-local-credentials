#!/usr/bin/env python
import sys
import os
import requests
import sys
import json
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


os.environ['PS_HOST_NAME'] = str(sys.argv[1])
os.environ['PS_HOST_IP'] = str(sys.argv[2])
os.environ['PS_HOST_OS'] = str(sys.argv[3])
os.environ['PS_AUTH_KEY'] = str(sys.argv[4])
os.environ['PS_RUN_AS'] = str(sys.argv[5])
os.environ['PS_BASE_URL'] = str(sys.argv[6])


def getEnvVariable(variable):
        try:
                return os.environ[variable]
        except:
                sys.stderr.write(variable + ' environment variable not found\n')
                return


# Password safe API URL
BASEURL = getEnvVariable('PS_BASE_URL')

# Authorization key provided by Password Safe Management Team
AUTH_KEY = getEnvVariable('PS_AUTH_KEY')

# User that will be logged on audit controls in the Password Safe
RUN_AS = getEnvVariable('PS_RUN_AS')

# 
#global HOST_NAME
HOST_NAME = getEnvVariable('PS_HOST_NAME')

#
#global HOST_IP 
HOST_IP = getEnvVariable('PS_HOST_IP')

#
#global HOST_OS 
HOST_OS = getEnvVariable('PS_HOST_OS')

print ("creating header")
#############################################################
# Creating session
print ("Creating Session")
header = {'Authorization': 'PS-Auth key=' + AUTH_KEY + '; runas=' + RUN_AS}
session = requests.Session()
session.headers.update(header)
print (session.headers)

#############################################################
# Logging in
print ("Logging In")
response = session.post(url = BASEURL + '/Auth/SignAppin', verify = False)
print("Login Response")
print (response.status_code)


# get asset
#response = session.get(url = BASEURL + '/Workgroups/BeyondTrust Workgroup/Assets', verify = False )
#requests = json.loads(response.text)
#print("Assets  Response")
#print (response.status_code)
#print (response.json())

##############################################################
# Creating New Asset
print ("Creating New Asset")
postData = {
'AssetName': HOST_NAME,
'DnsName': HOST_NAME + 'yourdomain',
'DomainName': 'WORKGROUP',
'IPAddress': HOST_IP,
'MacAddress': 'None',
'AssetType': 'Server'
}


response = session.post(url = BASEURL + '/Workgroups/BeyondTrust Workgroup/Assets', json = postData, verify = False)
requests = json.loads(response.text)
print ("Assets POST Response")
print (response.status_code)
print (response.content)
assetID = str(requests['AssetID'])



####################################################
# Add new asset to Managed System
# Create a new request
# here you need to check id assigned to windows and linux and change accordingly
print ("Creating Managed System")
if HOST_OS == 'windows':
        plat_id = 1
        func_id = 2
        port = "null"
elif HOST_OS == 'linux':
        plat_id = 1001
        func_id = 5
        port = 22

postData2 = {
'PlatformID': plat_id,
'Port': port,
'AutoManagementFlag': 'true',
'FunctionalAccountID': func_id
}
response = session.post(url = BASEURL + '/Assets/' + assetID + '/ManagedSystems', json = postData2, verify = False)
requests = json.loads(response.text)
print ("Assets Managed POST Response")
print (response.status_code)
print (response.content)
managedSystemID = str( requests['ManagedSystemID'])


############################################################
# Add new Managed User to Managed System
# Create a new request
print ("Creating Managed User")
if HOST_OS == 'windows':
        host_user = 'user'
        host_password = 'password'
elif HOST_OS == 'linux':
        host_user = 'user'
        host_password = 'password'

postData3 = {
'AccountName' : host_user,
'Password': host_password
}
response = session.post(url = BASEURL + '/ManagedSystems/' + managedSystemID + '/ManagedAccounts', json = postData3, verify = False)
#requests = json.loads(response.text)
print ("Account Managed POST Response")
print (response.status_code)
#print (response.json())

#############################################################
# Logging out
print ("Log Out")
response = session.post(url = BASEURL + '/Auth/Signout', verify = False)
print("Logout Response")
print (response.status_code)
