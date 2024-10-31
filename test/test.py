import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_tt_um_Richard28277(dut):
    dut._log.info("Starting ALU test for all operations and corner cases.")

    # Set up a 10us (100 KHz) clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Define opcode values corresponding to ALU operations
    opcodes = {
        "ADD": 0b0000,
        "SUB": 0b0001,
        "MUL": 0b0010,
        "DIV": 0b0011,
        "AND": 0b0100,
        "OR": 0b0101,
        "XOR": 0b0110,
        "NOT": 0b0111,
        "ENC": 0b1000
    }

    # Test values for `a` and `b`
    a_vals = [0, 1, 7, 8, 15]  # Testing edge cases and mid-values
    b_vals = [0, 1, 7, 8, 15]

    for op_name, opcode in opcodes.items():
        for a in a_vals:
            for b in b_vals:
                dut.ui_in.value = (a << 4) | b
                dut.uio_in.value = opcode
                await ClockCycles(dut.clk, 1)

                # Expected results based on opcode
                if op_name == "ADD":
                    expected_sum = (a + b) % 16
                    expected_carry = int(a + b >= 16)
                    assert dut.uo_out.value == expected_sum, f"{op_name} failed for a={a}, b={b}"
                    assert dut.uio_out[6].value == expected_carry, f"{op_name} carry failed for a={a}, b={b}"

                elif op_name == "SUB":
                    expected_sub = (a - b) % 16
                    expected_borrow = int(a < b)
                    assert dut.uo_out.value == expected_sub, f"{op_name} failed for a={a}, b={b}"
                    assert dut.uio_out[6].value == expected_borrow, f"{op_name} borrow failed for a={a}, b={b}"

                elif op_name == "MUL":
                    expected_mul = (a * b) % 256
                    assert dut.uo_out.value == expected_mul, f"{op_name} failed for a={a}, b={b}"

                elif op_name == "DIV":
                    expected_quotient = a // b if b != 0 else 0
                    expected_remainder = a % b if b != 0 else 0
                    assert dut.uo_out.value == (expected_remainder << 4) | expected_quotient, f"{op_name} failed for a={a}, b={b}"

                elif op_name == "AND":
                    expected_and = a & b
                    assert dut.uo_out.value == expected_and, f"{op_name} failed for a={a}, b={b}"

                elif op_name == "OR":
                    expected_or = a | b
                    assert dut.uo_out.value == expected_or, f"{op_name} failed for a={a}, b={b}"

                elif op_name == "XOR":
                    expected_xor = a ^ b
                    assert dut.uo_out.value == expected_xor, f"{op_name} failed for a={a}, b={b}"

                elif op_name == "NOT":
                    expected_not = ~a & 0xF  # 4-bit NOT
                    assert dut.uo_out.value == expected_not, f"{op_name} failed for a={a}"

                elif op_name == "ENC":
                    encryption_key = 0xAB
                    expected_enc = ((a << 4) | b) ^ encryption_key
                    assert dut.uo_out.value == expected_enc, f"{op_name} failed for a={a}, b={b}"

                dut._log.info(f"Operation {op_name} with a={a}, b={b}: Passed")

    dut._log.info("All ALU operation tests completed successfully.")
