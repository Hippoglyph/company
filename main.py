from dotenv import load_dotenv

load_dotenv(override=True)
#from workflow import run

#run()

from enviroment.terminal import Terminal

terminal = Terminal("test_name")

print(terminal.write_file("folder/tmp/script.py", "print('hello world')"))
print(terminal.bash("python folder/tmp/script.py"))

terminal.close()