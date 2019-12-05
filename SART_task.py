# Ce programme est destiné à lancer une tache SART (avec 2 conditions de difficultés)
# ainsi que des "thought probes" qui apparaitront en fonction de la variabilité des RTs des 8derniers essais
# voir README.md pour explicatino de cet aspect
#https://scienceofbehaviorchange.org/measures/sustained-attention-to-response-task/ pour détails


from expyriment import control, stimuli, design, misc
from random import randint

#crée une liste pseudo random de chiffres pour créer des stimuli  avec le nombre
#total de stimuli et le nombre de no-go trial voulu (defini dans main)
def list_creation(nb_el_block, nb_nogo):
    numbers = list(range(0,10))
    numbers.remove(3)
    compt = 0
    block_list = []
    while len(block_list)<nb_el_block:
        block_list.append(numbers[randint(0,8)])
        if compt < nb_nogo and 3 not in block_list[-5:]:
            dice=randint(1,10)
            if dice == 1:
                block_list.append(3)
                compt+=1
    while compt<nb_nogo:
        loca= randint(0,nb_el_block-1)
        if 3 not in block_list[loca-5 : loca+5]:
            block_list[loca]=3
            compt +=1

    return block_list


#creer les probes
def probes():

    instructions = stimuli.TextLine(text="From 1 to 9.\
    \n How are your thoughts related to the task?\
    \n [totally related] 1 2 3 4 5 6 7 8 9 [totally unrelated]")
    stim.present()
    button_r, rt_r = exp.keyboard.wait(misc.constants.K_ALL_DIGITS)

    instructions = stimuli.TextLine(text="From 1 to 9.\
    \n How in control of your train of thought did you feel ? ?\
    \n [In control] 1 2 3 4 5 6 7 8 9 [Not in control]")
    stim.present()
    button_c, rt_c = exp.keyboard.wait(misc.constants.K_ALL_DIGITS)

    return button_r, rt_r, button_c, rt_c
    
    globals()[''.join(data_probe_name)] = open(''.join(data_file_name), "a")
    globals()[''.join(data_probe_name)].write(str(block_name)+str(trial_number)\
    +str(button_r)+str(rt_r))++str(button_c)+str(rt_c))




#fait un block
def blocks(nb_el_block, nb_nogo, exp, block_name):
    #random size out of 5
    font_sizes_list = [48, 72, 94, 100, 120 ]

    # dont go into full screen mode with this line
    block = list_creation(nb_el_block, nb_nogo)
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


def main():

    exp = design.Experiment(name="SART")
    control.set_develop_mode(on=True)  ## Set develop mode. Comment for real experiment
    control.initialize(exp)
    control.start()
    exp.data_variable_names = ["digit", "btn", "rt", "error", "block_name"]

#crée data file for probes (and reaction time variability)
    data_probe_name = ['probe_data', exp.subject]
    data_file_name = ['probe_data', exp.subject, '.txt']
    globals()[''.join(data_probe_name)] = open(''.join(data_file_name), "w")
    globals()[''.join(data_probe_name)].write('block_number, trial_number, relatedness, rt_rel, control, rt_con'))

#practice block
    instructions = stimuli.TextLine(text="Thank you for participating in this experiment. \
    \nThe task is very simple : you will see numbers appeat briefly on the screen , followed by a crossed capital X.\
    \nYou must press spacebar everytime you see a number EXCEPT when it's the number 3. \
    \n\n You also need to know that at random momentsIf you understood well and are ready to do a practice trial, press space bar")
    stim.present()
    exp.keyboard.wait(misc.constants.K_SPACE)

    nb_el_block = 10
    nb_nogo = 2
    block_name = "practice"
    blocks(nb_el_block, nb_nogo, exp, block_name)

#real blocks
    nb_el_block = 12
    nb_nogo = 2
    instructions = stimuli.TextLine(text="Instructions:\nYou must press spacebar everytime you see a number EXCEPT when it's the number 3. \
    \nAnswer one the scale about your thoughts when they appear. \
    \n\nIf you are ready for the real experiment, press space bar")
    stim.present()
    exp.keyboard.wait(misc.constants.K_SPACE)

    for i in range(2):
        block_name = "real" + str(i+1)
        blocks(nb_el_block, nb_nogo, exp, block_name)
        instructions = stimuli.TextLine(text="Ready for the next trial? Press spacebar")
        stim.present()
        exp.keyboard.wait(misc.constants.K_SPACE)

    control.end(goodbye_text="Thank you very much...", goodbye_delay=2000)

main()
