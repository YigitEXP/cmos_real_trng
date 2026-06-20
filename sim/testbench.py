import cocotb
from cocotb.triggers import Timer
import tkinter as tk

dut_global = None
root = None
bit_label = None

clk_auto_run = False
rst_state = 0
bit_counter = 0

def gui_design():
    global root, bit_label, clk_auto_run, rst_state
    root = tk.Tk()
    root.title("CMOS TRNG Testbench GUI")
    root.geometry("400x300")
    root.configure(bg="#1e1e1e")

    status_label = tk.Label(root, text="FPGA Simulator", fg="#00ff00", bg="#1e1e1e", font=("Arial", 12, "bold"))
    status_label.pack(pady=10)

    info_label = tk.Label(root, text="Random Output:", fg="#aaaaaa", bg="#1e1e1e", font=("Arial", 10))
    info_label.pack(pady=2)
    
    bit_label = tk.Label(root, text="-", fg="#ffffff", bg="#2d2d2d", font=("Courier New", 24, "bold"), width=5, relief="solid", bd=2)
    bit_label.pack(pady=5)

    def clk_toggle():
        global clk_auto_run
        if not clk_auto_run:
            clk_auto_run = True
            clk_btn.config(text="CLK: ON (Running)", bg="#007acc")
        else:
            clk_auto_run = False
            clk_btn.config(text="CLK: OFF (Stopped)", bg="#333333")

    def reset_toggle():
        global rst_state
        if rst_state == 0:
            rst_state = 1
            reset_btn.config(text="Reset: ON", bg="#ff0000")
        else:
            rst_state = 0
            reset_btn.config(text="Reset: OFF", bg="#333333")

    clk_btn = tk.Button(root, text="CLK: OFF (Stopped)", font=("Arial", 11), bg="#333333", fg="white", command=clk_toggle, width=25)
    clk_btn.pack(pady=10)

    reset_btn = tk.Button(root, text="RESET", font=("Arial", 11), bg="#333333", fg="white", command=reset_toggle, width=25)
    reset_btn.pack(pady=10)

@cocotb.test()
async def trng_test(dut):
    global dut_global, root, clk_auto_run, rst_state, bit_counter
    dut_global = dut

    dut.clk.value = 0
    dut.rst.value = 0

    gui_design()
    print("Control panel UI loaded into simulator scheduler.")

    while True:
        if root is not None:
            try:
                root.update()
            except tk.TclError:
                break 

        dut.rst.value = rst_state

        if clk_auto_run:
            dut.clk.value = 1
            await Timer(5, unit="ns")

            try:
                val_str = str(dut.random_bit.value)
                if 'x' in val_str.lower() or 'z' in val_str.lower():
                    random_value = 0
                else:
                    random_value = int(dut.random_bit.value)
                
                bit_counter += 1
                print(f"Auto sampled random bit ({bit_counter}.): {random_value}")

                if random_value == 1:
                    bit_label.config(text="1", fg="#00ff00", bg="#1a3a1a")
                else:
                    bit_label.config(text="0", fg="#ffcc00", bg="#3a3a1a")
            except Exception:
                bit_label.config(text="X", fg="#ff0000", bg="#2d2d2d")

            dut.clk.value = 0
            await Timer(5, unit="ns")
        else:
            await Timer(10, unit="ns")