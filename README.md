# software-creator
Basic implementation of an LLM client that can scaffold simple software projects.

I wanted to try implementing something like those "agentic" software development tools. Compared to those, the capabilities of this are pretty limited, and I mostly wrote this as a proof of concept.

# Usage:
This doesn't contain code for actually running the LLM, just a client for connecting to an HTTP server running one, using the same format as my "Distributed LLM Server" project.

**CONFIG.py** is where the information for connecting to the server is specified.

Install dependencies:
```
pip3 install requests
```

To run the project, simply do:
```
python3 ./run.py
```

You will be prompted to assign a task to the LLM, and the LLM will attempt to generate the specified software project in the same directory.

# TODO:
- Fix errors resulting from the model producing incorrectly formatted JSONC, maybe by using a custom, simpler format.
- Allow the system to debug code and fix errors on its own
