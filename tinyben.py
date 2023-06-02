import importlib
from base import tb_benchmark_base
from rich.console import Console
from rich.table import Table
from rich import box


class TinyBenResult:
    testFullname = ""
    testShortname = ""
    testResult = ""
    testStatus = ""

    def __init__(self, test_fullname, test_shortname, test_result, test_status):
        self.testFullname = test_fullname
        self.testShortname = test_shortname
        self.testResult = test_result
        self.testStatus = test_status


class TinyBen:
    results = []

    def __init__(self, benchmarks: list = []):
        self.benchmarks = []
        if benchmarks:
            for plugin in benchmarks:
                plugin_to_add = importlib.import_module(
                    f"benchmarks.{plugin}"
                ).tb_benchmark()

                if isinstance(plugin_to_add, tb_benchmark_base):
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
                str(result.testFullname),
                str(result.testStatus),
                str(result.testResult),
            )

        console.print(table)



# benchmarkresult should have a meaningful placeholder in the event something fails
