# #SPC-fpga_mt_rand.tst-simulate
from nmigen import *
from nmigen.back.pysim import Simulator, Delay, Settle
from mt_rand import MtRand

class SevenSegController(Elaboratable):
    def __init__(self):
        self.val = Signal(2)
        self.leds = Signal(7)

    def elaborate(self, platform):
        m = Module()

        table = Array([0b0001, 0b10011])

        m.d.comb += self.leds.eq(table[self.val])

        return m

if __name__ == "__main__":
    dut = SevenSegController()
    sim = Simulator(dut)
    
    def process():
        for i in range(2):
            yield dut.val.eq(i)
            yield Delay()
            print((yield dut.leds))
    sim.add_process(process)
    sim.run()

