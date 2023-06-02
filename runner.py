from tinyben import TinyBen
import logging

FORMAT='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s  - %(message)s'
logging.basicConfig(
    level=logging.DEBUG, format=FORMAT
)

tb = TinyBen(benchmarks=["fake_success", "fake_failure","linux","imagemagick","godot"])
tb.run()
tb.print_results()