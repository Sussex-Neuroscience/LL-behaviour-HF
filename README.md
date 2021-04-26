# LL-behaviour-HF

a behavioural control system for head fixed mice



The task:

- At the start there is a 10 sec interval without a stimulus to record baseline activity. Then the mouse sees a stimulus (always the same drifting grating) which appears randomly either on the left or the right screen. after 5 sec. of stimulus presentation the actuator moves the lick sensors in front of the mouse for two sec. in which the mouse has to report on which side the stimulus is present, hence lick left or right. If the answer is correct a reward is given (solenoid valves). If the answer is incorrect no reward is given. The actuator retracts the lick sensors after 2 sec. either way. Then there is an inter trial interval for 5+ sec before the next stimulus will be presented. If the mouse was incorrect the stimulus will be presented on the same side as the trial before until the mouse makes the correct decision (to avoid bias).I might want to change the timeframes for the different stages depending on how the training goes.


- There will also be a second task where stimuli are presented on both sides on the screen (differing in orientation or contrast) and the animal has to decide which of the stimuli is the correct one. The time course will be the same, it is just the task that is changing.

- The stimulus orientation, size, contrast, frequencies etc. will be different for every mouse but will be the same throughout the training sessions, so there is only 1 type of stimulus in the first task and 2 type of stimuli in the second task. 

- The random stimulus presentation isn't in the code yet. So far, there was no task for the animal, so we always displayed the same stimulus on both sides simultaneously by mirroring one screen to the other. I'll have another chat with Antonio today to see how trivial it is to change that towards what I need.

 

 

- As for the scanimage channels. Yes, I was talking about the analog inputs. The DAQ has a lot of free slots left and I guess there are free digital inputs. I'm not too familiar with setting these things up.

 

- If everything works just using the labjack that would be great. We have an Arduino uno lying around just in case it is needed.


---

schematics on how the system is working and how it should work:

![](/media/connections_treadmill_setup.jpg)

--- 

### notes on implementation:

from what I could gather, Psychopy is not indicated to do millisecond precision of many different variables at once. I had a look on how it deals with timing (more info [here](https://www.psychopy.org/_modules/psychopy/clock.html#Clock)), and thinking that a good route would be to do the behavioural timing critical things on the ESP32.


---

initial bill of materials:

|||
|---|---|
|Linear actuator||
|solenoid valves||
|lick sensors||
|beehive main board||
|beehive peltier board||
|beehive solenoid valve board||
|||
