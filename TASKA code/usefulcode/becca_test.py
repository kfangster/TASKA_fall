


#imports 
import time
from Positional import Positional 



# define objects 
hand = Positional() 




# test script 
cont = True
while(cont):
    hand.test_command('pronate')
    time.sleep(2)
    hand.test_command('rest')



