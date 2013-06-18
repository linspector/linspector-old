from os.path import isfile
import json
import sys

from layouts import Layout
from hostgroups import HostGroup
from members import Member
from periods import CronPeriod, DatePeriod, IntervalPeriod

from lib.services.service import Service
from lib.processors.processor import Processor
from lib.parsers.parser import Parser
from lib.tasks.task import  Task

MOD_SERVICES     = "services"
MOD_PROCESSORS   = "processors"
MOD_PARSERS      = "parsers"
MOD_TASKS        = "tasks"

sys.path.append("lib/" + MOD_SERVICES)
sys.path.append("lib/" + MOD_PROCESSORS)
sys.path.append("lib/" + MOD_PARSERS)
sys.path.append("lib/" + MOD_TASKS)

KEY_LAYOUTS      = "layouts"
KEY_HOSTGROUPS   = "hostgroups"
KEY_MEMBERS      = "members"
KEY_PERIODS      = "periods"
KEY_CORE         = "core"

class ConfigurationException(Exception):
    def __init__(self, msg, log):
        log.e(msg)
        self.msg = msg
        
    def __str__(self):
        return repr(self.msg)


class ConfigParser:
    def __init__(self, log):
        """
        initializes a new ConfigParser Object
        
        params: 
            log: pre configured logger Object to post messages while parsing"
        """
        self.log = log
        self.hostgroups = {}
        self.members = {}
        self.periods = {}
        self.layouts = {}
        self._loadedMods={MOD_SERVICES:{}, MOD_PROCESSORS:{}, MOD_TASKS:{}}
        
    def _create_new_config_dict(self):
        return  {"members": {}, "periods":{}, "hostgroups":{}, "layouts":{}, "core":{}}
        
    def create_config(self, config):
        configDict = self._create_new_config_dict()
        for layout in config.get_layouts():
            layout._to_config_dict(configDict)

    def _read_json_config(self, configFilename):
        """
        reads the config File and returns a dictionary, while lowering the first keys
        
        params:
            configFilename: the path under which the configuration file should be found
        """
        if not isfile(configFilename):
            msg = "config file not found at " + str(configFilename)
            raise ConfigurationException(msg, self.log)
        
        self.configfilename = configFilename
        
        with open(configFilename) as cfgFile:
            config = cfgFile.read()
        
        self.log.i("reading Config: " + configFilename)
        return json.loads(config)

    def _get_as_list(self, configValue):
        """
        In some cases the config permits to define a list or a single value.
        
        returns the value as list
        """
        return configValue if isinstance(configValue, list) else [configValue]
    
    def _create_raw_Object(self, jsonDict, msgName, creator):
        items = []
        for key, val in jsonDict.items():
            try:
                item = creator(key, val)
                items.append(item)
            except Exception:
                self.log.w("ignoring " + msgName + ": " + key + "! reason:")
                self.log.w(str(Exception))
        return items
    
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
        """
        creates Hostgroups from the jsonConfig
        """
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
        """
        creates Members from the jsonConfig
        """
        members = []
        for memberName, memberValues in jsonMembers.items():
            try:
                member = memberName(memberName, **memberValues)
                members.append(member)
            except ConfigurationException:
                self.log.w("ignoring member: " + memberName + "!")
                self.log.w("reason: " + str(Exception))
        return members
    
    def _load_module(self, clazz, modPart):
        mods = self._loadedMods[modPart]
        if clazz in mods:
            return mods["class"]
        else:
            mod = __import__(clazz)
            mods[clazz] = mod
            return mod
    
    def replace_with_import(self, objList, modPart, items_func, class_check):
        for obj in objList:
            repl = []
            items = items_func(obj)
            for clazzItem in items:
                try:
                    clazz = clazzItem["class"]
                    mod = self._load_module(clazz, modPart)
                    item = mod.create(**clazzItem)
                    if class_check(item):
                        repl.append(item)
                    else:
                        self.log.w(" ignoring class " + clazzItem["class"] + "! It does not pass the class check!")
                except ImportError, err:
                    self.log.w("could not import " + clazz + ": " + str(clazzItem) + "! reason")
                    self.log.w(str(err))
                except KeyError:
                    self.log.w("Key 'class' not in classItem " + str(clazzItem))
                except Exception:
                    self.log.w("Error while replace: " + str(Exception))
            del items[:]
            items.extend(repl)

    def replace_pointer(self, objectList, replObjectList, id_list_func, id_get_func):
        for obj in objectList:
            replacements = []
            idList = id_list_func(obj)
            for id in idList:
                repl = [o for o in replObjectList if  id == id_get_func(o)]
                if len(repl) == 1:
                    replacements.append(repl[0])

            del idList[:]
            idList.extend(replacements)

    def parse_config(self, configFilename):
        """
        parses the json configuration and returns a list of layouts, 
        which contains all nessesary information of the config file.
        It will only parse nessesary Objects.
        Parsing will be done in 3 steps:
        1. get raw Config Objects by just passing the values defined inside the config
        2. replace references by objects
        3. do sanity checks
        
        params:
            configFilename: indicates which configuration file to parse
        """
        
        self.jsonDict = self._read_json_config(configFilename)
        
        jsonLayouts = self.jsonDict[KEY_LAYOUTS]
        #layouts = self._create_raw_Object(jsonLayouts, "Layouts", lambda name, vals: Layout(name, **vals))
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


def parsePeriodList(name, values):
    if "date" in values:
        return DatePeriod(name, **values)
        
    comp = ["weeks", "days", "hours", "minutes", "seconds", "start_date"]
    if len([i for i in comp if i in values]) > 0 :
        return IntervalPeriod(name, **values)
            
    comp = ["year", "month", "day", "week", "day_of_week", "hour", "minute", "second"]
    if len([i for i in comp if i in values]) > 0 :
        return CronPeriod(name, **values)
    else:
        raise ConfigurationException("could not determine correct Period(" + repr(values)+").")


class FullConfigParser(ConfigParser):
    def parse_config(self, configFilename):
        """
        parses the json configuration and returns a list of layouts, 
        which contains all nessesary information of the config file.
        parses the full config
        Parsing will be done in 3 steps:
        1. get raw Config Objects by just passing the values defined inside the config
        2. replace references by objects, import services, tasks, parsers and processors
        3. do sanity checks
        
        params:
            configFilename: indicates which configuration file to parse
        """
        self.jsonDict = self._read_json_config(configFilename)
        
        # first step
        creator = lambda name, values: Layout(name,**values)
        layouts = self._create_raw_Object(self.jsonDict[KEY_LAYOUTS], "Layout", creator)
        
        creator = lambda name, values: Member(name, **values)
        members = self._create_raw_Object(self.jsonDict[KEY_MEMBERS], "Member", creator)
        
        creator = lambda name, values: HostGroup(name, **values)
        hostgroups = self._create_raw_Object(self.jsonDict[KEY_HOSTGROUPS], "Hostgroup", creator)
        
        creator = parsePeriodList
        periods = self._create_raw_Object(self.jsonDict[KEY_PERIODS], "Period", creator)
        
        #2. import and replace
        items_func = lambda hostgroup: hostgroup.get_services()
        class_check = lambda service: isinstance(service, Service)
        self.replace_with_import(hostgroups, MOD_SERVICES, items_func, class_check)
        
        items_func = lambda hostgroup: hostgroup.get_processors()
        class_check = lambda processor: isinstance(processor, Processor)
        self.replace_with_import(hostgroups, MOD_PROCESSORS, items_func, class_check)
        
        items_func = lambda service: service.get_parser()
        class_check = lambda parser: isinstance(parser, Parser)
        self.replace_with_import(hostgroups.services, MOD_PARSERS, items_func, class_check)
        
        items_func = lambda member: member.get_tasks()
        class_check = lambda task: isinstance(task, Task)
        self.replace_with_import(members, MOD_TASKS, items_func, class_check)

        #replace object pointer
        id_list_func = lambda hostgroup: hostgroup.get_members()
        id_get_func = lambda member: member.id
        self.replace_pointer(hostgroups, members, id_list_func, id_get_func)

        services = []
        for hg in hostgroups:
            services.extend(hg.get_services())
        id_list_func = lambda  service: service.get_periods()
        id_get_func = lambda period: period.get_name()
        self.replace_pointer(services, periods, id_list_func, id_get_func)

        id_list_func = lambda layout: layout.get_hostgroups()
        id_get_func = lambda  hostgroup: hostgroup.get_name()
        self.replace_pointer(layouts, hostgroups, id_list_func, id_get_func)

        return layouts