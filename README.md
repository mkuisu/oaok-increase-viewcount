# OAOK view count boost
![Alt Text](views.gif)
# View count boost
Want your models at [OAOK](https://oaok.ru/) to have the most amount of views? Or want to become a philanthropist and help other users? Then I'm introducing to you, view count boost script!
# How to install
1. Install [Python 3](https://www.python.org/downloads/) (3.10+ version is necessary). During installation, check the option `"Add to PATH"`.
2. Download repository.
3. Install the libraries required by the program using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/). You can see list of needed libraries in `requirement.txt` file.
4. Open `oaok_main.py` file (cmd, IDE or anything else). 
5. Follow the instructions.
# Working with the program
There is 2 working modes in the program:\
`Gathering links for all models, in all categories and then randomly view them.`\
`Provide links to models in which you want to increase the number of views.`\
Then you're defining delay (in seconds), between viewing models. Delay is created so that server won't ban you for creating too many requests per amount of time.\
Depending on the chosen working mode, you'll either define another delay (between rechecking model links) or you're gonna insert links in text file. Another delay (in minutes) is created to include newly uploaded models in text file. About inserting links in text file there's not much to say, you are inserting links inside text file. Remember that each line should include only 1 link.\
After all settings are applied, program will start working!
# Possible questions
Q: I want to increase views faster, is it possible to have multiple instances of script running?\
A: *Yes, create separate folder for each instance of script and run it how you usually run it. Possibly later, I'll create more seamless process to work with multiple scripts.*\
Q: Compatible with Linux/Mac?\
A: *In theory everything's possible, I think it should work just fine.*\
Q: Program is not working as intended, help!\
A: *Create issue in the repository, I'll eventually check it!*\
Q: I want contribute to the project.\
A: *Honestly, I don't know anything about how this works, I'm not setting any rules about pull requests. If you really want to contribute: pull and we'll decide from then on how to proceed. If someone reads this, please help me with translation of the program to other languages. I don't know how to work with language packs or libraries.*
