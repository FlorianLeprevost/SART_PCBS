# SART task + data analysis
What I want to do is
I) first to program in python (1) the SART task (2) with several levels of difficulty (3) with probe apparition depending on the last reaction times

II) Then I want to program in R (1) the data analysis I'm going to do, ideally in a Rmarkdown document. (I'm not yet sure about how I'm going to go with this)


# 1) Sustained Attention to Response Task

## 1.1) SART  explanation and steps
### 1.1.1) Classic SART
The Sustained Attention to Response Task (SART) is a go/no-go task, which demand sustained but very little attention. It is often used combined with "thought probes" as a paradigm to investigate Mind Wandering. Indeed, as the task is long and boring, you are more likely to think of something else, and "wander" in/with your mind. The "thought probes" are sudden interruption of the task accompanied by a question that inquires about the participant's thoughts. See [Weinsten 2018](https://link.springer.com/article/10.3758/s13428-017-0891-9) for a review of probes.

I coded the SART task using the information from the [following site](https://scienceofbehaviorchange.org/measures/sustained-attention-to-response-task/).

What I had to do:
- [x] create a list of numbers to display
- [x] make sure I have the right number of no-go trials
- [x] make sure my no-go trials aren't too close from each other
- [x] make sure the ISI stayed at 1150ms even when subject answered early
- [x] random character size display between 5 possible

### 1.1.2) Probes
I used the [Seli 2016 article](https://doi.org/10.1016/j.concog.2016.02.002) to determine the probe rate.

What I had to do
- [x] create a different file to get probe data
- [x] create a trial number and a block_number var to add in file
- [x] set the probes to appear randomly during sub-blocks of 45 trials (and not to close to the begining and end of block)


### 1.1.3) Difficulty levels
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

### 1.2.3) Several blocks

# 2) Data analysis
## 2.1) Analysis explanation and steps
### 2.1.1) Get data
Create a data frame with the subject number, probe scores, and reaction time variability
- [ ] data.frame with subject + probe score
- [ ] get the reaction-time variability (see [Bastian & Sackur 2013](https://www.frontiersin.org/articles/10.3389/fpsyg.2013.00573/full) before the probe.

Also check the skill index for control
- [ ] get the skill index (mean no-go-trial accuracy divided by mean go-trial RT; Jonker, Seli, Cheyne, &
Smilek, 2013) for each subject for each task.
