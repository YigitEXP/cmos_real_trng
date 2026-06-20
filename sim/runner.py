import os
from pathlib import Path
from cocotb_tools.runner import get_runner

def run_sim():
    iverilog_path = r"C:\iverilog\bin" 
    if os.path.exists(iverilog_path):
        os.environ["PATH"] += os.pathsep + iverilog_path
    else:
        alt_path = r"C:\Program Files\iverilog\bin"
        if os.path.exists(alt_path):
            os.environ["PATH"] += os.pathsep + alt_path

    verilog_files = [
        r"C:\Develop\uart_cocotb\src\cmos_not.v",
        r"C:\Develop\uart_cocotb\src\ring_osc.v",
        r"C:\Develop\uart_cocotb\src\top_module.v"
    ]

    for file in verilog_files:
        if not os.path.exists(file):
            print(f"CRITICAL ERROR: File not found at {file}! Please check your directory structure.")

    runner = get_runner("icarus")

    runner.build(
        sources=verilog_files,
        hdl_toplevel="top_module",                
        build_dir=r"C:\Develop\uart_cocotb\sim\sim_build"
    )

    runner.test(
        hdl_toplevel="top_module",
        test_module="testbench"
    )

if __name__ == "__main__":
    run_sim()