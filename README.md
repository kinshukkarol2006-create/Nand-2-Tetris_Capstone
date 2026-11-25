# Nand2Tetris Capstone Project

**Student**: Kinshuk Karol
**Roll number**: 2501730171 
**Parameter:** K = 71

## Project Structure

- `Screenshots/Part A/` — Hardware test screenshots (`Memory.hdl`, `CPU.hdl`, `Computer.hdl`)
- `Screenshots/Part B/` — Assembler test and program verification screenshots
- `Screenshots/Part C/` — CPU Emulator screenshots for `Box.hack`
- `assembler.py` — Custom Python two-pass Hack assembler with duplicate-label warning (`71 mod 3 = 2`)
- `Computer.hdl`, `CPU.hdl`, `Memory.hdl` — Hack hardware implementations
- `Add.asm` / `Add.hack` (6 lines), `Max.asm` / `Max.hack` (16 lines), `Rect.asm` / `Rect.hack` (25 lines), `Pong.asm` / `Pong.hack` (27,483 lines)
- `Box.asm` / `Box.hack` — Interactive box program (starts at row 71, 20 rows tall, 64 pixels / 4 words wide)
- `dup_test.asm` / `dup_test.hack`, `test.asm` / `test.hack` — Additional test files

## Usage

Assemble any `.asm` program with the Part B assembler:

```bash
python3 assembler.py Box.asm

