// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
	@SCREEN
	D=A
	@i
	M=D
(LOOP)
	@KBD//check keyboard
	D = M
	@Black
	D;JGT//jump to BLACK if KBD != 0
	@White
	D;JEQ // if KBD == 0 jump to White
(White)//Starts filling screen in with white starting at the last black pixel
	@i
	A = M
	M = 0 // fills RAM[i] with white
	//Check to see if i should be incremented
	@i
	D = M 
	@SCREEN
	D = D - A 
	@LOOP
	D;JEQ // if i - SCREEN == 0 return to LOOP
	@i
	M = M - 1// decrements i to edit next set of pixels in memory map
	@LOOP//jumps back to start of white until i- KBD == 0
	0;JMP
(Black)//fills screen with black if kbd is pressed
	@i
	A = M
	M = -1 //files pixel at A location with black
	@i
	D = M
	@KBD
	D = D-A
	@LOOP
	D = D+1;JEQ
	@i
	M = M+1
	@LOOP
	0;JMP
	