"""
This module contains the base TBBenchmark class benchmarks extends
"""
import logging


class TBBenchmarkBase:
    """base TBBenchmark class benchmarks extends"""

    results = {}
    """base class for TBBenchmarks"""

    def pre(self):
        """method to setup the benchmark"""
        raise NotImplementedError

    def run_benchmark(self):
        """method that actually runs the benchmark"""
        raise NotImplementedError

    def run(self):
        """method introduced to add logging and call `pre` and `post` methods"""
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
        """method to cleanup the benchmark"""
        raise NotImplementedError
