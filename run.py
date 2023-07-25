import tinyben.benchmarks.godot as godot
import tinyben.benchmarks.imagemagick as im
import tinyben.benchmarks.linux as linux
import tinyben.benchmarks.llvm as llvm
import tinyben.benchmarks.lz4 as lz4
import tinyben.benchmarks.mbw as mbw
import tinyben.benchmarks.redis as redis
import tinyben.benchmarks.sqlite as sqlite
import tinyben.benchmarks.tinymembench as tmb

sqlite.main()
redis.main()
llvm.main()
linux.main()
tmb.main()
mbw.main()
godot.main()
im.main()
lz4.main()
