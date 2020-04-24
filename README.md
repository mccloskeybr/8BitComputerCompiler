
## 8 Bit Computer Compiler

This is for the breadboard computer based off of Ben Eater's SAP 8-bit breadboard computer (more info located [here](https://eater.net/8bit)). All commands and control logic is the same as theirs. This was created in an effort to move the instruction set to a separate EEPROM for the purpose of making programs more permanent and opening more space up for global variables, but it can also be utilized to minimize the amount of hand-translation you might have to do.

### Writing code

| Supported Instructions | Description |
|:----------------------:|:----------- |
| NOP | No operation |
| LDA x\* | Load the contents from address x into the A register | 
| ADD x\* | Add the contents from address x to the A register and store in the A register |
| SUB x\* | Subtract the contents of the address x from the A register and store in the A register |
| STA x\* | Store the contents from the A register in address x |
| LDI | Load the contents from the current instruction into the A register |
| JMP x\* | Jump to address x |
| JC x\* | Jump to address x if the carry flag is on |
| JZ x\* | Jump to address x if the zero flag is on |
| OUT | Load the contents of register A into the output register |
| HLT | Halt the clock |
| global x | Defines variable x in the global scope (so you don't have to remember the addresses of globals) |

Global variables can be added using the ```global``` instruction. These need to be pre-set in ram before program execution, however. **The addresses are stored from top to bottom** i.e., the first global variable defined is stored at address 15, the second at 14, and so on.

Comments are supported using # (all characters after # are ignored).

Adding additional commands is relatively easy, I encourage you to mess around with the code if it is at all interesting.

### Using the compiler

```
python compile.py <-v, --verbose> <-o, --out_path> input_path
```
- input\_path, the path to the file to compile (required)
- -v, verbose flag
- out\_path, the output path of the compiled file. If not specified, will print to console in a readable format.

Running without an output prints the contents directly to the screen.

![alt text](/res/fib_no_out.png)

Running with an output produces a .bin file that contains the compiled code.

![alt text](/res/fib_out.png)


