from distutils.core import setup

setup(
    name='linspector',
    version='0.12.1-alpha',
    packages=['bin', 'linspector', 'linspector.core', 'linspector.tasks', 'linspector.config', 'linspector.backends',
              'linspector.services', 'linspector.services.etc', 'linspector.services.net', 'linspector.services.ssh',
              'linspector.services.http', 'linspector.services.snmp',
              'linspector.frontends'],
    url='http://linspector.org',
    license='AGPLv3',
    author='hanez',
    author_email='you@hanez.org',
    description='linspector is for monitoring the vital information of hosts, services and devices in a network'
)
