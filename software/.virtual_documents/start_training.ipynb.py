#get_ipython().run_line_magic("serialconnect", " to --port=/dev/ttyUSB0 --baud=115200")
get_ipython().run_line_magic("serialconnect", " to --port=COM4 --baud=115200")


get_ipython().run_line_magic("sendtofile", " --source=\"training2.py\" \"training2.py\"")
#get_ipython().run_line_magic("sendtofile", " --source=\"training.py\" \"training.py\"")
get_ipython().run_line_magic("rebootdevice", "")


#import servo
#import tasks
#import training 
import training2



#set testing to 1 if you need to run things faster for testing purposes
#task = tasks.Task1(testing=1)
#task = training.Task1(testing=0)
task = training2.Task1(testing=0)



task.moveBackDelay = 700


#test solenoids 
task.solenoid1()



task.solenoid2()


#range of movement of the servo motors
#maximal max value 65
#minimum min value 25
task.servoMax = 43
task.servoMin = 26

#move servos forward
task.move_servos_forward()



task.move_servos_backward()



task.reward2Duration = 130
task.reward1Duration = 130


get_ipython().run_line_magic("capture", " \"test.csv\"")

task.run_task1()





get_ipython().run_line_magic("capture", " cap ")
#--no-stderr
print ('stuff')



get_ipython().run_line_magic("fetchfile", "  \"session_res.csv\" ")


%
