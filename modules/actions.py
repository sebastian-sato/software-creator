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