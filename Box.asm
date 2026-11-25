// Part C: Box Program for K = 71
// While any key is pressed (KBD != 0), draws a black box starting at row 71,
// 20 rows tall (rows 71..90), and 64 pixels (4 words) wide from the left edge.
// When no key is pressed (KBD == 0), clears the box back to white.

(MAIN)
    // Check keyboard state at RAM[24576] (KBD)
    @KBD
    D=M
    @CLEAR
    D;JEQ           // If no key is pressed (D == 0), clear the box

    // Set fill color to black (-1 = 1111111111111111) and draw
    @color
    M=-1
    @DRAW
    0;JMP

(CLEAR)
    // Set fill color to white (0 = 0000000000000000) and draw
    @color
    M=0

(DRAW)
    // Row counter r = 71
    @71
    D=A
    @row
    M=D

(ROW_LOOP)
    // Stop once row > 90 (71 + 20 - 1 = 90)
    @90
    D=A
    @row
    D=D-M           // D = 90 - row
    @MAIN
    D;JLT           // If row > 90, return to MAIN

    // Compute row start address: SCREEN + 32 * row
    // Multiply row by 32 using 5 left shifts
    @row
    D=M
    @prod
    M=D             // prod = row

    @prod
    D=M
    M=D+M           // prod = row * 2

    @prod
    D=M
    M=D+M           // prod = row * 4

    @prod
    D=M
    M=D+M           // prod = row * 8

    @prod
    D=M
    M=D+M           // prod = row * 16

    @prod
    D=M
    M=D+M           // prod = row * 32

    @SCREEN
    D=A
    @prod
    D=D+M           // D = SCREEN + 32 * row
    @addr
    M=D             // addr = start word of current row

    // Fill 4 consecutive words (64 pixels from left edge)
    // Word 0
    @color
    D=M
    @addr
    A=M
    M=D

    // Word 1
    @addr
    M=M+1
    @color
    D=M
    @addr
    A=M
    M=D

    // Word 2
    @addr
    M=M+1
    @color
    D=M
    @addr
    A=M
    M=D

    // Word 3
    @addr
    M=M+1
    @color
    D=M
    @addr
    A=M
    M=D

    // Advance to next row (row = row + 1)
    @row
    M=M+1
    @ROW_LOOP
    0;JMP