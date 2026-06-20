module ring_osc(
    output wire osc_out
);

wire w1, w2, w3;

cmos_not inv1(
    .in(w3),
    .out(w1)
);
cmos_not inv2(
    .in(w1),
    .out(w2)
);
cmos_not inv3(
    .in(w2),
    .out(w3)
);

assign osc_out = w3;

initial begin
    force w3 = 1'b0;
    #5;       
    force w3 = 1'b1; 
    #5;          
    release w3;     
end

endmodule