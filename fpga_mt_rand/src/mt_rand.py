import itertools

from nmigen import Elaboratable, Module, Signal, Cat, Const, Array
from nmigen.build import ResourceError
from nmigen_boards.tinyfpga_bx import TinyFPGABXPlatform

__all__ = ["MtRand"]

speed = 16


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

        clk_freq = platform.default_clk_frequency
        timer = Signal(range(int(clk_freq//speed)),
                       reset=int(clk_freq//speed) - 1)
        flops = Signal(len(leds))
        print("freq:", (clk_freq))

        is_zero = Signal()

        m.d.comb += is_zero.eq(timer == 0)
        m.d.comb += Cat(leds).eq(flops)

        secret_bitsize = 32
        secret_range = pow(2, secret_bitsize)

        secret = Const(1, range(secret_range))

        workers = pow(2, 5)
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
    TinyFPGABXPlatform().build(MtRand(), do_program=True)
