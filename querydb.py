# -*- coding: utf-8 -*-
#import pyArango
from pyArango.connection import *
import json
import sys

class querydb:
    def __init__(self):
        self.conn = Connection(arangoURL='http://cudaws02.ime.kfa-juelich.de:8529', username="haimasree", password="haimasree123")
        self.db = self.conn["Metadata"]
        self.rois = self.db["rois"]
        with open('files/filteredJuBrainJson.json') as file:
            self.metadata = json.load(file)
        self.idpmapdict = {}        
        self.createidpmap(self.metadata[0])

    def createidpmap(self, d):
        if isinstance(d, dict):
            if 'PMapURL' in d:
                if 'ontologyMetadata' in d and '_Id' in d['ontologyMetadata']:
                    self.idpmapdict[d['ontologyMetadata']['_Id']] = d['PMapURL']
                else:
                    self.idpmapdict[d['name']] = d['PMapURL']
                self.createidpmap(d['children'])
            if 'PMapURL' not in d:
                self.createidpmap(d['children'])
        elif isinstance(d, list):
            for k in d:
                self.createidpmap(k)
        else:
            print(type(d),' is not supported ')
            exit()

    def getidfromname(self, name):
        for item in self.rois.fetchAll():
            if item['Display name'] == name:
                return item['_Id']
        print('Roi name not found in the database')
        return

    '''
    def getpmap(self, id):
        for item in self.rois.fetchAll():
            if item['_Id'] is id:
                print(item['PmapURL']) #Ideally this should return the pmaps once they are part of the database
    '''

    def getpmapurlfromid(self, id):
        if id in self.idpmapdict:
            return self.idpmapdict[id]
        else:
            print('Not a valid id')
        return

    def printrois(self):
        if sys.version_info[0] < 3:
            for key, values in self.idpmapdict.iteritems():
                print(key,' values = ',values)
        else:
            for key, values in self.idpmapdict.items():
                print(key,' values = ',values)


