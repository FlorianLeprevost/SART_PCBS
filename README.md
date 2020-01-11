# SART task + data analysis
What I want to do is
I) first to program in python (1) the SART task (2) with several levels of difficulty (3) with probe apparition depending on the last reaction times

II) Then I want to program in R (1) the data analysis I'm going to do,  in a Rmarkdown document.


# 1) Sustained Attention to Response Task

## 1.1) SART  explanation and steps
### 1.1.1) Classic SART
The Sustained Attention to Response Task (SART) is a go/no-go task, which demand sustained but very little attention. It is often used combined with "thought probes" as a paradigm to investigate Mind Wandering. Indeed, as the task is long and boring, you are more likely to think of something else, and "wander" in/with your mind. The "thought probes" are sudden interruption of the task accompanied by a question that inquires about the participant's thoughts. See [Weinsten 2018](https://link.springer.com/article/10.3758/s13428-017-0891-9) for a review of probes.

I coded the SART task using the information from the [following site](https://scienceofbehaviorchange.org/measures/sustained-attention-to-response-task/).

### 1.1.2) My experiment

I based my experiment on the [Seli 2016 article](https://doi.org/10.1016/j.concog.2016.02.002), but I added some novelties. Their results was that

![Seli 2016](Seli.png)
In COGSCI311 class, we had to think of a new experiment, so I programmed a simplified version of [what I thought of](projetv3.pdf)

. Instead of using binary choice (Mind wandering or on-task thoughts) I used scales that may more precisely reflect the subjects experience ("how related are your thoughts to the task?"). I also wanted to introduce the notion of agency that is slightly different than what Seli et al. call intention.

What I had to do:
- [x] create a list of numbers to display
- [x] make sure I have the right number of no-go trials
- [x] make sure my no-go trials aren't too close from each other
- [x] make sure the ISI stayed at 1150ms even when subject answered early
- [x] random character size display between 5 possible

### 1.1.3) Probes
I used the [Seli 2016 article](https://doi.org/10.1016/j.concog.2016.02.002) to determine the probe rate.

What I had to do
- [x] create a different file to get probe data
- [x] create a trial number and a block_number var to add in file
- [x] set the probes to appear randomly during sub-blocks of 45 trials (and not to close to the begining and end of block)


### 1.1.4) Difficulty levels
Again, I used I used the [Seli 2016 article](https://doi.org/10.1016/j.concog.2016.02.002) to create the easy SART task.
- [x] change the way block lists are created

## 1.2) SART code
### 1.2.1) Stim
Create a list of numbers to display (block_list)

```python
numbers = list(range(0,10))
numbers.remove(3)                       #the no-go trial
block_list=[]
while len(block_list)<nb_el_block:      #with nb_el_block the number of stim wanted in a block
    block_list.append(numbers[randint(0,8)])
```
Insert randomly (and not too close to each other) no-go trials in list
```python
if compt < nb_nogo and 3 not in block_list[-5:]:
    dice=randint(1,10)
    if dice == 1:
        block_list.append(3)
        compt+=1

```
Make sure I have the right number of no-go trials
```python
while compt<nb_nogo:
    loca= randint(0,nb_el_block-1)              #any position in the list I just made
    if 3 not in block_list[loca-5 : loca+5]:    #that is not too close to another no-go
        block_list[loca]=3
        compt +=1

```

### 1.2.2) Classic block
For the gist of the code of a block, I copied from an example on the [expyriment stash of example on GitHub](https://github.com/expyriment/expyriment-stash/tree/master/examples). It's pretty straight forward

```python
block = list_creation(nb_el_block, nb_nogo)     #I create stim with the code of 1.1.1)
trial_number = 0
for digit in block:
    trial_number +=1
    target = stimuli.TextLine(text=str(digit))
    mask = stimuli.TextLine(text='X\u0336')
    target.present()
    exp.clock.wait(250)
    mask.present()
    button, rt = exp.keyboard.wait(misc.constants.K_SPACE, 900)   #get response and reaction time
    error = (button == misc.constants.K_SPACE and digit == 3) or (button == [] and digit !=3)

    exp.data.add([digit, button, rt, int(error), block_name])     # save the data
```

I added some subtleties like:
- varying font sizes
```python
font_sizes_list = [48, 72, 94, 100, 120 ]
...
f_size = randint(0,4)
target = stimuli.TextLine(text=str(digit), text_size= font_sizes_list[f_size])
```
- make sure the ISI stays at 1150 ms
```python
if rt != None:
        time_left = 900-rt
        exp.clock.wait(time_left - stimuli.BlankScreen().present())
```

### 1.2.3) Experiment and Probes
I made a "main" function with the instructions, that present the experiment, depending of the parameters of the beginning of the script. I also put the aforementionned expyriment for loop in a function to be able to call it several times
```python
nb_block_r = 1
nb_el_block_r = 270
nb_nogo_r = 18
nb_probes_r = 6
```
I created to function to display the probes (probes) and another one to make sure the probes appeared at pseudo-random interval, not too close to each other (probe-random).
```python

def probe_random(nb_el_block, nb_probes):
    sub_block = round(nb_el_block/nb_probes)       #length of intervals within each a probe should appear
    limits = round(0.1*sub_block)                  #makes sure the probes aren't in the very beginning or very end of each interval
    probe_trials=[]
    for i in range(nb_probes):                     #produce the trial numbers in which probes are going to appear
        probe_tr = randint(sub_block*i +limits, sub_block*(i+1)-limits)
        probe_trials.append(probe_tr)

    return probe_trials
```


A difficult part was to automatize the creation of file in which the probe data could be stored. For it to work, I had to initialize the experiment and create the files outside of main.

```python
#fichier probes
data_probe_name = ['probe_data', str(exp.subject)]  #retrieve subject number to create the name of the variable and of the file
data_file_name = ['probe_data', str(exp.subject), '.txt']
globals()[''.join(data_probe_name)] = open(''.join(data_file_name), "w") # creates and open a file with the number of the subject in it
globals()[''.join(data_probe_name)].write('block_number, trial_number, relatedness\
, rt_rel, control, rt_con\n') #write the variable names in the first line
globals()[''.join(data_probe_name)].close
```
Then an if loop in the "block" function, I could write every answer in the file
```python

if trial_number in probe_trials:
    button_r, rt_r, button_c, rt_c = probes()

    globals()[''.join(data_probe_name)] = open(''.join(data_file_name), "a")
    globals()[''.join(data_probe_name)].write(str(block_name)+','+str(trial_number)\
    +','+str(button_r)+','+str(rt_r)+','+str(button_c)+','+str(rt_c)+ '\n')
    globals()[''.join(data_probe_name)].close
```

### 1.2.4) Easy SART
To program the easy version of the SART, I deleted the no

# 2) Data
To have some data to analyse, I made two persons pass a reduced version of the experiment (only one block in each condition = approx. 15 minutes).

Then I used Rmarkdown to go through and document the data analysis: please see the data_analysis_SART.html ou .Rmd in the folder for more details.
