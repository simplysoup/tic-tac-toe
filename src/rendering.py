import os
from IPython.display import clear_output
import platform

def clear():
    if platform.system() in ['Linux', 'Darwin']:
        os.system('clear')
    elif platform.system() == 'Windows':
        os.system('cls')

    for i in range(10):
        clear_output(wait=True)