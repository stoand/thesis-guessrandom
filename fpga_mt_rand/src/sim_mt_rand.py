# #SPC-fpga_mt_rand.tst-simulate
from nmigen.back.pysim import Simulator, Delay
from mt_rand import MersenneTwister


if __name__ == "__main__":
    dut = MersenneTwister()
    sim = Simulator(dut)

    def process():
        for i in range(2):
            yield dut.input.eq(i)
            yield Delay()
            print((yield dut.output))
    sim.add_process(process)
    sim.run()
