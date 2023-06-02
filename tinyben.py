"""
this module contains the TinyBen class that collect all benchmarks and runs them
"""

import importlib
from rich.console import Console
from rich.table import Table
from rich import box
from base import TBBenchmarkBase


class TinyBenResult:
    """this is the class that implements benchmark results"""

    _test_fullname = ""
    _test_shortname = ""
    _test_result = ""
    _test_status = ""

    def __init__(self, test_fullname, test_shortname, test_result, test_status):
        self._test_fullname = test_fullname
        self._test_shortname = test_shortname
        self._test_result = test_result
        self._test_status = test_status

    def set_test_result(self, value):
        """set the test result"""
        self._test_result = value

    def get_test_result(self):
        """get the benchmark result"""
        return self._test_result

    def set_test_status(self, value):
        """set benchmark status"""
        self._test_status = value

    def get_test_status(self):
        """get the benchmark status"""
        return self._test_status

    def get_test_fullname(self):
        """get benchmark fullname"""
        return self._test_fullname


class TinyBen:
    """the class containing all tests"""

    results = []

    def __init__(self, benchmarks=None):
        if benchmarks is None:
            benchmarks = []
        self.benchmarks = []
        if benchmarks:
            for plugin in benchmarks:
                plugin_to_add = importlib.import_module(
                    f"benchmarks.{plugin}"
                ).TBBenchmark()

                if isinstance(plugin_to_add, TBBenchmarkBase):
                    self.benchmarks.append(plugin_to_add)

    def run(self):
        """run all the benchmarks"""
        for benchmark in self.benchmarks:
            benchmark.run()

    def print_results(self):
        """print a report"""
        console = Console()

        table = Table(
            show_header=True, header_style="bold", box=box.MINIMAL_DOUBLE_HEAD
        )
        table.add_column("Benchmark Name")
        table.add_column("Benchmark Status", justify="center")
        table.add_column("Benchmark Result")

        for result in self.results:
            table.add_row(
                str(result.getTestFullname()),
                str(result.getTestStatus()),
                str(result.getTestResult()),
            )

        console.print(table)
