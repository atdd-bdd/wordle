class Log:

    log = None

    def __init__(self, log_filename="log.txt"):
        Log.log = open(log_filename, "w")

    @staticmethod
    def write(message):
        if Log.log is None:
            Log.log = open("log.txt", "w")
        Log.log.write(message + "\n")

    @staticmethod
    def close():
        Log.log.close()


class Trace:

    trace = None

    def __init__(self, log_filename="trace.txt"):
        print("Opening ", log_filename)
        if Trace.trace is None:
            Trace.trace = open(log_filename, "w")

    @staticmethod
    def write(message):
        if Trace.trace is None:
            Trace.trace = open("trace.txt", "w")
            print("Opening trace.txt since it is not open ")
        Trace.trace.write(message + "\n")

    @staticmethod
    def close():
        Trace.trace.close()
        print("Closing trace file")
