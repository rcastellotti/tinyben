from tinyben import tinyben
import logging

logging.basicConfig(level=logging.INFO)
bot = tinyben(benchmarks=["llvm", "linux"])
bot.run()
