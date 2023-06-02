import importlib
from base import TBBenchmark_base
from rich.console import Console
from rich.table import Table
from rich import box


class TinyBenResult:
    _testFullname = ""
    _testShortname = ""
    _testResult = ""
    _testStatus = ""

    def __init__(self, test_fullname, test_shortname, test_result, test_status):
        self._testFullname = test_fullname
        self._testShortname = test_shortname
        self._testResult = test_result
        self._testStatus = test_status

    def set_testResult(self, value):
        self._testResult = value

    def set_testStatus(self, value):
        self._testStatus = value


class TinyBen:
    results = []

    def __init__(self, benchmarks: list = []):
        self.benchmarks = []
        if benchmarks:
            for plugin in benchmarks:
                plugin_to_add = importlib.import_module(
                    f"benchmarks.{plugin}"
                ).TBBenchmark()

                if isinstance(plugin_to_add, TBBenchmark_base):
                    self.benchmarks.append(plugin_to_add)

    def run(self):
        for benchmark in self.benchmarks:
            benchmark.run()

    def print_results(self):
        console = Console()

        table = Table(
            show_header=True, header_style="bold", box=box.MINIMAL_DOUBLE_HEAD
        )
        table.add_column("Benchmark Name")
        table.add_column("Benchmark Status", justify="center")
        table.add_column("Benchmark Result")

        for result in self.results:
            table.add_row(
                str(result._testFullname),
                str(result._testStatus),
                str(result._testResult),
            )

        console.print(table)
