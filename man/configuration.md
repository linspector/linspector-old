Linspector configuration
========================

members
-------

periods
-------

hostgroups
----------

layouts
-------

core
----

### instance_name
* instance1 -> Name of the Linspector instance (optional)

### max_logfile_size
* 1024000 -> Size of logfile in Bytes

### max_logfile_count
* 4 -> count of logfiles to save in rotation

### threshold_handling:
* "reset" -> Resets the threshold when service runs successful
* "decrement" -> Decrements the threshold when service runs successful (default)