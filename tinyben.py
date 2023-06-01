import importlib
from base import tb_benchmark_base


class tinyben:
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



# implement pre, post (if needed)