class LayouException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr(self.msg)

class Layout:
    def __init__(self, name, enabled = False , hostgroups=None):
        self._name = name
        self._enabled = enabled

        if hostgroups is None or len(hostgroups) <= 0:
            raise Exception("Layout: " + name + " without hostgroups is useless")
        else:
            self._hostgroups = hostgroups
            
    def get_name(self):
        return self._name
    
    def is_enabled(self):
        return self._enabled

    def get_hostgroups(self):
        return self._hostgroups

    def __str__(self):
        ret = "Layout: 'Name:" + str(self.name) + "', 'Enabled: " + str(self.enabled) + " "
        for group in self.hostgroups:
            ret += str(group)
        return ret


class LayoutList:
    def __init__(self, layouts, hostgroups):
        self.layouts = []
        self.dict = layouts
        self.plugins = []
        for k, v in layouts.items():
            if k in ("plugins", "Plugins"):
                self.plugins = v
                continue
            else:
                l = Layout(k)
                for k1, v1 in v.items():
                    if k1 in ("enabled", "Enabled"):
                        l.enabled = v1
                    elif k1 in ("hostgroups", "Hostgroups"):
                        l.hostgroups = []
                        for group in v1:
                            h = None
                            for hostg in hostgroups:
                                if hostg.name == group:
                                    h = hostg
                                    break
                            if h is not None:
                                l.hostgroups.append(h)
                            else:
                                # TODO: replace next line with new logging
                                #logger.logWarningConfig(file="hostgroups", missing=group)
                                pass
                self.layouts.append(l)

    def __str__(self):
        ret = ""
        ret += "Plugins: " + str(self.plugins) + "\n"
        for layout in self.layouts:
            ret += str(layout) + "\n"
        return ret
