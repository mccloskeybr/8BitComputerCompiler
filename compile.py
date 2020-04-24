
from argparse import ArgumentParser

verbose = False

parser = ArgumentParser(description = 'Compile assembly to machine code for custom computer.')
parser.add_argument('--in_path', '-i', type=str, help='Input file to be compiled.')
parser.add_argument('--out_path', '-o', type=str, help = 'Output file path.', default = None)
parser.add_argument('--verbose', '-v', action='store_true')

'''
Individual functions per assembly instruction
allows for addition of new commands that might be a combination of others,
or the addition of meta commands (i.e. global)
'''
def nop(cmd):
    return asm_to_machine[cmd[0]] << 4 & 0xf0

def lda(cmd):
    if cmd[1].isdigit():
        return asm_to_machine[cmd[0]] << 4 | int(cmd[1])
    return asm_to_machine[cmd[0]] << 4 | int(global_lookup.index(cmd[1]))


def add(cmd):
    if cmd[1].isdigit():
        return asm_to_machine[cmd[0]] << 4 | int(cmd[1])
    return asm_to_machine[cmd[0]] << 4 | int(global_lookup.index(cmd[1]))

def sub(cmd):
    if cmd[1].isdigit():
        return asm_to_machine[cmd[0]] << 4 | int(cmd[1])
    return asm_to_machine[cmd[0]] << 4 | int(global_lookup.index(cmd[1]))

def sta(cmd):
    if cmd[1].isdigit():
        return asm_to_machine[cmd[0]] << 4 | int(cmd[1])
    return asm_to_machine[cmd[0]] << 4 | int(global_lookup.index(cmd[1]))

def ldi(cmd):
    if cmd[1].isdigit():
        return asm_to_machine[cmd[0]] << 4 | int(cmd[1])
    return asm_to_machine[cmd[0]] << 4 | int(global_lookup.index(cmd[1]))

def jmp(cmd):
    if cmd[1].isdigit():
        return asm_to_machine[cmd[0]] << 4 | int(cmd[1])
    return asm_to_machine[cmd[0]] << 4 | int(global_lookup.index(cmd[1]))

def jc(cmd):
    if cmd[1].isdigit():
        return asm_to_machine[cmd[0]] << 4 | int(cmd[1])
    return asm_to_machine[cmd[0]] << 4 | int(global_lookup.index(cmd[1]))

def jz(cmd):
    if cmd[1].isdigit():
        return asm_to_machine[cmd[0]] << 4 | int(cmd[1])
    return asm_to_machine[cmd[0]] << 4 | int(global_lookup.index(cmd[1]))

def out(cmd):
    return asm_to_machine[cmd[0]] << 4 & 0xf0

def hlt(cmd):
    return asm_to_machine[cmd[0]] << 4 & 0xf0

def global_var(cmd):
    global_lookup.append(cmd[1])

'''
define lookup tables:
    global_lookup   - globals are defined in the order of appearance
    asm_parse       - links the language's instructions to the above functions
    asm_to_machine  - links the recognizable commands by the computer to machine code
'''
global_lookup = []

asm_to_machine = {
    'NOP': 0b0000,
    'LDA': 0b0001,
    'ADD': 0b0010,
    'SUB': 0b0011,
    'STA': 0b0100,
    'LDI': 0b0101,
    'JMP': 0b0110,
    'JC':  0b0111,
    'JZ':  0b1000,
    'OUT': 0b1110,
    'HLT': 0b1111
}

asm_parse = {
    'NOP': nop,
    'LDA': lda,
    'ADD': add,
    'SUB': sub,
    'STA': sta,
    'LDI': ldi,
    'JMP': jmp,
    'JC':  jc,
    'JZ':  jz,
    'OUT': out,
    'HLT': hlt,
    'global': global_var
}

'''
extracts the commands from the input file and puts them in a split list
'''
def get_cmds(input_path):
    cmds = []
    input_file = open(input_path, 'r')
    for line in input_file:
        full_cmd = line.split('#')[0]   # get rid of comments
        full_cmd = full_cmd.replace('\n', '')   # get rid of newlines
        full_cmd = full_cmd.replace('\t', '')   # get rid of tabs
        if full_cmd == '':
            continue
        cmds.append(full_cmd.split(' '))    # split by space
    input_file.close()
    return cmds

def validate(cmds):
    for i, cmd in enumerate(cmds):
        if cmd[0] not in asm_parse.keys():  # if encounter command that's not explicitly defined
            raise Exception('ERR on line ' + str(i) + ' (' + cmd[0] + '): Command not expected.')

def main():
    global verbose

    # parse args
    args = parser.parse_args()
    input_path = args.in_path
    output_path = args.out_path
    verbose = args.verbose

    # get commands and run initial checks
    cmds = get_cmds(input_path)
    try:
        validate(cmds)
    except:
        raise

    # begin compiling commands
    compiled_cmds = []
    for i, cmd in enumerate(cmds):
        try:
            compiled = asm_parse[cmd[0]](cmd)
            if compiled is not None:
                compiled = format(compiled, '08b')
                if verbose:
                    print(cmd + [compiled])
                compiled_cmds.append(compiled)
        except:
            raise Exception('ERR on line ' + str(i) + ' (' + cmd[0] + '): Could not compile.')

    # write compiled commands to file
    if output_path is not None:
        output_file = open(output_path, 'w')
        for cmd in compiled_cmds:
            output_file.write(cmd)
    else:
        for cmd in compiled_cmds:
            print(cmd)

if __name__ == '__main__':
    main()

