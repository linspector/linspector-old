This is the manual page for Lish - The Linspector interactive Shell
===================================================================

Introduction
------------

Lish ist the Linspecor interactive Shell. It is the primary interface for
managing a Linspector instance. It is a command prompt like a normal
system shell for accessing all kind of objects.

In Lish you can enable or disable services when a service fails to stop
alerting. You can list current running jobs ang get detailed information
about single jobs.

Since Lish is under heavy development and we have not defined the syntax
most features are not implemented but will be when we are releasing the
first production release of Linspector.

Commands
--------

### about

Show the About dialog.

### exit

Exits Linspector.

### help

Show simple overview of available commands or of detailed information about
special commands. E.g.: `help job` shows help for the job command.

### job

Job related Command.

### jobs

Jobs related Command.

### license

Show licensing information.

### log

Manage Logging.

### man

Show detailed documentation like UNIX man pages. E.g.: `man job` shows the
complete job command manual page.

### python

Executes Python code using exec. E.g.: `python time.sleep(5)`. you will have
full access to Linspector objects from your Python code, so be careful using
this.

### shell or !

Executed system shell commands. E.g.: `shell df` or `!df` executes the "df"
command from your $PATH.

### status

Show the internal status of Linspector.

Selectors
---------

Selectors are used to select special objects in Lish commands. For example
`jobs @all list` lists all jobs and `jobs %foobar list` lists all jobs for
Host "foobar".

*   `@` = Predefined group; Example `@all`
*   `$` = Hostgroup
*   `%` = Host
*   `?` = Service
*   `!` = Job
*   `~` = Member
*   `&` = unused
*   `#` = unused
*   `+` = unused
*   `§` = unused

Examples:
---------

### Configuration

*   `config @hostgroup add %host`

*   `config @hostgroup %host del ?service`

*   `config @hostgroup %host add ?service "OBJECT"`

### Job Management

*   `jobs @all table`

*   `jobs @all list`

*   `jobs ?service list`

*   `jobs $hostgroup list`

*   `jobs @hostgroup enable`

*   `jobs %host enable`

*   `jobs %host list`

*   `jobs @all list`

*   `jobs ?tcpconnect list` (what about args?)

*   `jobs ?tcpconnect disable`

*   `jobs %host`

*   `jobs @all list 10-20` (list job 10 to 20)

*   `jobs !jobid enable` (enable two jobs)

*   `jobs !jobid1,jobid2 diable` (disable two jobs)

*   `jobs &hostgroup %host list`

*   `jobs &hostgroup %host disable` (disable all jobs for `%host` in `&hostgroup`)

*   `jobs &hostgroup %host ?service disable` (disable a service for `%host` in  `&hostgroup`)

*   `jobs &hostgroup %host ?service disable`

*   `jobs !4b22e5e7 enable`

*   `jobs !4b22e5e7,4b22e5e6 enable`
