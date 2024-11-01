from dotenv import load_dotenv

load_dotenv(override=True)
#from workflow import run

#run()

from enviroment.terminal import Terminal

terminal = Terminal("test_name")

terminal.bash('echo "print(\'hello world\')" > script.py')
terminal.bash("python script.py")

terminal.close()