# connect to the micropython board

#get_ipython().run_line_magic("serialconnect", " to --port=/dev/ttyUSB0 --baud=115200")
get_ipython().run_line_magic("serialconnect", " to --port=com4 --baud=115200")


get_ipython().run_line_magic("sendtofile", " --source=\"main.py\" \"main.py\"")
get_ipython().run_line_magic("sendtofile", " --source=\"boot.py\" \"boot.py\"")
get_ipython().run_line_magic("sendtofile", " --source=\"tasks.py\" \"tasks.py\"")
get_ipython().run_line_magic("sendtofile", " --source=\"training.py\" \"training.py\"")
get_ipython().run_line_magic("sendtofile", " --source=\"training2.py\" \"training2.py\"")
#get_ipython().run_line_magic("sendtofile", " --source=\"tests.py\" \"tests.py\"")
get_ipython().run_line_magic("rebootdevice", "")




#print board contents
get_ipython().run_line_magic("ls", "")


#print a list of available commands
get_ipython().run_line_magic("lsmagic", "")


#get_ipython().run_line_magic("rebootdevice", "")
#get_ipython().run_line_magic("%local", "")
#pyboard.py --device /dev/com4 -f cp main.py :main.py
#import pyboard
#pyb = pyboard.Pyboard('/dev/ttyUSB0', 115200)
#pyb = pyboard.Pyboard('/dev/com4', 115200)


pyb



