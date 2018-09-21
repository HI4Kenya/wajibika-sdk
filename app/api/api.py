import json
import requests
from . import BASE_URL, session

"""
- Handle endpoint to analytics url
"""
def analytics_api(payload={}):
   """
   Common parameters to this endpoint
   :
   :param dimension
   ::: dx -- (program,indicator)
   ::: ou -- (organisation unit)
   ::: pe -- (period)
   :param filter
   ::: dx -- (program,indicator)
   ::: ou -- (organisation unit)
   :param columns
   :param rows
   :param skipMeta {bool}
   """
   # endpoint
   path = "/analytics"

   # check if there is a value on payload AND ou,dx,pe
   if not payload.get("dx") or not payload.get("ou") or not payload.get("pe"):
      return json.dumps({"404": "Cant have null parameters"})

   ou = payload["ou"].split(",")
   dx = payload["dx"].split(",")

   params = {
      "dimension": [ "dx:"+';'.join(dx), "pe:"+payload["pe"] ],
      "filter": ["ou:"+';'.join(ou)],
      "skipMeta": "true",
      "displayProperty": "NAME"
   }

   url = BASE_URL + path

   session.params = params
   response = session.get(url)

   rows = response.json()["rows"]

   """
   = Data dict
   = Format 
   = {
   =     "dx_id_1": [<values>],
   =     ...
   =     "dx_id_n": [<values>]
   = }
   """
   data = {}
   for dx_id in dx:
      data[dx_id] = []

      for key, value in enumerate(rows):
         if dx_id == value[0]:
            data[dx_id].append(value[2])
   
   return data


"""
- Handle endpoint to indicators url
"""
def indicators_api(payload={}):
   """
   Common paramters to this endpoint
   :
   :param paging {bool}
   :param fields {list}
   :param query
   """
   # /indicatorGroups

   path = "/indicatorGroups" if payload.get("kind") == "group" else "/indicators"

   params = {
      "paging": "false",
      "fields": ["id", "name", "code"]
   }

   id = payload.get("members")
   if id:
      return indicator_members(id)

   url = BASE_URL + path

   session.params = params
   response = session.get(url)

   # slice the path var to return
   # matching response always 
   return response.json()[path[1:]]


"""
- Handle endpoint to organisationUnits url
"""
def organisationUnits_api(payload={}):
   """
   Common parameters to this endpoint
   :
   :param paging {bool}
   :param fields {list}
   :param level {int}
   :param query
   """

   path = "/organisationUnits"

   params = {
      "level": 2 if not payload.get("level") else payload["level"],
      "paging": "false",
      "fields": ["id", "name", "code"]
   }

   url = BASE_URL + path

   session.params = params
   response = session.get(url)

   return response.json()[path[1:]]

def indicator_members(group_id):
   # returns list of dicts with ids only
   def get_ids(group_id):

      path = "/indicatorGroups/"+group_id
      url = BASE_URL + path

      res = requests.get(url, auth=session.auth)
      return res.json()["indicators"]
      

   all_members_id = get_ids(group_id)

   members_list = []
   params = {
      "fields": ["id", "name"]
   }
   session.params = params
   path = "/indicators/"

   # # loop through list of dicts
   for key, val in enumerate(all_members_id):

      url = BASE_URL + path + val["id"]
      res = session.get(url)

      members_list.append(res.json())

   return members_list


def parseData(payload={}):
   pass

def gis_api(payload={}):
   """
   Common parameters to this endpoint
   :
   :param dimension
   ::: dx -- (program,indicator)
   ::: ou -- (organisation unit)
   ::: pe -- (period)
   :param filter
   ::: dx -- (program,indicator)
   ::: ou -- (organisation unit)
   :param columns
   :param rows
   :param skipMeta {bool}
   """
   # endpoint
   path = "/analytics"

   # check if there is a value on payload AND ou,dx,pe
   if not payload.get("dx") or not payload.get("ou") or not payload.get("pe"):
      return json.dumps({"404": "Cant have null parameters"})

   ou = payload["ou"].split(",")
   dx = payload["dx"].split(",")

   params = {
      "dimension": ["ou:"+';'.join(ou),  "pe:"+payload["pe"] ],
      "filter": ["dx:"+';'.join(dx)],
      "skipMeta": "true",
      "displayProperty": "NAME"
   }

   url = BASE_URL + path

   session.params = params
   response = session.get(url)

   rows = response.json()["rows"]

   return rows


def poly_units_geojson(level=2):
   path = "/organisationUnits.geojson"

   params = {
      'level': level
   }

   url = BASE_URL + path

   session.params = params

   response = session.get(url)
   return response.json()


def analytics_data(analitic_data, level):
   
   
   def get_org_name(id_key):
      for k, v in enumerate(organisationUnits_api({})):
         if k == id_key:
            return v

   columns = {
      "records" : []
   }

   orgs = []

   for i in range(len(analitic_data)):
      dat = {}
      org = analitic_data[i][0]
      orgs.append(org)
      pe = analitic_data[i][1]
      val = analitic_data[i][2]
      dat['Organisation Unit'] = org
      dat['pe'] = pe
      dat['val'] = float(val)
      columns['records'].append(dat)

   unique_orgs = set(orgs)
	
   def get_geojson_pk():
      x = poly_units_geojson(level)

   collection = {}

   for org in unique_orgs:
      collection[org] = [{"period" : [], "value" : [], "name" : '', "average" : ''}]

   geojson = poly_units_geojson()
	
   for x in unique_orgs:
      for n in columns["records"]:
         org = n["Organisation Unit"]
         if x==org:
            org_name = get_org_name(x)
            collection[x][0]["period"].append(n['pe'])
            collection[x][0]["value"].append(n['val'])
            collection[x][0]["name"] = org_name
            tot = sum(collection[x][0]["value"])
            av = tot / len(collection[x][0]["period"])
            collection[x][0]["average"] = av

            for i in range(len(geojson["features"])):
               feat = geojson["features"][i]
               id = feat["id"]
               if x == id:
                  total = sum(collection[x][0]["value"])
                  av = total / len(collection[x][0]["period"])
                  feat["properties"]['average'] = av

   collection["geojson"] = geojson
   return collection
