
"""
=========================================================
NAND2TETRIS CAPSTONE PROJECT
HACK ASSEMBLER v1.0
=========================================================

Student: kinshuk karol
Roll Number: 2501730171
Personal Number K: 71

Required extra feature:
Warn when the same label is declared more than once.

Architecture:
1. Source cleaning
2. Pass 1: Label detection and symbol table
3. Pass 2: Machine code generation
4. A-instruction translation
5. C-instruction translation
6. Variable allocation
7. Error and warning reporting
8. .hack file generation

Usage:
    python assembler.py
    python assembler.py --self-test
    python assembler.py Add.asm
    python assembler.py Add.asm Add.hack
=========================================================
"""

import sys
from pathlib import Path

PREDEFINED_SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4,
    "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9,
    "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
}

COMP_TABLE = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000", "M":   "1110000",
    "!D":  "0001101",
    "!A":  "0110001", "!M":  "1110001",
    "-D":  "0001111",
    "-A":  "0110011", "-M":  "1110011",
    "D+1": "0011111",
    "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101",
}

DEST_TABLE = {
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011", "DM":  "011",
    "A":   "100",
    "AM":  "101", "MA":  "101",
    "AD":  "110", "DA":  "110",
    "AMD": "111", "ADM": "111", "MAD": "111", "MDA": "111", "DAM": "111", "DMA": "111",
}

JUMP_TABLE = {
    "":    "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def clean_line(raw_line: str) -> str:
    return raw_line.split("//", 1)[0].strip()


def first_pass(lines: list[str], symbols: dict[str, int]) -> list[str]:
    instructions = []
    seen_labels = set()
    rom_address = 0

    for line_number, raw_line in enumerate(lines, start=1):
        cleaned = clean_line(raw_line)
        if not cleaned:
            continue

        if cleaned.startswith("(") and cleaned.endswith(")"):
            label = cleaned[1:-1].strip()
            if label in seen_labels:
                print(f"Warning: Duplicate label ({label}) on line {line_number}")
            seen_labels.add(label)
            symbols[label] = rom_address
        else:
            instructions.append(cleaned)
            rom_address += 1

    return instructions


def encode_c_instruction(instr: str) -> str:
    if "=" in instr:
        dest_part, rest = instr.split("=", 1)
    else:
        dest_part, rest = "", instr

    if ";" in rest:
        comp_part, jump_part = rest.split(";", 1)
    else:
        comp_part, jump_part = rest, ""

    dest = dest_part.strip()
    comp = comp_part.strip()
    jump = jump_part.strip()

    return f"111{COMP_TABLE[comp]}{DEST_TABLE[dest]}{JUMP_TABLE[jump]}"


def second_pass(instructions: list[str], symbols: dict[str, int]) -> list[str]:
    binary_lines = []
    next_ram_address = 16

    for instr in instructions:
        if instr.startswith("@"):
            operand = instr[1:].strip()
            if operand.isdigit():
                address = int(operand)
            else:
                if operand not in symbols:
                    symbols[operand] = next_ram_address
                    next_ram_address += 1
                address = symbols[operand]
            binary_lines.append(f"0{address:015b}")
        else:
            binary_lines.append(encode_c_instruction(instr))

    return binary_lines


def assemble(asm_path: Path) -> Path:
    symbols = dict(PREDEFINED_SYMBOLS)
    raw_lines = asm_path.read_text(encoding="utf-8").splitlines()

    instructions = first_pass(raw_lines, symbols)
    binary_lines = second_pass(instructions, symbols)

    out_path = asm_path.with_suffix(".hack")
    out_path.write_text("\n".join(binary_lines) + "\n", encoding="utf-8")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 assembler.py <Program.asm>")
        sys.exit(1)

    output_file = assemble(Path(sys.argv[1]))
    print(f"Generated {output_file}")