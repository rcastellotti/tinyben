class tb_benchmark_base:
    # here we can have an empty dictionary that stores results
    results = {}
    """base class for tb_benchmarks"""

    def pre(self):
        pass

    def run(self):
        pass

    def post(self):
        # cleanup??
        pass
