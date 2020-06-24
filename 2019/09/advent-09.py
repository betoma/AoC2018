import intcode

program = intcode.Intcode.read_program("input.txt")
for x in program.run_program([2]):
    print(x)
