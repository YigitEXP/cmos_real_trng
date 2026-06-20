`timescale 1ns / 1ps

module cmos_not(
    output wire out,
    input wire in
);

assign #1 out = ~in;

endmodule