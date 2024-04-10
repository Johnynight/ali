import requests
import json
import pprint
from sel import PartsViz

d = ('{"actions":[{"id":"911;a","descriptor":"apex://SCVFormApexController/ACTION$networkAvail",'
     '"callingDescriptor":"markup://c:SCVNetworkAvailability","params":{"custCode":"v364","partNumber":"8E2882",'
     '"orderType":"E"},"version":null},{"id":"912;a",'
     '"descriptor":"apex://SCVFormApexController/ACTION$getSupplierPendSchSearch",'
     '"callingDescriptor":"markup://c:SCVNetworkAvailability","params":{"custCode":"v364","partNumber":"8E2882",'
     '"orderType":"E"},"version":null},{"id":"913;a",'
     '"descriptor":"apex://SCVFormApexController/ACTION$getSupplierFirmSchSearch",'
     '"callingDescriptor":"markup://c:SCVNetworkAvailability","params":{"custCode":"v364","partNumber":"8E2882",'
     '"orderType":"E"},"version":null},{"id":"914;a",'
     '"descriptor":"apex://SCVFormApexController/ACTION$getManufacturingData",'
     '"callingDescriptor":"markup://c:SCVNetworkAvailability","params":{"custCode":"v364","partNumber":"8E2882"},'
     '"version":null},{"id":"910;a","descriptor":"apex://SCVFormApexController/ACTION$getRODData",'
     '"callingDescriptor":"markup://c:SCVNetworkAvailability","params":{"custCode":"v364","partNumber":"8E2882"},'
     '"version":null},{"id":"924;a","descriptor":"apex://SCVFormApexController/ACTION$getCurrentTime",'
     '"callingDescriptor":"markup://c:PartsAttributeComponent","params":{},"version":null},{"id":"925;a",'
     '"descriptor":"apex://SCVFormApexController/ACTION$checkUserDetails",'
     '"callingDescriptor":"markup://c:PartsAttributeComponent","params":{},"version":null},{"id":"927;a",'
     '"descriptor":"apex://SCVFormApexController/ACTION$checkURL",'
     '"callingDescriptor":"markup://c:PartsAttributeComponent","params":{},"version":null},{"id":"932;a",'
     '"descriptor":"apex://SCVFormApexController/ACTION$getPartMasterData",'
     '"callingDescriptor":"markup://c:PartsAttributeComponent","params":{"custCode":"v364","partNumber":"8E2882",'
     '"orderType":"E"},"version":null},{"id":"929;a",'
     '"descriptor":"apex://SCVFormApexController/ACTION$getApprovalRule",'
     '"callingDescriptor":"markup://c:PartsAttributeComponent","params":{"custCode":"v364","partNumber":"8E2882",'
     '"orderType":"E"},"version":null},{"id":"931;a",'
     '"descriptor":"apex://SCVFormApexController/ACTION$getExpandedStock",'
     '"callingDescriptor":"markup://c:PartsAttributeComponent","params":{"custCode":"v364","partNumber":"8E2882",'
     '"orderType":"E"},"version":null},{"id":"930;a","descriptor":"apex://SCVFormApexController/ACTION$getFreeze",'
     '"callingDescriptor":"markup://c:PartsAttributeComponent","params":{"custCode":"v364","partNumber":"8E2882",'
     '"orderType":"E"},"version":null},{"id":"928;a",'
     '"descriptor":"apex://SCVFormApexController/ACTION$getEntryPoint",'
     '"callingDescriptor":"markup://c:PartsAttributeComponent","params":{"custCode":"v364","partNumber":"8E2882",'
     '"orderType":"E"},"version":null}]}')

with open('parts.txt', 'r', encoding='utf-8') as f:
    files = f.readlines()


def update_part_number(data, new_part_number):
    data_dict = json.loads(data)

    for action in data_dict['actions']:
        if 'partNumber' in action['params']:
            action['params']['partNumber'] = new_part_number

    updated_data = json.dumps(data_dict, indent=4)
    return updated_data


# a = PartsViz(login='v363vc4', password='Vchurikov199707')
# b = a.parser()
# cookies = b[1]

# data = {
#     'message': update_part_number(d,'5M3320'),
#     'aura.context': '{"mode":"PROD","fwuid":"ZDROWDdLOGtXcTZqSWZiU19ZaDJFdzk4bkk0bVJhZGJCWE9mUC1IZXZRbmcyNDguMTAuNS01LjAuMTA","app":"siteforce:communityApp","loaded":{"APPLICATION@markup://siteforce:communityApp":"XvLrnsfis-Fl75QQFAqN9A","COMPONENT@markup://instrumentation:o11ySecondaryLoader":"nSN3-Xh18FbrdCVGqsWZnw","COMPONENT@markup://forceCommunity:dashboard":"Yhwk4JQdO86kGQa6VU8kZw","COMPONENT@markup://forceCommunity:embeddedServiceSidebar":"Aaa2U-qSumo-_DXbRovlWA","COMPONENT@markup://forceCommunity:objectHome":"grkThfos18gd4-W073O23Q","COMPONENT@markup://force:outputField":"EK6w4AVzGIfP2l203QXCzA"},"dn":[],"globals":{},"uad":false}',
#     'aura.pageURI': '/PartsViz/s/supply-chain-visibility',
#     'aura.token': b[0],
# }

# response = requests.post(
#     'https://cat.my.site.com/PartsViz/s/sfsites/aura',

#     cookies=cookies,

#     data=data,
# )

# print(
#     response.json()
# )

for i in files:
    print(i)