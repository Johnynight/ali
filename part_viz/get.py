import requests
import json
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


a = PartsViz(login='v363vc4', password='Vchurikov199707')
b = a.parser()

PV = []
part_number = None
facing_facility = None
replacement_part = None
entry_point = None
part_description = None
supplier_lead_time = None
discontinued = None
freezecode = None
Constrained_Part_Score = None
Search_Network = None
Reman_Part = None
Pkg_Qty = None


for part in files:
    cookies = b[1]

    data = {
        'message': update_part_number(d, part.strip()),
        'aura.context': '{"mode":"PROD","fwuid":"ZDROWDdLOGtXcTZqSWZiU19ZaDJFdzk4bkk0bVJhZGJCWE9mUC1IZXZRbmcyNDguMTAuNS01LjAuMTA","app":"siteforce:communityApp","loaded":{"APPLICATION@markup://siteforce:communityApp":"XvLrnsfis-Fl75QQFAqN9A","COMPONENT@markup://instrumentation:o11ySecondaryLoader":"nSN3-Xh18FbrdCVGqsWZnw","COMPONENT@markup://forceCommunity:dashboard":"Yhwk4JQdO86kGQa6VU8kZw","COMPONENT@markup://forceCommunity:embeddedServiceSidebar":"Aaa2U-qSumo-_DXbRovlWA","COMPONENT@markup://forceCommunity:objectHome":"grkThfos18gd4-W073O23Q","COMPONENT@markup://force:outputField":"EK6w4AVzGIfP2l203QXCzA"},"dn":[],"globals":{},"uad":false}',
        'aura.pageURI': '/PartsViz/s/supply-chain-visibility',
        'aura.token': b[0],
    }

    response = requests.post(
        'https://cat.my.site.com/PartsViz/s/sfsites/aura',

        cookies=cookies,

        data=data,
    )
    print(part.strip())
    for i in response.json()['actions']:
        if i['id'] == '932;a':
            part_number = i['returnValue'][0]['Name']
            # facing_facility = i['returnValue'][0]['Facing_Facility_Stocking_Ind__c']
            if i.get('returnValue', [{}])[0].get('Replacement_Part__c'):
                replacement_part = i.get('returnValue', [{}])[0].get('Replacement_Part__c')
            entry_point = i['returnValue'][0]['Entry_Point__c']
            part_description = i['returnValue'][0]['Part_Description__c']
            if i.get('returnValue', [{}])[0].get('Reman_Part__c'):
                Reman_Part = i['returnValue'][0]['Reman_Part__c']
            Pkg_Qty = i['returnValue'][0]['Pkg_Qty__c']

        if i['id'] == '928;a':
            supplier_lead_time = json.loads(i['returnValue'])['entryPointResult']['Supplier_Lead_Time__c']
            entry_point = json.loads(i['returnValue'])['entryPointResult']['Entry_Point__c']
            facing_facility = json.loads(i['returnValue'])['facingFacilityName']
            discontinued = json.loads(i['returnValue'])['entryPointResult']['Discontinued__c']
            Constrained_Part_Score = json.loads(i['returnValue'])['entryPointResult']['Constrained_Parts_Score__c']
        if i['id'] == '930;a':
            freezecode = i['returnValue']['FreezeCode']
        if i['id'] == '911;a':
            Search_Network = i['returnValue']['SearchNWAsList']

    PV.append({
        'part_number': part_number,
        'facing_facility': facing_facility,
        'replacement_part': replacement_part,
        'entry_point': entry_point,
        'part_description': part_description,
        'supplier_lead_time': supplier_lead_time,
        'discontinued': discontinued,
        'freezecode': freezecode,
        'Constrained_Part_Score_Desc': Constrained_Part_Score,
        'Reman_Part': Reman_Part,
        'Search_Network': Search_Network,
        'Pkg_Qty': Pkg_Qty

    })

    PV.append({
        'part_number': part_number,
        'facing_facility': facing_facility,
        'replacement_part': replacement_part,
        'entry_point': entry_point,
        'part_description': part_description,
        'supplier_lead_time': supplier_lead_time,
        'discontinued': discontinued,
        'freezecode': freezecode,
        'Constrained_Part_Score_Desc': Constrained_Part_Score,
        'Search_Network': Search_Network

    })

with open('my_data.json','w') as f:
    json.dump(PV, f)
