# Ce programme est destiné à lancer une tache SART (avec 2 conditions de difficultés) 
# ainsi que des "thought probes" qui apparaitront en fonction de la variabilité des RTs des 8derniers essais
# voir README.md pour explicatino de cet aspect
#https://scienceofbehaviorchange.org/measures/sustained-attention-to-response-task/ pour détails


from expyriment import control, stimuli, design, misc

# création des stimuli 
numbers = list(range(1,10))
print (numbers)
# dont go into full screen mode with this line
design.randomize.shuffle_list(numbers)

exp = design.Experiment(name="SART")
control.set_develop_mode(on=True)  ## Set develop mode. Comment for real experiment
control.initialize(exp)
exp.data_variable_names = ["digit", "btn", "rt", "error"]

control.start()
for digit in numbers:
    target = stimuli.TextLine(text=str(digit), text_size=80)
    exp.clock.wait(500 - stimuli.FixCross().present() - target.preload())
    target.present()
    button, rt = exp.keyboard.wait(misc.constants.K_SPACE)
    error = (button == misc.constants.K_SPACE and digit == 3)
    if error: stimuli.Tone(duration=200, frequency=2000).play()
    exp.data.add([digit, button, rt, int(error)])
    exp.clock.wait(1000 - stimuli.BlankScreen().present() - target.unload())

print(exp.data)
control.end(goodbye_text="Thank you very much...", goodbye_delay=2000)
