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

    _benchmark_fullname = ""
    _benchmark_shortname = ""
    _benchmark_result = ""
    _benchmark_status = ""

    def __init__(
        self,
        benchmark_fullname,
        benchmark_shortname,
        benchmark_result,
        benchmark_status,
    ):
        self._benchmark_fullname = benchmark_fullname
        self._benchmark_shortname = benchmark_shortname
        self._benchmark_result = benchmark_result
        self._benchmark_status = benchmark_status

    def set_benchmark_result(self, value):
        """set the benchmark result"""
        self._benchmark_result = value

    def get_benchmark_result(self):
        """get the benchmark result"""
        return self._benchmark_result

    def set_benchmark_status(self, value):
        """set benchmark status"""
        self._benchmark_status = value

    def get_benchmark_status(self):
        """get the benchmark status"""
        return self._benchmark_status

    def get_benchmark_fullname(self):
        """get benchmark fullname"""
        return self._benchmark_fullname


class TinyBen:
    """the class containing all benchmarks"""

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
                str(result.getbenchmarkFullname()),
                str(result.getbenchmarkStatus()),
                str(result.getbenchmarkResult()),
            )

        console.print(table)
