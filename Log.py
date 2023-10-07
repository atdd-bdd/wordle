class Log:

    log = None

    def __init__(self, log_filename="log.txt"):
        Log.log = open(log_filename, "w")
    @staticmethod
    def write(message):
        Log.log.write(message + "\n")

    @staticmethod
    def __del__(self):
        Log.log.close()



