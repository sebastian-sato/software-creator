raise Exception("Do not run this file directly! do 'python3 ./run.py'") #!REMOVE
#!INCLUDE ./CONFIG.py
#!INCLUDE ./modules/depend.py
#!INCLUDE ./modules/constants.py
#!INCLUDE ./modules/utilities.py
#!INCLUDE ./modules/shell.py
#!INCLUDE ./modules/llm_client.py
#!INCLUDE ./modules/construct_prompt.py
#!INCLUDE ./modules/actions.py

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