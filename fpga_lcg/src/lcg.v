module lcg (
    input CLK,    // 16MHz clock
    output LED,   // User/boot LED next to power LED
);

    // scans expected rng outputs
    // the led will light up if a valid seed is found
    
    
    reg done;

    lcg_guess lcg_guess0(
        .CLK(CLK),
        
        .done(done),
                
        .MODULUS(993441),
        .MULTIPLIER(4001),
        .INCREMENT(60211),
        
        .done(done),
        // .valid_seed(valid_seed),
        
        // check if the fpga is doing real calculations by 
        // setting a wrong sequence value and ensuring the light stays off
        
        // .expected_v0(0),
        .expected_v0(444307),
        .expected_v1(1777732518),
        .expected_v2(242022553),
        
    );
    
    assign LED = done;

endmodule

module lcg_guess(
    input CLK,
    
    input [`SIZE:0] MODULUS, // m
    input [`SIZE:0] MULTIPLIER, // a
    input [`SIZE:0] INCREMENT, // c
    
    input [`SIZE:0] expected_v0,
    input [`SIZE:0] expected_v1,
    input [`SIZE:0] expected_v2,
    
    output done,
    output [`SIZE:0] valid_seed,
);

    reg [`SIZE:0] scan_seed = 0;
    reg [`SIZE:0] scan_v0;
    reg [`SIZE:0] scan_v1;
    reg [`SIZE:0] scan_v2;
    
    initial 
        done = 0;
    
    always @(posedge CLK) begin
        // TODO - add the modulus back
        // scan_v0 = ((scan_seed * MULTIPLIER) + INCREMENT) % MODULUS;
        
        // Modulus emulation - too expensive to synthesize
        // scan_v0 = ((scan_seed * MULTIPLIER) + INCREMENT) - MODULUS *
        // ( ((scan_seed * MULTIPLIER) + INCREMENT) / MODULUS);
        
        scan_v0 = ((scan_seed * MULTIPLIER) + INCREMENT);
        scan_v1 = ((scan_v0 * MULTIPLIER) + INCREMENT);
        scan_v2 = ((scan_v1 * MULTIPLIER) + INCREMENT);
        
        if (expected_v0 == scan_v0 &&
            expected_v1 == scan_v1 &&
            expected_v2 == scan_v2) begin
            
            done = 1;
            valid_seed = scan_seed;
        end
        
        scan_seed = scan_seed + 1;
    end
endmodule

`ifdef FORMAL
module testbench(input CLK);
    
    reg done;
    
    reg [`SIZE:0] valid_seed;
    
    reg [`SIZE:0] counter = 0;
    
    reg [`SIZE:0] expected_valid_seed = 96;
    
    lcg_guess lcg_guess0(
        .CLK(CLK),
        
        .MODULUS(993441),
        .MULTIPLIER(4001),
        .INCREMENT(60211),
        
        .done(done),
        .valid_seed(valid_seed),
        
        .expected_v0(444307),
        .expected_v1(1777732518),
        .expected_v2(242022553),
    );
    
    always @(posedge CLK) begin
        
        // 100 > 96 so we just scan deep enough
        if(counter == 100) begin
            assert (done == 1); 
            assert (valid_seed == expected_valid_seed); 
        end
        
        counter = counter + 1;
    end
endmodule
`endif
