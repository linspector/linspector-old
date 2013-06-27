import json
import imp
import os.path as path

class DummyParent(object):
    def __init__(self, name=None, argsToReplace=None):
        self.name = name
        self.argsToReplace = argsToReplace

    def get_args_to_replace(self):
        return self.argsToReplace


def replace_with_import(objList, items_func):
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
                    p = path.join("lib", clazz + ".py")
                    mod = imp.load_source(clazz, p)
                    item = mod.create(clazzItem)
                    repl.append(item)
                except ImportError, err:
                    print "could not import " + clazz + ": " + str(clazzItem) + "! reason"
                    print str(err)
                except KeyError, k:
                    print "Key " + str(k) + " not in classItem " + str(clazzItem)
                except Exception, e:
                    print "Error while replacing class ( " + clazz + " ):" + str(e)

            del items[:]
            items.extend(repl)

jsonFile = '''
{
    "someDummy": {
        "argsToReplace":
        [
            {"class": "dummy", "args": {"someargs":"ok"}},
            {"class": "dummy", "args": {"someother":"blah"}}
        ]
    }
}
'''

jsonDict = json.loads(jsonFile)

dummys=[]
for key, val in jsonDict.items():
    dummys.append(DummyParent(key, **val))

items_func = lambda dummy: dummy.get_args_to_replace()
replace_with_import(dummys, items_func)



