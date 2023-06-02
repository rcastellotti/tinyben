from tinyben import TinyBen
import logging

logging.basicConfig(level=logging.INFO)
tb = TinyBen(benchmarks=["llvm", "linux"])
tb.run()
tb.print_results()
