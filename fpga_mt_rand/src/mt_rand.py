# #SPC-fpga_mt_rand
import itertools

from nmigen import Elaboratable, Module, Signal, Cat, Const, Array, unsigned, Mux
from nmigen.build import ResourceError
from tinyfpga_bx import TinyFPGABXPlatformCustomFreq

__all__ = ["MtRand", "MersenneTwister"]

speed = 16

MT_SCAN_DEPTH = 3
MT_SKIP = 397
UINT_SIZE = 32

WORKER_COUNT = pow(2, 5)


def twist(m, u, v):
    op0 = u & 0x80000000
    op1 = v & 0x7FFFFFFF
    op2 = op0 | op1
    op3 = op2 >> 1
    op4 = m ^ op3
    op5 = Mux(v & 1, 0xFFFFFFFF, 0)
    op6 = op5 & 0x9908B0DF
    op7 = op4 ^ op6

    return op7


def init_next(prev, index):
    op0 = prev >> 30
    op1 = prev ^ op0
    op2 = 1812433253 * op1
    op3 = op2 + index
    return op3 & 0xffffffff


def final_processing(state):
    state = state ^ (state >> 11)
    state = state ^ (state << 7) & 0x9d2c5680
    state = state ^ (state << 15) & 0xefc60000
    state = state ^ (state >> 18)
    return state >> 1


class MersenneTwister(Elaboratable):
    def __init__(self):
        self.seed = Signal(UINT_SIZE)

        self.twist_args = Array([Signal(UINT_SIZE) for _ in range(3)])
        self.twist_result = Signal(UINT_SIZE)

        self.state0 = Array([Signal(unsigned(UINT_SIZE))
                            for _ in range(MT_SCAN_DEPTH + MT_SKIP)])
        self.state1 = Array([Signal(unsigned(UINT_SIZE))
                            for _ in range(MT_SCAN_DEPTH)])

        self.output = Array([Signal(unsigned(UINT_SIZE))
                             for _ in range(MT_SCAN_DEPTH)])

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.twist_result.eq(
            twist(
                self.twist_args[0],
                self.twist_args[1],
                self.twist_args[2]))

        m.d.comb += self.state0[0].eq(self.seed & 0xffffffff)

        for index in range(1, len(self.state0)):
            m.d.comb += self.state0[index].eq(
                init_next(self.state0[index - 1], index))

        for index in range(len(self.state1)):
            m.d.comb += self.state1[index].eq(
                twist(self.state0[index + MT_SKIP],
                      self.state0[index], self.state0[index + 1]))

        for index in range(MT_SCAN_DEPTH):
            m.d.comb += self.output[index].eq(
                final_processing(self.state1[index]))

        return m


class MtRand(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        mersenne_twister = MersenneTwister()
        m.submodules += mersenne_twister

        def get_all_resources(name):
            resources = []
            for number in itertools.count():
                try:
                    resources.append(platform.request(name, number))
                except ResourceError:
                    break
            return resources

        leds = [res.o for res in get_all_resources("led")]
        buttons = [res.i for res in get_all_resources("button")]
        switches = [res.i for res in get_all_resources("switch")]

        inverts = [0 for _ in leds]
        for index, button in zip(itertools.cycle(range(len(inverts))), buttons):
            inverts[index] ^= button
        for index, switch in zip(itertools.cycle(range(len(inverts))), switches):
            inverts[index] ^= switch

        # state = Array([Signal(unsigned(UINT_SIZE)) for _ in range(MT_SCAN_DEPTH)])

        clk_freq = platform.default_clk_frequency
        timer = Signal(range(int(clk_freq//speed)),
                       reset=int(clk_freq//speed) - 1)
        flops = Signal(len(leds))

        print("freq:", (clk_freq))

        is_zero = Signal()

        m.d.comb += is_zero.eq(timer == 0)
        m.d.comb += Cat(leds).eq(flops)

        secret_bitsize = 32

        workers = WORKER_COUNT
        print("workers:", workers)

        scan_iter = Signal(range(pow(2, 32)), reset=pow(2, 32) - 1)
        scan_result = Signal(range(pow(2, 32)))

        found_secret = Signal(range(1), reset=0)
        started = Signal(range(1), reset=0)
        
        output_expected = [104635876, 1716423271, 620858268]

        with m.If(found_secret == 0):
            with m.If((scan_iter != scan_iter.reset) | (started == 0)):
                m.d.sync += started.eq(Const(1))
                for w in range(workers):
                    m.d.sync += mersenne_twister.seed.eq(scan_iter+w)
                    output = mersenne_twister.output
                    
                    with m.If((output[0] == output_expected[0]) &
                              (output[1] == output_expected[1]) &
                              (output[2] == output_expected[2])):
                        # Exit
                        m.d.sync += scan_result.eq(scan_iter+w)
                        m.d.sync += scan_iter.eq(scan_iter.reset)
                        m.d.sync += found_secret.eq(Const(1))
                m.d.sync += scan_iter.eq(scan_iter - workers)
        with m.Else():
            display_bit = Signal(range(secret_bitsize), reset=0)
            secret_bits = Array([scan_result[i]
                                for i in range(secret_bitsize)])
            # display secret in binary by blinking
            with m.If(is_zero):
                m.d.sync += timer.eq(timer.reset)
                m.d.sync += flops.eq(secret_bits[display_bit])
                # m.d.sync += flops.eq(~flops)
                m.d.sync += display_bit.eq(display_bit + 1)
            with m.Else():
                m.d.sync += timer.eq(timer - 1)

        return m


if __name__ == "__main__":
    TinyFPGABXPlatformCustomFreq().build(MtRand(), do_program=True)
