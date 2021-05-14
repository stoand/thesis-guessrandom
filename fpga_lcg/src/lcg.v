module lcg(input CLK, output [5:0] counter);
    
    initial
        counter = 33;
    
    always @(posedge CLK) begin
        counter = 33;
    end
endmodule

module testbench(input CLK);
    
    reg [5:0] counter;
    
    lcg lcg0(
        .CLK(CLK),
        .counter(counter)
    );
    
    always @(posedge CLK) begin
        assert (counter == 33); 
    end
endmodule
