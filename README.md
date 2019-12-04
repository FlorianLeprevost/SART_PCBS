# SART task + data analysis
What I want to do is
I) first to program in python (1) the SART task (2) with several levels of difficulty (3) with probe apparition depending on the last reaction times

II) Then I want to program in R (1) the data analysis I'm going to do, ideally in a Rmarkdown document. (I'm not yet sure about how I'm going to go with this)

# 1) SART Task
## 1.1) Basic SART Task
The Sustained Attention to Response Task (SART) is a go/no-go task, which demand sustained but very little attention. It is often used combined with "thought probes" as a paradigm to investigate Mind Wandering. Indeed, as the task is long and boring, you are more likely to think of something else, and "wander" in/with your mind. The "thought probes" are sudden interruption of the task accompanied by a question that inquires about the participant's thoughts. See [REF](http) for a review of probes.

I coded the SART task using the information from the [following site](https://scienceofbehaviorchange.org/measures/sustained-attention-to-response-task/).

What I had to do
- [x] create a list of numbers to display
- [x] make sure I have the right number of no-go trials
- [x] make sure my no-go trials aren't too close from each other
- [x] make sure the ISI stayed at 1150ms even when subject answered early
- [x] random character size display between 5 possible

## 1.2) Difficulty levels
## 1.3) Probes
I used the [Seli 2016 article](https://doi.org/10.1016/j.concog.2016.02.002) to determine the probe rate.

What I had to do
- [ ] create a different file to get probe data
- [ ] set the probes to appear randomly during sub-blocks of 45 trials (and not to close to the begining and end of block)
