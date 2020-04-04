# #SPC-fpga_mt_rand
import itertools

from nmigen import Elaboratable, Module, Signal, Cat, Const, Array, unsigned
from nmigen.build import ResourceError
from tinyfpga_bx import TinyFPGABXPlatformCustomFreq

__all__ = ["MtRand", "MersenneTwister"]

speed = 16

MT_SCAN_DEPTH = 3
UINT_SIZE = 32


# define loBit(u)      ((u) & 0x00000001U)  /* mask all but lowest    bit of u */
# define twist(m,u,v)  (m ^ (mixBits(u,v)>>1) ^ ((uint32_t)(-(int32_t)(loBit(v))) & 0x9908b0dfU))
def twist(m, u, v):
    return 0


class MersenneTwister(Elaboratable):
    def __init__(self):
        self.seed = Signal(UINT_SIZE)

        self.state0 = Array([Signal(unsigned(UINT_SIZE))
                            for _ in range(MT_SCAN_DEPTH)])

        self.state1 = Array([Signal(unsigned(UINT_SIZE))
                            for _ in range(MT_SCAN_DEPTH)])

        self.outputs = Array([Signal(unsigned(UINT_SIZE))
                             for _ in range(MT_SCAN_DEPTH)])

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.state0[0].eq(self.seed & 0xffffffff)

        for index in range(1, MT_SCAN_DEPTH):
            prev = self.state0[index - 1]

            op0 = prev >> 30
            op1 = prev ^ op0
            op2 = 1812433253 * op1
            op3 = op2 + index
            op4 = op3 & 0xffffffff

            m.d.comb += self.state0[index].eq(op4)

        for index in range(1, MT_SCAN_DEPTH):
            print()

        for index in range(MT_SCAN_DEPTH):
            m.d.comb += self.outputs[index].eq(self.state1[index])

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

        leds = [res.o for res in get_all_resources("led")]
        buttons = [res.i for res in get_all_resources("button")]
        switches = [res.i for res in get_all_resources("switch")]

        inverts = [0 for _ in leds]
        for index, button in zip(itertools.cycle(range(len(inverts))), buttons):
            inverts[index] ^= button
        for index, switch in zip(itertools.cycle(range(len(inverts))), switches):
            inverts[index] ^= switch

        state = Array([Signal(unsigned(UINT_SIZE)) for _ in range(MT_COUNT)])

        clk_freq = platform.default_clk_frequency
        timer = Signal(range(int(clk_freq//speed)),
                       reset=int(clk_freq//speed) - 1)
        flops = Signal(len(leds))

        m.d.sync += flops.eq(state[0])

        print("freq:", (clk_freq))

        is_zero = Signal()

        m.d.comb += is_zero.eq(timer == 0)
        m.d.comb += Cat(leds).eq(flops)

        secret_bitsize = 32
        secret_range = pow(2, secret_bitsize)

        secret = Const(1, range(secret_range))

        workers = pow(2, 7)
        print("workers:", workers)

        scan_iter = Signal(range(pow(2, 32)), reset=pow(2, 32) - 1)
        scan_result = Signal(range(pow(2, 32)))

        found_secret = Signal(range(1), reset=0)
        started = Signal(range(1), reset=0)

        with m.If(found_secret == 0):
            with m.If((scan_iter != scan_iter.reset) | (started == 0)):
                m.d.sync += started.eq(Const(1))
                # guess secret
                for w in range(workers):
                    with m.If((scan_iter+w)[:secret_bitsize] == secret):
                        # Exit
                        m.d.sync += scan_result.eq((scan_iter+w)
                                                   [:secret_bitsize])
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
