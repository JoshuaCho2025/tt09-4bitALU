<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works
4-Bit ALU:


Inputs and Outputs:

ui_in: 8-bit input split into a and b, each being 4 bits.
uo_out: 8-bit output to send the result of the operation.
uio_in: 8-bit input for the opcode, only the lower 4 bits are used to determine the operation.
uio_out: 8-bit output for flags (e.g., carry out and overflow).
uio_oe: 8-bit output enable signal, which defines whether the bits are inputs or outputs.
Operation Encoding:

Each arithmetic or logical operation is assigned a 4-bit opcode, defining ADD, SUB, MUL, DIV, AND, OR, XOR, NOT, and ENC (encryption operation).
Internal Signals:

a and b are extracted from ui_in.
opcode is extracted from uio_in.
Additional signals hold results for each operation type (add_result, sub_result, mul_result, div_quotient, and div_remainder), while and_result, or_result, xor_result, and not_result handle logical operations.
Operations:

Addition: add_result captures the sum of a and b and a carry-out bit.
Subtraction: sub_result captures the difference and a borrow indicator.
Multiplication: mul_result stores the product.
Division: div_quotient stores the quotient, and div_remainder stores the remainder. Division by zero is handled by setting the result to zero.
Logical Operations: AND, OR, XOR, and NOT are performed directly.
Encryption: Combines a and b into an 8-bit value and XORs it with ENCRYPTION_KEY.
Sequential Logic:

On each positive clock edge or when reset (rst_n) is low, the module updates result, carry_out, and overflow based on opcode.
Overflow Detection: It uses specific conditions for both addition and subtraction to set the overflow flag.
Output Assignments:

uo_out is assigned the final result.
uio_out[7] holds the overflow flag, and uio_out[6] holds the carry-out flag, with other bits set to zero.
uio_oe is set to indicate which bits are output and which are input.
Unused Signal Handling:

_unused combines unused signals to avoid synthesis warnings.

## How to test

Explain how to use your project

## External hardware

No External Hardware Used
