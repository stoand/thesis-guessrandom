module lcg(
    input CLK,
    
    input [31:0] MODULUS, // m
    input [31:0] MULTIPLIER = 4001, // a
    input [31:0] INCREMENT = 60211, // c
    
    input [31:0] value, // X
    
    output [31:0] next_value,
);
    
    
    always @(posedge CLK) begin
        next_value = value + 1;
        // counter = 33;
    end
endmodule

module testbench(input CLK);
    
    reg [5:0] counter = 33;
    
    reg started = 0;
    
    reg [31:0] value = 96;
    reg [31:0] next_value;
    
    lcg lcg0(
        .CLK(CLK),
        
        .MODULUS(993441),
        .MULTIPLIER(4001),
        .INCREMENT(60211),
        
        .value(value),
        .next_value(next_value),
    );
    
    always @(posedge CLK) begin
        
        if(started == 1) begin
            assert (next_value == (value + 1)); 
        end
        
        started = 1;
    end
endmodule
