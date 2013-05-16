from ..core import logger


class Layout:
    def __init__(self, myLayout):
        self.name = myLayout
        self.enabled = False
        self.hostgroups = []

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
                                logger.logWarningConfig(file="hostgroups", missing=group)
                self.layouts.append(l)

    def __str__(self):
        ret = ""
        ret += "Plugins: " + str(self.plugins) + "\n"
        for layout in self.layouts:
            ret += str(layout) + "\n"
        return ret
