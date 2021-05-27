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
    
    input [31:0] MODULUS, // m
    input [31:0] MULTIPLIER, // a
    input [31:0] INCREMENT, // c
    
    input [31:0] expected_v0,
    input [31:0] expected_v1,
    input [31:0] expected_v2,
    
    output done,
    output [31:0] valid_seed,
);

    reg [31:0] scan_seed = 0;
    reg [31:0] scan_v0;
    reg [31:0] scan_v1;
    reg [31:0] scan_v2;
    
    initial 
        done = 0;
    
    always @(posedge CLK) begin
        // TODO - add the modulus back
        // scan_v0 = ((scan_seed * MULTIPLIER) + INCREMENT) % MODULUS;
        scan_v0 = ((scan_seed * MULTIPLIER) + INCREMENT) - MODULUS *
            ( ((scan_seed * MULTIPLIER) + INCREMENT) / MODULUS);
        scan_v1 = ((scan_v0 * MULTIPLIER) + INCREMENT) % MODULUS;
        scan_v2 = ((scan_v1 * MULTIPLIER) + INCREMENT) % MODULUS;
        
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
    
    reg [31:0] valid_seed;
    
    reg [31:0] counter = 0;
    
    reg [31:0] expected_valid_seed = 96;
    
    lcg_guess lcg_guess0(
        .CLK(CLK),
        
        .MODULUS(993441),
        .MULTIPLIER(4001),
        .INCREMENT(60211),
        
        .done(done),
        .valid_seed(valid_seed),
        
        .expected_v0(444307),
        .expected_v1(466569),
        .expected_v2(127141),
    );
    
    always @(posedge CLK) begin
        // emulate modulus using division and multiplication
        assert(9 - 22 * ( 9 / 22) == 9 % 22);
        
        
        // 100 > 96 so we just scan deep enough
        if(counter == 100) begin
            assert (done == 1); 
            assert (valid_seed == expected_valid_seed); 
        end
        
        counter = counter + 1;
    end
endmodule
`endif
