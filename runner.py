from mqtt_handler import MqttHandler
from process_handler import ProcessHandler

class Runner:
    def __init__(self):
        self.mqtt_handler = MqttHandler()
        self.process_handler = ProcessHandler()

    def cleanup(self):
        self.mqtt_handler.stop()

    def run(self):
        handlers = [self.mqtt_handler.start()]
        self.process_handler.start(handlers, self.cleanup)


if __name__ == "__main__":
    Runner().run()
