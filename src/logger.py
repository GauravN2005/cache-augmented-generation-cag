import datetime

class Logger:
    def __init__(self, logfile="log.txt"):
        self.logfile = logfile

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        text = timestamp + message

        print(text)  # print to console for demo

        with open(self.logfile, "a", encoding="utf-8") as f:
            f.write(text + "\n")
