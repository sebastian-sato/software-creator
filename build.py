# THIS FILE WAS AUTOMATICALLY GENERATED, CHANGES TO IT WILL NOT BE SAVED!

#START OF MODULE: ./CONFIG.py
# Server settings
SERVER_IP: str = "192.168.50.88"
PORT: int = 8000
PASSWORD: str = "GENERICPASSWORD123"
SERVICE_NAME = "llmaccess"

# Agent settings
TASK = input("Task: ")
#END OF MODULE

#START OF MODULE: ./modules/depend.py
import requests
import json
import re
import time
import os
#END OF MODULE

#START OF MODULE: ./modules/constants.py
# Special characters
END_TRANSMISSION: str = "\x04"
SIGINT: str = "\x03"
ESCAPE: str = "\x1b"
UP: str = "\x1b[A"
DOWN: str = "\x1b[B"
RIGHT: str = "\x1b[C"
LEFT: str = "\x1b[D"
#END OF MODULE

#START OF MODULE: ./modules/utilities.py
def if_str_empty_prompt_user(val: str, prompt: str) -> str:
    if val in (None, ""):
        return input(prompt + ": ")
    else:
        return val

def replace_special_characters(text: str) -> str:
    text = text.replace("[SIGINT]", SIGINT)
    text = text.replace("[ESCAPE]", ESCAPE)
    text = text.replace("[END]", END_TRANSMISSION)
    text = text.replace("[UP]", UP)
    text = text.replace("[DOWN]", DOWN)
    text = text.replace("[LEFT]", LEFT)
    text = text.replace("[RIGHT]", RIGHT)
    text = text.replace("[DONE]","")
    text = text.replace("[WAIT]","")
    text = text.replace("`","")
    return text

def between_substr(text: str, a: str, b: str):
    start = text.find(a)
    cut = text[start+len(a):]
    end = cut.find(b)
    cut = cut[:end]
    return cut

def strip_comments(jsonc):
    without_single_line = re.sub(r'(\/\/.*)', '', jsonc) # Remove single line comments
    json = re.sub(r'(\/\**.*\*\/)', '', without_single_line, flags=re.DOTALL) # Remove multi line comments
    return json

def resolve_nonexistent_directories(path):
    folders = path.split("/")[:-1]
    for i in range(len(folders)):
        os.system("mkdir " + "/".join(folders[:i+1]))
#END OF MODULE

#START OF MODULE: ./modules/shell.py
class VirtualShell():
    def __init__(self):
        pid, self.fd = os.forkpty()
        if pid == 0:
            os.execvp("bash", ["bash"])
        self.buffer = b""
    
    def send(self, text: str, DEBUG: bool = True) -> str:
        time.sleep(1)
        os.write(self.fd, text.encode())
        time.sleep(8)
        readin = self.read_buffer()
        if DEBUG:
            self.display_buffer(readin)
        return str(readin)
    
    def read_buffer(self):
        time.sleep(0.25)
        readin = os.read(self.fd, 10_000)
        return readin
    
    def display_buffer(self, buffer): # For debugging and visualization
        #os.system("clear") # TODO: Find a more efficient way to clear the terminal
        os.write(os.open("/dev/tty", os.O_WRONLY),buffer)
#END OF MODULE

#START OF MODULE: ./modules/llm_client.py
URL = f"http://{SERVER_IP}:{PORT}/{SERVICE_NAME}"

def generate(chat: list[dict], max_tokens: int=4000) -> dict:
    return sendAndRecieve(data={"payload":{"messages":chat}}, url=URL, password=PASSWORD, max_tokens=max_tokens)

def sendAndRecieve(data: dict, url: str, password: str, max_tokens: int=500) -> dict: # Apparently you can do static type checking in Python with mypy, neat!
    try:
        data["pass"] = password
        data["max_tokens"] = max_tokens
        return requests.post(url=url, json=data, timeout=60).json()
    except:
        print("Failed to connect to LLM server! Make sure you entered the correct information in config.json, or check your internet connection!")
        raise ConnectionError

#END OF MODULE

#START OF MODULE: ./modules/construct_prompt.py
def construct_prompt(text_prompt: str) -> list[dict[str, str]]:
    return [{"role":"user","content":text_prompt}]
#END OF MODULE

#START OF MODULE: ./modules/actions.py
def bash_impl(action: str) -> str:
    prompt = [
        {"role":"user","content":"Write bash script for: \"" + action + "\", use bash comments '#' for explanation."}
    ]
    return between_substr(generate(prompt)["message"], "```bash", "```").strip()

def create_software_specification(task_is_to: str) -> str:
    prompt = construct_prompt("""You are an AI software developer. Your task is to: '"""+task_is_to+"""'
    
	Your first step is to draft a specification document that defines 1. Every file in the project, 2. Every class in each file and its constructor arguments, 3. Every public method (as in, non-helper methods) in each class.
    
	Generate the specification as computer readable JSONC (JSON with comments), and include comments explaining the purpose of everything, like the following example:
```
// ProjectName
{
	"sourcefile.py": { // Does cool stuff
		"Class1":{ // Does foo
			"inherits":null,
			"__init__":"default constructor", // Accepts no constructor arguments
			"methodOne":{
				"arg1":"int", // foo arguments
				"arg2":"str",
				"returns": "bool"
			},
			"methodTwo":{
				"arg1":"dict",
				"returns": "tuple[int, np.array]"
			},
		},
		"Class2":{ // does bar
			"inherits":"Class1",
			"__init__":{
				"name":"str" // Name to use
			},
			"helloMethod":{
				"returns":"str" // Takes no arguments, outputs "Hello, Name!"
			}
		}
	},
	"sourcefile2.py": {
		"FunClass":{
			"__init__":{
				"fun":"bool" // Defaults to True
			},
			"funMethod":{
				"verySillyArg":"Class2" // Mutates the Name field in Class2!
			}
		}
	}
}
```""")
    return between_substr(generate(prompt)["message"], "```jsonc", "```")

def impl_software_specification(jsonc_text: str) -> dict[str,str]:
	parsed_json: dict = json.loads(strip_comments(jsonc_text))
	files = parsed_json.keys()
	file_impls: dict[str,str] = {}
	for file in files:
		#print(file)
		file_impl = ""
		prompt = construct_prompt("You are an AI software implementer, given the following overall software specification:\n```jsonc" + jsonc_text+"\n```\n\n" + "implement the source code for the file " + file)
		file_impl = '\n'.join(between_substr(generate(prompt)["message"],'```','```').split('\n')[1:]) # Remove the first line specifiying the language the code was written in
		file_impls[file] = file_impl
	return file_impls

#def impl_main(jsonc_text: str) -> tuple[str, str]:
#	prompt = construct_prompt("You are an AI software implementer, given the following overall software specification:\n```jsonc"+jsonc_text+"\n```\n\nYour task is to implement the source code for a file called 'main' that will use the specified files/classes to drive the program. Assume that all the other files will be in the same directory as main. Also specify in a comment at the top of the file what the exact name of the file will be (i.e. The file's name and file extension)")
#	main_impl = '\n'.join(between_substr(generate(prompt)["message"],'```','```').split('\n')[1:])
#	return main_impl, main_impl.split('\n')[0].replace('#','').strip()

def draft_name(task: str) -> str:
	prompt = construct_prompt("Based on the given software requirement: '" + task + "', come up with a name for the top level folder for the project, output only the suggested name and nothing else.") # This could go horribly wrong, but it'd pretty hilarious to see that your project folder was named "Sure, I can do that! heres a suggestion for your top level folders name: SimpleHTTPServer"
	name = generate(prompt)["message"].strip()
	return name
#END OF MODULE


print("Drafting software specification...")
specification = create_software_specification(TASK)
print("Implementing modules...")
modules_source = impl_software_specification(specification)
#print("Implementing driver program...")
#main_source, main_name = impl_main(specification)

print("Writing generated code to disk...")
project_name: str = draft_name(TASK)
os.system("mkdir "+project_name) # TODO: Use path join
for module in modules_source:
    resolve_nonexistent_directories(f"./{project_name}/{module}")
    with open(f"./{project_name}/{module}","w+") as f:
        f.write(modules_source[module])
#with open(f"./{project_name}/{main_name}", "w+") as f:
#    f.write(main_source)
print("Done.")
