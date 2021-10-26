import jwt
import requests
#from bs4 import BeautifulSoup
import json
from json import dumps
import asyncio
SUCCESS      = 200
CLIENT_ERROR = 400
SERVER_ERROR = 500
compress_level = 9
minimum_size = 1000
count = 1

from flask import Flask, jsonify, request,make_response,Response
application = Flask(__name__)

@application.route("/",defaults={'path':''})

@application.route("/<path:path>",methods = ['GET'])
def hello(path):

    #print("path is --",path)
    print(request.headers)
    #print("Header Val --",type(request.headers))
    val=request.headers.get('x-amzn-oidc-data') #get the encoded token
    #print("token val is ",val)
    if not val:
        return "<p><h1>Illegal Access, You are Not Authorized</h1></p>"
    decodeval=jwt.decode(val,"secret",options={"verify_signature":False}) #command to decode
    print("Accept ----",request.headers.get("Accept"))
    header = dict(request.headers)
    with open('/home/ec2-user/newheader.txt', 'w') as f:
        f.write(json.dumps(header))
    if 'custom:GROUP_MEMBER' in decodeval:
        header['jwt-token'] = header.pop("X-Amzn-Oidc-Data")
        header['jwt-accesstoken'] = header.pop("X-Amzn-Oidc-Accesstoken")
        header['jwt-identity'] = header.pop("X-Amzn-Oidc-Identity")
        customgrp=decodeval['custom:GROUP_MEMBER']
        #Group_list = list(map(str.strip,customgrp[1:len(customgrp)-1].split(",")))
        grp = customgrp.replace("[","").replace("]","").split(",")
        group_list = list(map(str.strip, grp))
        if "APP_BIOINFO_DATA_HUB" in group_list:
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop=asyncio.get_event_loop()
            result=loop.run_until_complete(processRequest(path,header))
            return result
            '''url = "http://internal-bioinformatics-dev-alb-backend-270089063.us-west-2.elb.amazonaws.com/"+path
            request_get = requests.get(url,stream=True)
            acceptval=request.headers.get("Accept")
            if "Content-Type" in request_get.headers and 'image' in request_get.headers['Content-Type']:
                print("Image Headers --",request_get.headers)
                response=make_response(request_get.content)
                #if ".png" in path:
                #    response.headers.set('Content-Type','image/png')
                #elif ".jpg" in path:
                #    response.headers.set('Content-Type','image/jpeg')
                response.headers.set('Content-Type',request_get.headers['Content-Type'])
                return response #base64.b64encode(request_get.content).decode('utf-8')
            else:
                return request_get.text'''
        else:
            return "<p><h1>You are Not Part of APP_BIOINFO_DATA_HUB Group Contact John Austin</h1></p>"
    else:
        #request_get = requests.get(url,stream=True)
        return "<p><h1>You are Not Authorized, please contact John Austin</h1></p>"

async def processRequest(path,header):
    url = "http://internal-bioinformatics-dev-alb-backend-270089063.us-west-2.elb.amazonaws.com/"+path
    with open('/home/ec2-user/afterheader.txt', 'w') as fi:
        fi.write(json.dumps(header))
    request_get = requests.get(url,headers=header,stream=True)
    #acceptval=request.headers.get("Accept")
    if "Content-Type" in request_get.headers and 'image' in request_get.headers['Content-Type']:
        #if "image" in acceptval:
        #print("Image Headers --",request_get.headers)
        response=make_response(request_get.content)
        response.headers.set('Content-Type',request_get.headers['Content-Type'])
        return response
    else:
        response=make_response(request_get.content)
        response.headers.set('Content-Type',request_get.headers['Content-Type'])
        return response

#@app.route("/",defaults={'path':''})

@application.route("/<path:path>",methods = ['POST'])
def hello_post(path):
    #print("path is --",path)
    #print(request.headers)
    print("Header Val --",len(request.headers))
    val=request.headers.get('x-amzn-oidc-data') #get the encoded token
    print("token val is ",val)
    if not val:
        return "<p><h1>Illegal Access, You are Not Authorized</h1></p>"
    decodeval=jwt.decode(val,"secret",options={"verify_signature":False}) #command to decode
    print("Accept ----",request.headers.get("Accept"))
    if 'custom:GROUP_MEMBER' in decodeval:
        customgrp=decodeval['custom:GROUP_MEMBER']
        header = dict(request.headers)
        header['jwt-token'] = header.pop("X-Amzn-Oidc-Data")
        header['jwt-accesstoken'] = header.pop("X-Amzn-Oidc-Accesstoken")
        header['jwt-identity'] = header.pop("X-Amzn-Oidc-Identity")
        grp = customgrp.replace("[","").replace("]","").split(",")
        group_list = list(map(str.strip, grp))
        if "APP_BIOINFO_DATA_HUB" in group_list:
            url = "http://internal-bioinformatics-dev-alb-backend-270089063.us-west-2.elb.amazonaws.com/"+path
            request_post = requests.post(url,headers=header)
            return request_post
        else:
            return "<p><h1>You are Not Part of APP_BIOINFO_DATA_HUB Group Contact John Austin</h1></p>"
    else:
        return "<p><h1>You are Not Authorized, please contact John Austin</h1></p>"

@application.route("/<path:path>",methods = ['PUT'])
def hello_put(path):
    val=request.headers.get('x-amzn-oidc-data') #get the encoded token
    print("token val is ",val)
    if not val:
        return "<p><h1>Illegal Access, You are Not Authorized</h1></p>"
    decodeval=jwt.decode(val,"secret",options={"verify_signature":False}) #command to decode
    print("Accept ----",request.headers.get("Accept"))
    if 'custom:GROUP_MEMBER' in decodeval:
        customgrp=decodeval['custom:GROUP_MEMBER']
        header = dict(request.headers)
        header['jwt-token'] = header.pop("X-Amzn-Oidc-Data")
        header['jwt-accesstoken'] = header.pop("X-Amzn-Oidc-Accesstoken")
        header['jwt-identity'] = header.pop("X-Amzn-Oidc-Identity")
        grp = customgrp.replace("[","").replace("]","").split(",")
        group_list = list(map(str.strip, grp))                                                                          
        if "APP_BIOINFO_DATA_HUB" in group_list:
            url = "http://internal-bioinformatics-dev-alb-backend-270089063.us-west-2.elb.amazonaws.com/"+path
            request_put = requests.put(url,headers=header)
            return request_put
        else:
            return "<p><h1>You are Not Part of APP_BIOINFO_DATA_HUB Group Contact John Austin</h1></p>"
    else:
        return "<p><h1>You are Not Authorized, please contact John Austin</h1></p>"
@app.route("/<path:path>",methods = ['DELETE'])
def hello_delete(path):
    val=request.headers.get('x-amzn-oidc-data') #get the encoded token
    print("token val is ",val)
    if not val:
         return "<p><h1>Illegal Access, You are Not Authorized</h1></p>"
    decodeval=jwt.decode(val,"secret",options={"verify_signature":False}) #command to decode
    print("Accept ----",request.headers.get("Accept"))
    if 'custom:GROUP_MEMBER' in decodeval:
        customgrp=decodeval['custom:GROUP_MEMBER']
        header = dict(request.headers)
        header['jwt-token'] = header.pop("X-Amzn-Oidc-Data")
        header['jwt-accesstoken'] = header.pop("X-Amzn-Oidc-Accesstoken")
        header['jwt-identity'] = header.pop("X-Amzn-Oidc-Identity")
        grp = customgrp.replace("[","").replace("]","").split(",")
        group_list = list(map(str.strip, grp))                                                                          
        if "APP_BIOINFO_DATA_HUB" in group_list:
            url = "http://internal-bioinformatics-dev-alb-backend-270089063.us-west-2.elb.amazonaws.com/"+path
            request_delete = requests.delete(url,headers=header)
            return request_delete
        else:
            return "<p><h1>You are Not Part of APP_BIOINFO_DATA_HUB Group Contact John Austin</h1></p>"
    else:
        return "<p><h1>You are Not Authorized, please contact John Austin</h1></p>"
@application.route("/<path:path>",methods = ['OPTIONS'])                                                                        
def hello_option(path):                                                                                                 
    val=request.headers.get('x-amzn-oidc-data') #get the encoded token
    print("token val is ",val)                                                                                          
    if not val:                                                                                                         
        return "<p><h1>Illegal Access, You are Not Authorized</h1></p>"
    decodeval=jwt.decode(val,"secret",options={"verify_signature":False})
    print("Accept ----",request.headers.get("Accept"))
    if 'custom:GROUP_MEMBER' in decodeval:

        customgrp=decodeval['custom:GROUP_MEMBER']
        header = dict(request.headers)
        header['jwt-token'] = header.pop("X-Amzn-Oidc-Data")
        header['jwt-accesstoken'] = header.pop("X-Amzn-Oidc-Accesstoken")
        header['jwt-identity'] = header.pop("X-Amzn-Oidc-Identity")
        grp = customgrp.replace("[","").replace("]","").split(",")
        group_list = list(map(str.strip, grp))                                                                          
        if "APP_BIOINFO_DATA_HUB" in group_list:
            url = "http://internal-bioinformatics-dev-alb-backend-270089063.us-west-2.elb.amazonaws.com/"+path
            request_options = requests.options(url,headers=header)
            return request_options
        else:
            return "<p><h1>You are Not Part of APP_BIOINFO_DATA_HUB Group Contact John Austin</h1></p>"
    else:
        return "<p><h1>You are Not Authorized, please contact John Austin</h1></p>"
@application.route("/<path:path>",methods = ['PATCH'])#called for patch method
def hello_patch(path):
    print("Header Val --",len(request.headers))
    val=request.headers.get('x-amzn-oidc-data') #get the encoded token
    print("token val is ",val)
    if not val:
        return "<p><h1>Illegal Access, You are Not Authorized</h1></p>"
    decodeval=jwt.decode(val,"secret",options={"verify_signature":False}) #command to decode
    print("Accept ----",request.headers.get("Accept"))
    if 'custom:GROUP_MEMBER' in decodeval:#check if the custom:GROUP_MEMBER is in the decoded value
        customgrp=decodeval['custom:GROUP_MEMBER']
        header = dict(request.headers)
        header['jwt-token'] = header.pop("X-Amzn-Oidc-Data")
        header['jwt-accesstoken'] = header.pop("X-Amzn-Oidc-Accesstoken")
        header['jwt-identity'] = header.pop("X-Amzn-Oidc-Identity")
        group_list = list(map(str.strip,customgrp[1:len(customgrp)-1].split(",")))
        if "APP_BIOINFO_DATA_HUB" in group_list:#check if APP_BIOINFO_DATA_HUB in the group list
            url = "http://internal-bioinformatics-dev-alb-backend-270089063.us-west-2.elb.amazonaws.com/"+path
            request_patch = requests.patch(url,headers=header)
            return request_patch#response for patch method
        else:# Response if APP_BIOINFO_DATA_HUB not in group list
            return "<p><h1>You are Not Part of APP_BIOINFO_DATA_HUB Group Contact John Austin</h1></p>"
    else:# Response if the custom:GROUP_MEMBER is not in the decoded value
            return "<p><h1>You are Not Authorized, please contact John Austin</h1></p>"


if __name__ == '__main__':
    application.run(host='0.0.0.0')
