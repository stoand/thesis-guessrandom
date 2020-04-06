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

WORKER_COUNT = 2


def trunc(v):
    return v[:UINT_SIZE]


def twist(m, u, v):
    op0 = trunc(u & 0x80000000)
    op1 = trunc(v & 0x7FFFFFFF)
    op2 = trunc(op0 | op1)
    op3 = trunc(op2 >> 1)
    op4 = trunc(m ^ op3)
    op5 = trunc(Mux(v & 1, 0xFFFFFFFF, 0))
    op6 = trunc(op5 & 0x9908B0DF)
    op7 = trunc(op4 ^ op6)
    return op7


def init_next(prev, index):
    op0 = trunc(prev >> 30)
    op1 = trunc(prev ^ op0)
    op2 = trunc(1812433253 * op1)
    op3 = trunc(op2 + index)
    return op3


def final_processing(state):
    state = trunc(state ^ (state >> 11))
    state = trunc(state ^ (state << 7) & 0x9d2c5680)
    state = trunc(state ^ (state << 15) & 0xefc60000)
    state = trunc(state ^ (state >> 18))
    return state >> 1


class MersenneTwister(Elaboratable):
    def __init__(self):
        self.seed = Signal(UINT_SIZE)

        self.twist_args = Array([Signal(UINT_SIZE) for _ in range(3)])
        self.twist_result = Signal(UINT_SIZE)

        self.state0 = Array([Signal(unsigned(UINT_SIZE))
                            for _ in range(MT_SCAN_DEPTH + 1)])

        self.state0_skipped = Array(
            [Signal(unsigned(UINT_SIZE)) for _ in range(MT_SCAN_DEPTH)])
        self.skipped_calc = Signal(range(MT_SKIP + 1))
        self.skipped_calc_done = Signal(1)

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

        # Set the initial state
        m.d.comb += self.state0[0].eq(self.seed & 0xffffffff)

        # Set following states
        for index in range(1, len(self.state0)):
            m.d.comb += self.state0[index].eq(
                init_next(self.state0[index - 1], index))

        # Set following skipped states
        for index in range(1, len(self.state0_skipped)):
            m.d.comb += self.state0_skipped[index].eq(
                init_next(self.state0_skipped[index - 1], index + MT_SKIP))

        # Calculate the first skipped state
        with m.If(self.skipped_calc_done == 0):
            # Go to next skip index (applied in the next tick)
            m.d.sync += self.skipped_calc.eq(self.skipped_calc + 1)
            with m.If(self.skipped_calc == 0):
                # Initialize the first state
                m.d.sync += self.state0_skipped[0].eq(self.state0[0])
            with m.Else():
                # Get the next state
                m.d.sync += self.state0_skipped[0].eq(
                    init_next(self.state0_skipped[0], self.skipped_calc))
                with m.If(self.skipped_calc == MT_SKIP):
                    # Reached end of skip index
                    m.d.sync += self.skipped_calc_done.eq(1)

        # States after twisting
        for index in range(len(self.state1)):
            m.d.comb += self.state1[index].eq(
                twist(self.state0_skipped[index],
                      self.state0[index], self.state0[index + 1]))

        # Do final processing
        for index in range(MT_SCAN_DEPTH):
            m.d.comb += self.output[index].eq(
                final_processing(self.state1[index]))

        return m


class MtRand(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        def get_all_resources(name):
            resources = []
            for number in itertools.count():
                try:
                    resources.append(platform.request(name, number))
                except ResourceError:
                    break
            return resources

        led = get_all_resources("led")[0].o

        clk_freq = platform.default_clk_frequency
        timer = Signal(range(int(clk_freq//speed)),
                       reset=int(clk_freq//speed) - 1)

        result_bits = Array(Signal(1) for i in range(UINT_SIZE))

        found_secret = Signal(range(1), reset=0)

        output_expected = [1489665453, 160506331, 132536224]

        with m.If(found_secret == 0):
            for worker_index in range(WORKER_COUNT):
                scan_iter = Signal(range(pow(2, 32)), reset=worker_index)
                mersenne_twister = MersenneTwister()
                m.submodules += mersenne_twister

                m.d.comb += mersenne_twister.seed.eq(scan_iter)

                # Will loop indefinitly if no result is found
                with m.If(mersenne_twister.skipped_calc_done == 1):
                    output = mersenne_twister.output
                    with m.If((output[0] == output_expected[0]) &
                              (output[1] == output_expected[1]) &
                              (output[2] == output_expected[2])):
                        m.d.sync += found_secret.eq(1)
                        m.d.sync += Cat(result_bits).eq(scan_iter)
                    with m.Else():
                        m.d.sync += scan_iter.eq(scan_iter + WORKER_COUNT)
                        m.d.sync += mersenne_twister.skipped_calc_done.eq(0)
        with m.Else():
            display_bit = Signal(range(UINT_SIZE), reset=0)
            # display secret in binary by blinking
            with m.If(timer == 0):
                m.d.sync += timer.eq(timer.reset)
                m.d.sync += led.eq(result_bits[display_bit])
                m.d.sync += display_bit.eq(display_bit + 1)
            with m.Else():
                m.d.sync += timer.eq(timer - 1)

        return m


if __name__ == "__main__":
    TinyFPGABXPlatformCustomFreq().build(MtRand(), do_program=True)
