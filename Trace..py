class Trace:

    log = None

    def __init__(self, log_filename="trace.txt"):
        Trace.log = open(log_filename, "w")

    @staticmethod
    def write(message):
        if Trace.log is None:
            Trace.log = open("trace.txt", "w")
        Trace.log.write(message + "\n")

    @staticmethod
    def close():
        Trace.log.close()
