import logging


class TBBenchmark_base:
    results = {}
    """base class for TBBenchmarks"""

    def pre(self):
        raise NotImplementedError

    def run_benchmark(self):
        raise NotImplementedError

    def run(self):
        logging.debug("start running pre <BENCHMARK NAME>")
        self.pre()
        logging.debug("completed pre <BENCHMARK NAME>")

        logging.debug("start running benchmark <BENCHMARK NAME>")
        self.run_benchmark()
        logging.debug("completed benchmark <BENCHMARK NAME>")

        logging.debug("start running post <BENCHMARK NAME>")
        self.post()
        logging.debug("completed post <BENCHMARK NAME>")

    def post(self):
        raise NotImplementedError
