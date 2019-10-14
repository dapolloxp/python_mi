from msrestazure.azure_active_directory import MSIAuthentication
from azure.storage.blob import ( 
    BlockBlobService,
    )
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient
import base64, jwt, json


def demo_msi():

    # Invoke-WebRequest -Uri 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/' -Method GET -Headers @{Metadata="true"}
    
    """
    credentials = MSIAuthentication()        

    subscription_client = SubscriptionClient(credentials)
    subscription = next(subscription_client.subscriptions.list())
    subscription_id = subscription.subscription_id
    """
    #
    print("*" * 80)
    print("Using User Managed Identitiy to access blob containers:\n")
    get_blob_with_user_MSI()
    print("\n")

    print("*" * 80)
    print("Using System Managed Identities to access blob containers:\n")
    
    get_blob_with_system_MSI()
    print("\n")
    print("*" * 80)
    
    #resource_client = ResourceManagementClient(credentials, subscription_id)
    #print(subscription_id)

def get_blob_with_user_MSI():

    storage_credential = MSIAuthentication(
        client_id = '3d5368bc-4bfd-4ccf-aa6a-649a237504ec',
        resource='https://storage.azure.com/'
    )

    #print("Storage Credential {}".format(storage_credential))
    #print("Storage Token {}".format(storage_credential.token["access_token"]))
    base_64_token = storage_credential.token["access_token"] + '=='
    jwt_token = storage_credential.token["access_token"]
    
    jwt_json = jwt.decode(jwt_token, verify=False)
    json_t = json.dumps(jwt_json)
    json_dict = json.loads(json_t)
    print("MSI Token:".format(json_t))
    print("aud: {}\niss: {}\nxms_mirid: {}\n".format(json_dict['aud'], json_dict['iss'], json_dict['xms_mirid']))
   
   
    service = BlockBlobService('azuredocuments', token_credential=storage_credential)

    print("\nListing blobs in the 'azuredocs' container:\n")
    generator = service.list_blobs('azuredocs')
    for blob in generator:
        print("\tBlob name: " + blob.name)


def get_blob_with_system_MSI():

    """
    
    """    
    storage_credential = MSIAuthentication(resource='https://storage.azure.com/')



    jwt_token = storage_credential.token["access_token"]
    
    jwt_json = jwt.decode(jwt_token, verify=False)
    json_t = json.dumps(jwt_json)
    json_dict = json.loads(json_t)

    print("MSI Token:")
    print("aud: {}\niss: {}\nxms_mirid: {}\n".format(json_dict['aud'], json_dict['iss'], json_dict['xms_mirid']))
    
    service = BlockBlobService('azuredocuments', token_credential=storage_credential)

    print("\nListing blobs in the 'azuredocs' container:\n")
    generator = service.list_blobs('azuredocs')
    for blob in generator:
        print("\tBlob name: " + blob.name)

if __name__ == "__main__":
    demo_msi()