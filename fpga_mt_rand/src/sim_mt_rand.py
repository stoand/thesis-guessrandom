# #SPC-fpga_mt_rand.tst-simulate
from nmigen.back.pysim import Simulator, Delay, Tick
from mt_rand import MersenneTwister, MT_SCAN_DEPTH, MT_SKIP
from nmigen.test.utils import FHDLTestCase

seed = 500

twist_inputs = [500, 33, 7]
twist_expected = 2567483688

state0_expected = [500, 4273494341, 527150752]
state0_skipped_expected = [4115431134, 1797084095, 1721022853]
state1_expected = [1394139811, 615023855, 3652963275]
output_expected = [1489665453, 160506331, 132536224]


def test_twist(self):
    sim = Simulator(self.mt)

    def process():
        for index in range(len(twist_inputs)):
            yield self.mt.twist_args[index].eq(twist_inputs[index])
        yield Delay()
        self.assertEqual((yield self.mt.twist_result), twist_expected)

    sim.add_process(process)
    sim.run()


def test_states(self):
    sim = Simulator(self.mt)

    def process():
        yield self.mt.seed.eq(seed)
        yield Tick()
        yield Delay()

        for _ in range(MT_SKIP+1):
            yield Tick()

        print("\nskipped[0]\n", (yield self.mt.state0_skipped[0]))

        for i in range(MT_SCAN_DEPTH):
            actual_state0 = yield self.mt.state0[i]
            self.assertEqual(actual_state0, state0_expected[i])

            actual_state0_skipped = yield self.mt.state0_skipped[i]
            self.assertEqual(actual_state0_skipped, state0_skipped_expected[i])

            actual_state1 = yield self.mt.state1[i]
            self.assertEqual(actual_state1, state1_expected[i])
            
            actual_output = yield self.mt.output[i]
            self.assertEqual(actual_output, output_expected[i])

    sim.add_clock(1e-6)
    sim.add_process(process)
    sim.run()


class MersenneTwisterTest(FHDLTestCase):
    def setUp(self):
        self.mt = MersenneTwister()

    test_0 = test_twist
    test_1 = test_states
