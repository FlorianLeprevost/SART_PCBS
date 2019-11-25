# Ce programme est destiné à lancer une tache SART (avec 2 conditions de difficultés) 
# ainsi que des "thought probes" qui apparaitront en fonction de la variabilité des RTs des 8derniers essais
# voir README.md pour explicatino de cet aspect
#https://scienceofbehaviorchange.org/measures/sustained-attention-to-response-task/ pour détails


from expyriment import control, stimuli, design, misc
from random import randint


def list_creation():
	numbers = list(range(0,10))
	numbers.remove(3)
	compt = 0
	block_list = []
	while len(block_list)<26:
		block_list.append(numbers[randint(0,8)])
		if compt < 8 and 3 not in block_list[-5:]:
				dice=randint(1,10)
				if dice == 1:
					block_list.append(3)
					compt+=1
	while compt<1:
		loca= randint(0,259)
		if 3 not in block_list[loca-5 : loca+5]:
			block_list[loca]=3
			compt +=1
    
	return block_list


def experience():
    #random size out of 5
    font_sizes_list = [48, 72, 94, 100, 120 ]
    
    # dont go into full screen mode with this line
    block = list_creation()
    
    exp = design.Experiment(name="SART")
    control.set_develop_mode(on=True)  ## Set develop mode. Comment for real experiment
    control.initialize(exp)
    exp.data_variable_names = ["digit", "btn", "rt", "error"]
    
    control.start()
    for digit in block:
        f_size = randint(0,4)
        target = stimuli.TextLine(text=str(digit), text_size= font_sizes_list[f_size])
        mask = stimuli.TextLine(text='X\u0336', text_size= font_sizes_list[f_size])
        
        target.present()
        exp.clock.wait(250)
        mask.present()     
        button, rt = exp.keyboard.wait(misc.constants.K_SPACE, 900)

        error = (button == misc.constants.K_SPACE and digit == 3) or (button ==[] and digit !=3)
        exp.data.add([digit, button, rt, int(error)])
    
    print(exp.data)
    control.end(goodbye_text="Thank you very much...", goodbye_delay=2000)

experience()