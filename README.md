# ALU Simulator CS 325 Report

A mini ALU simulator in Python using Rich for CLI

Rich is a bit complex on how it deals with layouts but the core idea is in `alu.py` with the `ALU` class. It has functions inside it that uses Python's own bitwise operators to calculate ADD, SUB, AND, OR, XOR, shift left, and shift right. In the program itself, you can select which operation to perform and then choose 2 numbers to perform it on

There are binaries for Linux and Windows built by github actions in the Releases section for download.

## Examples

This is using the `alu.add()` function and displaying it nicely with Rich (base 10 numbers formatted to base 2)

```
╭─────── Mini ALU Simulator ───────╮                                                                                                                                                                                                                            
│    1. ADD      5. XOR            │                                                                                                                                                                                                                            
│    2. SUB      6. Shift Left     │                                                                                                                                                                                                                            
│    3. AND      7. Shift Right    │                                                                                                                                                                                                                            
│    4. OR       0. Exit           │                                                                                                                                                                                                                            
╰──────────────────────────────────╯                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                
╭─────────────── ADD ────────────────╮                                                                                                                                                                                                                          
│ A     00000101  (5)                │                                                                                                                                                                                                                          
│ + B   00001010  (10)               │                                                                                                                                                                                                                          
│       ────────                     │                                                                                                                                                                                                                          
│ =     00001111  (15)               │                                                                                                                                                                                                                          
│                                    │                                                                                                                                                                                                                          
│ Carry: False                       │                                                                                                                                                                                                                          
│ Signed overflow: False             │                                                                                                                                                                                                                          
│                                    │                                                                                                                                                                                                                          
│ Unsigned result: 15                │                                                                                                                                                                                                                          
│ Signed (2's complement): 15        │                                                                                                                                                                                                                          
│                                    │                                                                                                                                                                                                                          
│ Press Enter to return to the menu. │                                                                                                                                                                                                                          
╰────────────────────────────────────╯       
```

XOR implementation:

This is just using `alu.bitwise_xor()` function, which technically doesn't *really* need a function since it's pretty simple (along with AND), but the use of a dataclass of `ALUResult` makes it really nice to use types in Python :)

```
╭─────── Mini ALU Simulator ───────╮                                                                                                                                                                                                                            
│    1. ADD      5. XOR            │                                                                                                                                                                                                                            
│    2. SUB      6. Shift Left     │                                                                                                                                                                                                                            
│    3. AND      7. Shift Right    │                                                                                                                                                                                                                            
│    4. OR       0. Exit           │                                                                                                                                                                                                                            
╰──────────────────────────────────╯                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                
╭─────────────── XOR ────────────────╮                                                                                                                                                                                                                          
│ A     00000001  (1)                │                                                                                                                                                                                                                          
│ ^ B   00000000  (0)                │                                                                                                                                                                                                                          
│       ────────                     │                                                                                                                                                                                                                          
│ =     00000001  (1)                │                                                                                                                                                                                                                          
│                                    │                                                                                                                                                                                                                          
│                                    │                                                                                                                                                                                                                          
│ Unsigned result: 1                 │                                                                                                                                                                                                                          
│ Signed (2's complement): 1         │                                                                                                                                                                                                                          
│                                    │                                                                                                                                                                                                                          
│ Press Enter to return to the menu. │                                                                                                                                                                                                                          
╰────────────────────────────────────╯  
```

## Tests

There are tests that I made for the `ALU` class in particular in `tests/test_alu.py` that uses PyTest. It just validates outputs that should be expected for each function. You can run them like this:

```bash
uv run pytest
```

The current source code says they all pass and I believe their assertions are right

## License

it's just released into the public domain with the CC0 Universal license, it's not that complex of code especially the backend of it, the frontend was what took the most time...