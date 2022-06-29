import requests

def airtable_download(table,  api_key=None, base_id=None, record_id=None):
    """Makes a request to Airtable for all records from a single table.
        Returns data in dictionary format.
    Keyword Arguments:
    • table: set to table name
        ◦ see: https://support.airtable.com/hc/en-us/articles/360021333094#table
    • params_dict: desired parameters in dictionary format {parameter : value}
        ◦ example: {"maxRecords" : 20, "view" : "Grid view"}
        ◦ see "List Records" in API Documentation (airtable.com/api)
    • api_key: retrievable at https://airtable.com/account
        ◦ looks like "key●●●●●●●●●●●●●●"
    • base_id: retrievable at https://airtable.com/api for specific base
        ◦ looks like "app●●●●●●●●●●●●●●"
    • record_id: optional for single record lookups
        ◦ looks like "rec●●●●●●●●●●●●●●"
        """

    # Authorization Credentials
    if api_key is None:
        print("Enter Airtable API key. \n  *Find under Airtable Account Overview: https://airtable.com/account")
        api_key = input()
    headers = {"Authorization": "Bearer {}".format(api_key)}
    

    # Locate Base
    if base_id is None:
        print("Enter Airtable Base ID. \n  *Find under Airtable API Documentation: https://airtable.com/api for specific base")
        base_id = input()
    url = 'https://api.airtable.com/v0/{}/'.format(base_id)
    path = url + table
    print(path)


   

    # Start with blank list of records
    airtable_records = []

    
    # Retrieve multiple record
    run = True
    while run is True:
        response = requests.get(path, headers=headers)
        airtable_response = response.json()

        try:
            airtable_records += (airtable_response['records'][-5:])
        except:
            if 'error' in airtable_response:
                #identify_errors(airtable_response)
                return airtable_response

        if 'offset' in airtable_response:
            run = True
            params = (('offset', airtable_response['offset']))
        else:
            run = False

    # Retrieve single record
    if record_id is not None:
        path = "{}/{}".format(path, record_id)
        response = requests.get(path, headers=headers)
        airtable_response = response.json()
        if 'error' in airtable_response:
            #identify_errors(airtable_response)
            return airtable_response
        return airtable_response

    return airtable_response

data = airtable_download(table='Table%201', api_key='keyaBsw18laM26RJw', base_id='appYg9u6AyKu7LQV0')#, record_id='rectzaIuGBmxgQL6p')
#print(data['fields']['status'])
output = {}
generated_id= '0d88b007-8862-4ed7-8be2-b4830f6ced7e'
print(data)
for i in data:
    if generated_id ==i['fields']['id']:
        output= i['fields']
print(output['status'])