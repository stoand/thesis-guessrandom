module lcg(
    input CLK,
    
    input [31:0] MODULUS, // m
    input [31:0] MULTIPLIER, // a
    input [31:0] INCREMENT, // c
    
    input [31:0] seed, // X
    
    output [31:0] v0,
    output [31:0] v1,
    output [31:0] v2,
);
    
    always @(posedge CLK) begin
        v0 = ((seed * MULTIPLIER) + INCREMENT) % MODULUS;
        v1 = ((v0 * MULTIPLIER) + INCREMENT) % MODULUS;
        v2 = ((v1 * MULTIPLIER) + INCREMENT) % MODULUS;
    end
endmodule

module testbench(input CLK);
    
    reg [31:0] counter = 0;
    
    reg [31:0] seed;
    
    reg [31:0] v0;
    reg [31:0] v1;
    reg [31:0] v2;
    
    lcg lcg0(
        .CLK(CLK),
        
        .MODULUS(993441),
        .MULTIPLIER(4001),
        .INCREMENT(60211),
        
        .seed(seed),
        .v0(v0),
        .v1(v1),
        .v2(v2),
    );
    
    always @(posedge CLK) begin
        
        if(counter == 2) begin
            assert (v0 == 444307); 
            assert (v1 == 466569); 
            assert (v2 == 127141); 
        end
        
        seed = 96;
        counter = counter + 1;
    end
endmodule
