class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self, result):
        for step in self.steps:
            result = step.process(result)
        return result