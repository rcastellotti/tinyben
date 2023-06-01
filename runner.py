from tinyben import Bot
import logging

logging.basicConfig(level=logging.INFO)
bot = Bot(benchmarks=["llvm"])
bot.run()