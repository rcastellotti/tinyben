import logging
from tinyben import TinyBen

FORMAT = "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s  - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

tb = TinyBen(
    benchmarks=[
        # "fake_success",
        # "fake_failure",
        # "linux",
        # "imagemagick",
        # "godot",
        # "llvm",
        # "tinymembench",
        "sqlite",
    ]
)
tb.run()
tb.print_results()
