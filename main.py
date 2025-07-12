import sys

def run_CharLang(code):
    tape = [0] * 30000
    ptr = 0
    pc = 0
    loops = []
    output = []

    while pc < len(code):
        cmd = code[pc]
        
        if cmd == '>': 
            ptr += 1
        elif cmd == '<': 
            ptr -= 1
        elif cmd == '+': 
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-': 
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.': 
            output.append(chr(tape[ptr]))
        elif cmd == ',': 
            data = sys.stdin.read(1)
            tape[ptr] = ord(data) if data else 0
        elif cmd == '[':
            if tape[ptr] == 0:
                depth = 1
                while depth > 0:
                    pc += 1
                    if pc >= len(code): break
                    if code[pc] == '[': depth += 1
                    elif code[pc] == ']': depth -= 1
            else:
                loops.append(pc)
        elif cmd == ']':
            if tape[ptr] != 0: 
                pc = loops[-1]
            else: 
                loops.pop()
        elif cmd == 'C': 
            tape[ptr+1] = tape[ptr]
        elif cmd == 'S': 
            tape[ptr], tape[ptr+1] = tape[ptr+1], tape[ptr]
        elif cmd == 'P': 
            output.append(str(tape[ptr]))
        elif cmd == 'R': 
            tape[ptr] = 0
        pc += 1

    return ''.join(output)

def main():
    result = run_CharLang("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>+++.")
    print(result)

if __name__ == "__main__":
    main()