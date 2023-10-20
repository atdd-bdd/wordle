from config import Configuration


class Log:
    log = None
    opened = False

    def __init__(self, log_filename="log.txt"):
        Log.check_for_open(log_filename)

    @staticmethod
    def write(message):
        if Configuration.log_output:
            Log.check_for_open()
            Log.log.write(message + "\n")

    @staticmethod
    def check_for_open(log_filename="log.txt"):
        if Log.log is None:
            if not Log.opened:
                Log.log = open(log_filename, "w")
                Log.opened = True
            else:
                Log.log = open(log_filename, "a")

    @staticmethod
    def close():
        Log.log.close()
        Log.log = None


class Trace:
    trace = None
    opened = False

    def __init__(self, trace_filename="trace.txt"):
        print("Opening ", trace_filename)
        Trace.check_for_open(trace_filename)

    @staticmethod
    def write(message):
        if Configuration.trace_output:
            Trace.check_for_open()
            Trace.trace.write(message + "\n")

    @staticmethod
    def check_for_open(trace_filename="trace.txt"):
        if Trace.trace is None:
            if not Trace.opened:
                Trace.trace = open(trace_filename, "w")
                Trace.opened = True
            else:
                Trace.trace = open(trace_filename, "a")

    @staticmethod
    def close():
        Trace.trace.close()
        Trace.trace = None
        print("Closing trace file")


class ResultLog:
    @staticmethod
    def write(message):
        log = open("game_results.txt", "a")
        log.write(message + "\n")
        log.close()
