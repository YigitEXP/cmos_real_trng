`timescale 1ns / 1ps

module top_module (
    input wire clk,
    input wire rst,
    output reg random_bit
);

wire osc_signal;

ring_osc u_ring_osc(
    .osc_out(osc_signal)
);

always @(posedge clk) begin
    if(rst) begin
        random_bit <= 1'b0;
    end else begin
        random_bit <= osc_signal;
    end
end

endmodule