Programmed and tested using IDLE 3.3.2 on Windows 8.1, may work differently on other combinations of operating systems and IDLE enviroments.

Supports filename and mode switching as arguments in a command line (ssps.py [FILENAME] [-d,-s]) or, if not provided a filename, will display a prompt at runtime asking for the filename and mode.

filename: Name of the ssps program that you wish the interpretor to interprete.
mode:
 -d: Dynamic linking, variables are "defined" by their most recent live definition.
 -s: Static linking, variables are "defined" by their most recent *parent* definition within their scope.