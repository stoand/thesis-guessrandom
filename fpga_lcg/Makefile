# Makefile borrowed from https://github.com/cliffordwolf/icestorm/blob/master/examples/icestick/Makefile
#
# The following license is from the icestorm project and specifically applies to this file only:
#
#  Permission to use, copy, modify, and/or distribute this software for any
#  purpose with or without fee is hereby granted, provided that the above
#  copyright notice and this permission notice appear in all copies.
#
#  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

PIN_DEF = pins.pcf
DEVICE = lp8k
BUILD = build

$(BUILD)/%.json: src/%.v
	mkdir -p $(BUILD)
	yosys -Q -qq -l $(basename $@).log -p 'synth_ice40 -top $(basename $(@F)) -json $@' $<

$(BUILD)/%.asc: $(BUILD)/%.json src/$(PIN_DEF)
	nextpnr-ice40 --lp8k --package cm81 --json $< --pcf src/$(PIN_DEF) --asc $@ --ignore-loops

%.gui: $(BUILD)/%.json src/$(PIN_DEF)
	nextpnr-ice40 --lp8k --package cm81 --json $< --pcf src/$(PIN_DEF) --asc $@ --gui

$(BUILD)/%.bin: $(BUILD)/%.asc
	icepack $< $@

$(BUILD)/%.rpt: $(BUILD)/%.asc
	icetime -d $(DEVICE) -mtr $@ $<
	
%.prog: $(BUILD)/%.bin
	tinyprog -p $<

%.prog-wsl2: $(BUILD)/%.bin
	powershell.exe -Command "tinyprog -p $<"

%.sim:
	sby -d build/$(basename $@) -f $(basename $@).sby
	
%.sim-watch:
	nodemon -e v,sby --ignore build -x "make $(basename $@).sim || echo"

clean:
	rm build -rf

.SECONDARY:
.PHONY: clean
