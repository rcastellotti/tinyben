from tinyben import TinyBen
import logging
import argparse

parser = argparse.ArgumentParser(prog="tinyben")


parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)

args = parser.parse_args()

FORMAT='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s  - %(message)s'

logging.basicConfig(
    level=logging.DEBUG, format=FORMAT
)

# tb = TinyBen(benchmarks=["fake_success", "fake_failure", "llvm", "linux"])
# tb = TinyBen(benchmarks=["fake_success", "fake_failure","imagemagick","linux"])
# tb = TinyBen(benchmarks=["fake_success", "fake_failure","godot"])
tb = TinyBen(benchmarks=["fake_success", "fake_failure","godot"])


tb.run()
tb.print_results()


