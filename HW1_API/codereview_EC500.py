#Code Review test case
#EC 500

import os


##################################-------------- TEST 1 --------------#########################################


#VALID username
program1 = 'python testtwitter2.py @Hayatopia'
os.system(program1)

#INVALID username
program2 = 'python testtwitter2.py @hfeahfleajflejaflejlfkejwlafkeja'
os.system(program2)

##################################-------------- TEST 2 --------------#########################################


#This user has no twitter photos
program3 = 'python testtwitter2.py @hellomyname000'
os.system(program3)



##################################-------------- TEST 3 --------------#########################################

#pt a

program4 = 'export GOOGLE_APPLICATION_CREDENTIALS = doesnotexist.json'
os.system(program4)

#pt b

#this will be parsed as the secret consumer key (obviously wrong)
program5 = '777'
os.system('python testtwitter2.py @Hayatopia 777')



