'''This scripts try to connect to Xero without using any python wrapper
created by Muhit Anik <muhit@convertworx.com.au>
For xero reference use this guide: https://developer.xero.com/documentation/api

To access another endpoint for instance accessing Name which is found inside Contact, we must call it like Contact.Name
The following example demonstrates that. Keep in mind, we are doing percent encoding. So there exists difference between
'' (single quote) and "" (double quote).

The settings are inside config.cfg.
The sample response will be written in output.json
'''


import requests
from requests_oauthlib import OAuth1
import simplejson as json
from urllib2 import quote
import ConfigParser

def Xero(url, requestType="GET", body=""):
    config = ConfigParser.ConfigParser()    
    config.readfp(open('config.cfg'))

    consumer_key = config.get("xero_api", "consumer_key") ##consumer secret is NOT used for private companies.
    
    with open("privatekey.pem", "rb") as rsafile:
        rsakey = rsafile.read()

    ### consumer key is used both as consumer key and auth token.
    oauth = OAuth1(consumer_key, resource_owner_key=consumer_key, rsa_key=rsakey, signature_method='RSA-SHA1', signature_type='auth_header')

    if requestType == "POST":
        headers = {'Content-Type': 'application/json'}
        if body == "":
            print "Empty body. Nothing to post."
            exit()
        resp = requests.post(url=url, auth=oauth, headers=headers, data=body)


    if requestType == "PUT":
        headers = {'Content-Type': 'application/json'}
        if body == "":
            print "Empty body. Nothing to put."
            exit()
        resp = requests.put(url=url, auth=oauth, headers=headers, data=body)

    if requestType == "GET":
        ### this will allow the output in json
        headers = {'Accept': 'application/json'}
        resp = requests.get(url=url, auth=oauth, headers=headers)

    with open("output.json", "wb") as f:
        f.write(resp.text)

def filter_invoice_by_contact_name():
    ### API reference: https://developer.xero.com/documentation/api/invoices
    ### Example-1: Getting invoices where Contact Name is "B Catering Melbourne"
    base_url = "https://api.xero.com/api.xro/2.0/Invoices?where="
    filter_url = 'Contact.Name=="Q Catering Melbourne"'   ### value must be double quoted, single quoting will fail.
    url = base_url + quote(filter_url)
    Xero(url)

def filter_invoice_by_trackingCategory():
    ### API reference: https://developer.xero.com/documentation/api/tracking-categories#Options
    ### Example-2: Using trackingCategories end point and filtering by category name
    base_url = "https://api.xero.com/api.xro/2.0/TrackingCategories?where="
    filter_url = 'Name=="Region"'
    url = base_url + quote(filter_url)
    Xero(url)


def startswith_contains_endswith():
    ### API reference: https://developer.xero.com/documentation/api/requests-and-responses#get-modified
    ### Example-3 usage of Name.Contains 
    base_url = "https://api.xero.com/api.xro/2.0/Invoices?where="
    filter_url = 'Contact.Name.StartsWith("B")' 
    ### similarly we can use Contact.Name.Contains("B") and Contact.Name.EndsWith("B") etc
    url = base_url + quote(filter_url)
    Xero(url)


def journals_by_sourceType():
    ### API reference: https://developer.xero.com/documentation/api/journals
    ### Example-4 getting a journal by using the sourceType attribute
    base_url = "https://api.xero.com/api.xro/2.0/Journals?where="
    filter_url = 'SourceType=="ACCREC"'
    url = base_url + quote(filter_url)

    Xero(url)

def new_invoice():
    ### API reference: https://developer.xero.com/documentation/api/invoices#post
    ### Example-5 demonstrates how to make post/put requests to Xero.
    url = "https://api.xero.com/api.xro/2.0/Invoices"
    body = {
                "Type" : "ACCREC",
                "Contact" : {"Name": "TESTABCD"},
                "LineItems" : [{"Description" : "TEST Item 1", "Quantity" : 5, "UnitAmount" : 30}]
            }
    body = json.dumps(body, encoding="utf-8")
    Xero(url, "POST", body)