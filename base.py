"""
This module contains the base TBBenchmark class benchmarks extends
"""
import logging
import abc


class TBBenchmarkBase(metaclass=abc.ABCMeta):
    """base TBBenchmark class benchmarks extends"""

    results = {}
    """base class for TBBenchmarks"""

    @abc.abstractmethod
    def pre(self):
        """method to setup the benchmark"""
        raise NotImplementedError

    @abc.abstractmethod
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

    @abc.abstractmethod
    def post(self):
        """method to cleanup the benchmark"""
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "pre")
            and callable(subclass.pre)
            and hasattr(subclass, "post")
            and callable(subclass.post)
            and hasattr(subclass, "run_benchmark")
            and callable(subclass.run_benchmark)
            or NotImplemented
        )
