module lcg(
    input CLK,
    
    input [31:0] MODULUS, // m
    input [31:0] MULTIPLIER, // a
    input [31:0] INCREMENT, // c
    
    input [31:0] value, // X
    
    output [31:0] next_value,
);
    
    
    always @(posedge CLK) begin
        next_value = ((value * MULTIPLIER) + INCREMENT) % MODULUS;
    end
endmodule

module testbench(input CLK);
    
    reg [31:0] counter = 0;
    
    // initial seed
    reg [31:0] value;
    reg [31:0] next_value;
    
    initial 
        value = 96;
    
    lcg lcg0(
        .CLK(CLK),
        
        .MODULUS(993441),
        .MULTIPLIER(4001),
        .INCREMENT(60211),
        
        .value(value),
        .next_value(next_value),
    );
    
    always @(posedge CLK) begin
        
        if(counter == 1) begin
            assert (next_value == 444307); 
        end
        
        if(counter == 2) begin
            // assert (next_value == 466569); 
        end
        
        counter = counter + 1;
        value = next_value;
    end
endmodule
