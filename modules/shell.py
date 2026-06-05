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