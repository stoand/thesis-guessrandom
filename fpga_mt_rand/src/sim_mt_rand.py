# #SPC-fpga_mt_rand.tst-simulate
from nmigen import Signal
from nmigen.back.pysim import Simulator, Delay
from mt_rand import MersenneTwister, MT_SCAN_DEPTH
from nmigen.test.utils import FHDLTestCase

seed = 500

twist_inputs = [500, 33, 8]
twist_expected = 2586481474

state0_expected = [500, 4273494341, 527150752]


def test_twist(self):
    sim = Simulator(self.mt)

    def process():
        for index in range(len(twist_inputs)):
            yield self.mt.twist_args[index].eq(twist_inputs[index])
        yield Delay()
        # TODO
        # self.assertEqual((yield self.mt.twist_result), twist_expected)

    sim.add_process(process)
    sim.run()


def test_state0(self):
    sim = Simulator(self.mt)

    def process():
        yield self.mt.seed.eq(seed)
        for i in range(MT_SCAN_DEPTH):
            yield Delay()
            actual = yield self.mt.state0[i]
            self.assertEqual(actual, state0_expected[i])

    sim.add_process(process)
    sim.run()


class MersenneTwisterTest(FHDLTestCase):
    def setUp(self):
        self.mt = MersenneTwister()

    test_0 = test_twist
    test_1 = test_state0


# if __name__ == "__main__":
#     mt = MersenneTwister()
#     sim = Simulator(mt)

#     def process():
#         yield mt.seed.eq(500)
#         for i in range(MT_SCAN_DEPTH):
#             yield Delay()
#             print((yield mt.outputs[i]))

#     sim.add_process(process)
#     sim.run()
