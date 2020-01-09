"""This programm launches an EASY sustained-attention-to-response task (SART; https://scienceofbehaviorchange.org/measures/sustained-attention-to-response-task/)
Make sure your arguments are correct, the following is the classic SART:

Practice block :
    nb_el_block_p = 160
    nb_nogo_p = 8
    nb_probes_p = 14
Real blocks :
    nb_block_r = 4
    nb_el_block_r = 260
    nb_nogo_r = 18
    nb_probes_r = 6



"""
from expyriment import control, stimuli, design, misc
from random import randint


#définir les paramètres (nombre de trials par block, de no_go par block,
# de probe par block, pour le block practice (p) et pour les real blocks (r))
nb_el_block_p = 20
nb_nogo_p = 2
nb_probes_p = 1

nb_block_r = 1
nb_el_block_r = 260
nb_nogo_r = 2
nb_probes_r = 6


#crée une liste pseudo random de chiffres pour créer des stimuli  avec le nombre
#total de stimuli et le nombre de no-go trial voulu (defini dans main)


#creer les probes
def probes():

    instructions = stimuli.TextScreen(heading = "Hold your thoughts!",text="From 1 to 9.\
    \n How are your thoughts related to the task?\
    \n [totally unrelated] 1 2 3 4 5 6 7 8 9 [totally related]")
    instructions.present()
    button_r, rt_r = exp.keyboard.wait(misc.constants.K_ALL_DIGITS)

    instructions = stimuli.TextScreen(heading = "", text="From 1 to 9.\
    \n How in control of your train of thought did you feel ? ?\
    \n [Not in control] 1 2 3 4 5 6 7 8 9 [Totally in control]")
    instructions.present()
    button_c, rt_c = exp.keyboard.wait(misc.constants.K_ALL_DIGITS)

    return button_r, rt_r, button_c, rt_c


#determine which trials are gonna have a probe
def probe_random(nb_el_block, nb_probes):
    sub_block = round(nb_el_block/nb_probes)
    limits = round(0.1*sub_block)
    probe_trials=[]
    for i in range(nb_probes):
        probe_tr = randint(sub_block*i +limits, sub_block*(i+1)-limits)
        probe_trials.append(probe_tr)

    return probe_trials


#fait un block
def blocks(nb_el_block, nb_nogo, nb_probes, exp, block_name):
    #random size out of 5
    font_sizes_list = [48, 72, 94, 100, 120 ]

    #list far easier this way
    #numbers = list(range(0,10))
    repetitions = round(nb_el_block/10)
    block =[]
    for i in range(repetitions):
        for j in range(0,10):
            block.append(j)

    probe_trials = probe_random(nb_el_block, nb_probes)
    trial_number = 0
    for digit in block:
        trial_number +=1
        f_size = randint(0,4)
        target = stimuli.TextLine(text=str(digit), text_size= font_sizes_list[f_size])
        mask = stimuli.TextLine(text='X\u0336', text_size= font_sizes_list[f_size])

        target.present()
        exp.clock.wait(250)
        mask.present()
        button, rt = exp.keyboard.wait(misc.constants.K_SPACE, 900)

        #to make sure the ITI stays at 1150ms
        if rt != None:
            time_left = 900-rt
            exp.clock.wait(time_left - stimuli.BlankScreen().present())

        error = (button == misc.constants.K_SPACE and digit == 3) or (button == [] and digit !=3)
        exp.data.add([digit, button, rt, int(error), block_name])

        #probe trials
        if trial_number in probe_trials:
            button_r, rt_r, button_c, rt_c = probes()

            globals()[''.join(data_probe_name)] = open(''.join(data_file_name), "a")
            globals()[''.join(data_probe_name)].write(str(block_name)+','+str(trial_number)\
            +','+str(button_r)+','+str(rt_r)+','+str(button_c)+','+str(rt_c)+ '\n')
            globals()[''.join(data_probe_name)].close


def main(exp):
#crée data file for probes (and reaction time variability)

#practice block
    instructions = stimuli.TextScreen(heading = "Practise", text="Thank you for participating in this experiment. \
    \nThe task is very simple : you will see numbers appear briefly on the screen, followed by a crossed capital X.\
    \nYou must press spacebar everytime you see a number EXCEPT when it's the number 3. \
    \n\n You also need to know that at random moments, 'thought probes' are going to appear. \
    \nThose probes inquire about what you were thinking about, just before they appeared.\
    \n\nIf you understood well and are ready to do a practice trial, press space bar")
    instructions.present()
    exp.keyboard.wait(misc.constants.K_SPACE)
    block_name = "practice"
    blocks(nb_el_block_p, nb_nogo_p, nb_probes_p, exp, block_name)

#real blocks

    instructions = stimuli.TextScreen(heading = "Experiment",text="Instructions:\nYou must press spacebar everytime you see a number EXCEPT when it's the number 3. \
    \nAnswer on the scaleS about your thoughts when they appear. \
    \n\nIf you are ready for the real experiment, press space bar")
    instructions.present()
    exp.keyboard.wait(misc.constants.K_SPACE)

    for i in range(nb_block_r):
        block_name = "real" + str(i+1)
        blocks(nb_el_block_r, nb_nogo_r, nb_probes_r, exp, block_name)
        instructions = stimuli.TextLine(text="Ready for the next trial? Press spacebar")
        instructions.present()
        exp.keyboard.wait(misc.constants.K_SPACE)

    control.end(goodbye_text="Thank you very much...", goodbye_delay=2000)




## MAIN
exp = design.Experiment(name="SART")
control.set_develop_mode(on=False)  ## Set develop mode. Comment for real experiment
control.initialize(exp)
control.start()
exp.data_variable_names = ["digit", "btn", "rt", "error", "block_name"]

#fichier probes
data_probe_name = ['probe_data_easy', str(exp.subject)]
data_file_name = ['probe_data_easy', str(exp.subject), '.txt']
globals()[''.join(data_probe_name)] = open(''.join(data_file_name), "w")
globals()[''.join(data_probe_name)].write('block_number, trial_number, relatedness\
, rt_rel, control, rt_con\n')
globals()[''.join(data_probe_name)].close


main(exp)
