'''
Created on Jun 9, 2013

@author: Rafael Timmerberg(raffn1+linspector@gmail.com)
'''

from os.path import isfile
import json
from layouts import Layout
from hostgroups import HostGroup


class ConfigurationException(Exception):
    def __init__(self, msg, log):
        log.e(msg)
        self.msg = msg
        
    def __str__(self):
        return repr(self.msg)


KEY_LAYOUTS      = "layouts"
KEY_HOSTGROUPS   = "hostgroups"
KEY_MEMBERS      = "members"
KEY_PERIODS      = "periods"
KEY_CORE         = "core"


class ConfigParser:
    def __init__(self, log):
        '''
        initializes a new ConfigParser Object
        
        params: 
            log: pre configured logger Object to post messages while parsing"
        '''
        self.log = log
        self.hostgroups = {}
        self.members = {}
        self.periods = {}

    def _read_json_config(self, configFilename):
        '''
        reads the config File and returns a dictionary, while lowering the first keys
        
        params:
            configFilename: the path under which the configuration file should be found
        '''
        if not isfile(configFilename):
            msg = "config file not found at " + str(configFilename)
            raise ConfigurationException(msg, self.log)
        
        self.configfilename = configFilename
        
        with open(configFilename) as cfgFile:
            config = cfgFile.read()
        
        self.log.i("reading Config: " + configFilename)
        return json.loads(config)

    def _get_as_list(self, configValue):
        '''
        In some cases the config permits to define a list or a single value.
        
        returns the value as list
        '''
        return configValue if isinstance(configValue, list) else [configValue]

    def create_layouts_from_json(self, jsonLayouts):
        layouts = []
        for lName, lValues in jsonLayouts.items():
            try:
                layout = Layout(lName, **lValues)
                layouts.append(layout)
            except ConfigurationException:
                self.log.w("ignoring Layout " + lName + "! reason:")
                self.log.w(str(Exception))
        return layouts

    def create_hostgroups_from_json(self, jsonHostGroups):
        '''
        creates Hostgroups from the jsonConfig
        '''
        hostgroups = []
        for hgName, hgValues in jsonHostGroups.items():
            try:
                hostgroup = HostGroup(hgName, **hgValues)
                hostgroups.append(hostgroup)
            except ConfigurationException:
                self.log.w("ignoring hostgroup: " + hgName + "!")
                self.log.w("reason: " + str(Exception))
        return hostgroups

    def create_members_from_json(self, jsonMembers):
        '''
        creates Members from the jsonConfig
        '''
        members = []
        for memberName, memberValues in jsonMembers.items():
            try:
                member = memberName(memberName, **memberValues)
                members.append(member)
            except ConfigurationException:
                self.log.w("ignoring member: " + memberName + "!")
                self.log.w("reason: " + str(Exception))
        return members

    def parse_config(self, configFilename):
        '''
        parses the json configuration and returns a list of layouts, 
        which contains all nessesary information of the config file.
        Parsing will be done in 3 steps:
        1. get raw Config Objects by just passing the values defined inside the config
        2. replace references by objects
        3. do sanity checks
        
        params:
            configFilename: indicates which configuration file to parse
        '''
        
        self.jsonDict = self._read_json_config(configFilename)
        
        jsonLayouts = self.jsonDict[KEY_LAYOUTS]
        layouts = self.create_layouts_from_json(jsonLayouts)
        
        hostgroupNames = set()
        for layout in layouts:
            for hgName in layout.get_hostgroups():
                hostgroupNames.add(hgName)
                
        
        jsonHostgroups = {}
        for hgName in hostgroupNames:
            if not hgName in self.jsonDict[KEY_HOSTGROUPS]:
                self.log.w("Hostgroup " + hgName + " not found!")
                for layout in layouts:
                    if hgName in layout.hostgroups:
                        del layout.hostgroups[layout.hostgroups.index(hgName)]
            jsonHostgroups[hgName] = self.jsonDict[KEY_HOSTGROUPS][hgName]
        
        self.hostgroups = self.create_hostgroups_from_json(jsonHostgroups)
        
        memberNames = set()
        for layout in layouts:
            for memberName in layout.get_members():
                memberNames.add(memberName)

        jsonMembers = {}
        for memberName in memberNames:
            if not memberName in self.jsonDict[KEY_MEMBERS]:
                self.log.w("Member " + memberName + " not found!")
                for hostgroup in self.hostgroups:
                    if memberName in hostgroup.members:
                        del hostgroup.members[hostgroup.members.index(memberName)]
            jsonMembers[memberName] = self.jsonDict[KEY_HOSTGROUPS][memberName]
        
        self.members = self.create_members_from_json(jsonMembers)
        