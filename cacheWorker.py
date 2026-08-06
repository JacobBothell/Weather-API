from queue import Queue


class cacheWorker():
    def __init__(self, cacheQueue: Queue, cacheValidatorQueue: Queue, weatherData: dict, overload_options: dict):
        self.cacheQueue = cacheQueue
        self.cacheValidatorQueue = cacheValidatorQueue
        self.weatherData = weatherData
        self.overload_options = overload_options

    def run(self):
        cacheRequest = self.cacheQueue.get()
        #create key
        #store time weather data

        if 'should_overload' in self.overload_options and self.overload_options['should_overload']:
            print("Overloading cache request for ...")
            if 'depth' in self.overload_options and self.overload_options['depth'] > 0:
                for depth_iter in range(self.overload_options['depth']):
                    pass
