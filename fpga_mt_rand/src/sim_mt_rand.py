# #SPC-fpga_mt_rand.tst-simulate
from nmigen.back.pysim import Simulator, Delay
from mt_rand import MersenneTwister, MT_SCAN_DEPTH

if __name__ == "__main__":
    mt = MersenneTwister()
    sim = Simulator(mt)

    def process():
        yield mt.seed.eq(500)
        for i in range(MT_SCAN_DEPTH):
            yield Delay()
            print((yield mt.outputs[i]))

    sim.add_process(process)
    sim.run()
