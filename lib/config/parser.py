from os.path import isfile
from os.path import join
from os import getcwd
import json
import sys
import imp
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
        
        :param log: pre configured logger Object to post messages while parsing"
        """
        self.log = log
        self.hostgroups = {}
        self.members = {}
        self.periods = {}
        self.layouts = {}
        self._loadedMods = {MOD_SERVICES: {}, MOD_PROCESSORS: {}, MOD_TASKS: {}, MOD_PARSERS: {}}
        
    def _create_new_config_dict(self):
        return {"members": {}, "periods": {}, "hostgroups": {}, "layouts": {}, "core": {}}
        
    def create_config(self, config):
        configDict = self._create_new_config_dict()
        for layout in config.get_layouts():
            layout._to_config_dict(configDict)

    def _read_json_config(self, configFilename):
        """
        reads the config File and returns a dictionary, while lowering the first keys
        
        :param configFilename: the path under which the configuration file should be found
        """
        if not isfile(configFilename):
            msg = "config file not found at " + str(configFilename)
            raise ConfigurationException(msg, self.log)
        
        self.configFilename = configFilename
        
        with open(configFilename) as cfgFile:
            config = cfgFile.read()
        
        self.log.i("reading Config: " + configFilename)
        return json.loads(config)

    def _create_raw_Object(self, jsonDict, msgName, creator):
        """
        creates an Main object from the configuration, but just parses raw data and hands it to the object

        :param jsonDict: the configuration file part as dict
        :param msgName: name of object for error message
        :param creator: function pointer which is taking two arguments: identifier of the object and arguments.
        :should return an object
        :return: a list of objects returned by creator
        """
        items = []
        for key, val in jsonDict.items():
            try:
                item = creator(key, val)
                items.append(item)
            except Exception:
                self.log.w("ignoring " + msgName + ": " + key + "! reason:")
                self.log.w(str(Exception))
        return items

    def _load_module(self, clazz, modPart):
        """
        imports and caches a module.

        :param clazz: the filename of the module (i.e email, ping...)
        :param modPart: the folder of the module. (i.e services, parsers...)
        :return: the imported/cached module, or throws an error if it couldn't find it
        """
        mods = self._loadedMods[modPart]
        if clazz in mods:
            return mods["class"]
        else:
            #mod = __import__(clazz)
            path = join("lib", modPart, clazz + ".py")
            mod = imp.load_source(clazz, path)
            mods[clazz] = mod
            return mod
    
    def replace_with_import(self, objList, modPart, items_func, class_check):
        """
        replaces configuration dicts with their objects by importing and creating it in the first step.
        In the second step the original list of json config dicts gets replaced by the loaded objects

        :param objList: the list of objects which is iterated on
        :param modPart: the folder from the module (i.e tasks, parsers)
        :param items_func: function to get a pointer on the list of json-config-objects to replace. Takes one argument and
        should return a list of
        :param class_check: currently unsupported
        """
        for obj in objList:
            repl = []
            items = items_func(obj)
            for clazzItem in items:
                try:

                    clazz = clazzItem["class"]
                    mod = self._load_module(clazz, modPart)
                    item = mod.create(clazzItem)
                    if class_check(item):
                        repl.append(item)
                    else:
                        self.log.w(" ignoring class " + clazzItem["class"] + "! It does not pass the class check!")

                except ImportError, err:
                    self.log.w("could not import " + clazz + ": " + str(clazzItem) + "! reason")
                    self.log.w(str(err))
                except KeyError, k:
                    self.log.w("Key " + str(k) + " not in classItem " + str(clazzItem))
                except Exception, e:
                    self.log.w("Error while replacing class ( " + clazz + " ):" + str(e))

            del items[:]
            items.extend(repl)

    def replace_pointer(self, objectList, replObjectList, id_list_func, id_get_func):
        """
        replaces objects from the config by ids.

        :param objectList: the list of objects to be iterated on
        :param replObjectList: the list of objects to replace
        :param id_list_func: function taking one argument as object and should return a list of config ids to replace
        :param id_get_func: function taking one config-object as argument and should return the config id to compare
        """
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
        pass


def parsePeriodList(name, values):
    if "date" in values:
        return DatePeriod(name, **values)
        
    comp = ["weeks", "days", "hours", "minutes", "seconds", "start_date"]
    if len([i for i in comp if i in values]) > 0:
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
        which contains all necessary information of the config file.
        parses the full config
        Parsing will be done in 3 steps:
        1. get raw Config Objects by just passing the values defined inside the config
        2. replace references by objects, import services, tasks, parsers and processors
        3. do sanity checks
        
        :param configFilename: the configuration file to parse
        """
        self.jsonDict = self._read_json_config(configFilename)
        
        # first step
        creator = lambda name, values: Layout(name,**values)
        layouts = self._create_raw_Object(self.jsonDict[KEY_LAYOUTS], "Layout", creator)
        
        creator = lambda name, values: Member(name, **values)
        members = self._create_raw_Object(self.jsonDict[KEY_MEMBERS], "Member", creator)
        
        creator = lambda name, values: HostGroup(name, **values)
        self.hostgroups = self._create_raw_Object(self.jsonDict[KEY_HOSTGROUPS], "Hostgroup", creator)
        
        creator = parsePeriodList
        periods = self._create_raw_Object(self.jsonDict[KEY_PERIODS], "Period", creator)

        #2. import and replace
        items_func = lambda hostgroup: hostgroup.get_services()
        class_check = lambda service: isinstance(service, Service)
        self.replace_with_import(self.hostgroups, MOD_SERVICES, items_func, class_check)
        
        items_func = lambda hostgroup: hostgroup.get_processors()
        class_check = lambda processor: isinstance(processor, Processor)
        self.replace_with_import(self.hostgroups, MOD_PROCESSORS, items_func, class_check)

        services = []
        for hg in self.hostgroups:
            services.extend(hg.get_services())

        items_func = lambda service: service.get_parser()
        class_check = lambda parser: isinstance(parser, Parser)
        self.replace_with_import(services, MOD_PARSERS, items_func, class_check)
        
        items_func = lambda member: member.get_tasks()
        class_check = lambda task: isinstance(task, Task)
        self.replace_with_import(members, MOD_TASKS, items_func, class_check)

        #replace object pointer
        id_list_func = lambda hostgroup: hostgroup.get_members()
        id_get_func = lambda member: member.get_id()
        self.replace_pointer(self.hostgroups, members, id_list_func, id_get_func)

        id_list_func = lambda service: service.get_periods()
        id_get_func = lambda period: period.get_name()
        self.replace_pointer(services, periods, id_list_func, id_get_func)

        id_list_func = lambda layout: layout.get_hostgroups()
        id_get_func = lambda hostgroup: hostgroup.get_name()
        self.replace_pointer(layouts, self.hostgroups, id_list_func, id_get_func)

        for hg in self.hostgroups:
            for service in hg.get_services():
                service.set_hostgroup(hg)
        core = None
        if "core" in self.jsonDict:
            core = self.jsonDict["core"]

        return layouts, core