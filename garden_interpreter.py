import sys

class Garden:
    def __init__(self):
        self.frames = [{
            'plots': {},
            'current_plot': None,
            'loop_count': 0,
            'loop_label': None,
            'last_multiplier_for_plot': {},
            'last_graft_arg_for_plot': {}
        }]
        self.greenhouse = []
        self.weather = 'sunny'
        self.harvest = []
        self.functions = {}
        self.global_labels = {}
        self.function_labels = {}
        self.string_plots = {}
        self.current_plot_type = None

    @property
    def current_frame(self):
        return self.frames[-1]
    
    @property
    def plots(self):
        return self.current_frame['plots']
    
    @property
    def current_plot(self):
        return self.current_frame['current_plot']
    
    @current_plot.setter
    def current_plot(self, value):
        self.current_frame['current_plot'] = value
        
    @property
    def loop_count(self):
        return self.current_frame['loop_count']
    
    @loop_count.setter
    def loop_count(self, value):
        self.current_frame['loop_count'] = value
        
    @property
    def loop_label(self):
        return self.current_frame['loop_label']
    
    @loop_label.setter
    def loop_label(self, value):
        self.current_frame['loop_label'] = value
        
    @property
    def last_multiplier_for_plot(self):
        return self.current_frame['last_multiplier_for_plot']
    
    @property
    def last_graft_arg_for_plot(self):
        return self.current_frame['last_graft_arg_for_plot']

    def plant_seed(self, plot_name, value):
        if isinstance(value, str):
            self.string_plots[plot_name] = value
        else:
            self.plots[plot_name] = value

    def tend_plot(self, plot_name):
        if plot_name not in self.plots and plot_name not in self.string_plots:
            raise NameError(f"Plot '{plot_name}' not defined!")
        self.current_plot = plot_name
        self.current_plot_type = 'str' if plot_name in self.string_plots else 'int'

    def concat_plot(self, src_plot):
        if self.current_plot_type != 'str':
            raise TypeError(f"Current plot {self.current_plot} is not a string")
        if src_plot not in self.string_plots:
            raise NameError(f"String plot '{src_plot}' not defined")
            
        self.string_plots[self.current_plot] += self.string_plots[src_plot]

    def slice_plot(self, start, end):
        if self.current_plot_type != 'str':
            raise TypeError(f"Current plot {self.current_plot} is not a string")
            
        self.string_plots[self.current_plot] = \
            self.string_plots[self.current_plot][start:end]

    def water_plot(self, amount):
        if self.current_plot is None:
            raise ValueError("No current plot selected!")
        self.plots[self.current_plot] += amount

    def prune_plot(self, amount):
        if self.current_plot is None:
            raise ValueError("No current plot selected!")
        self.plots[self.current_plot] -= amount

    def graft_value(self, value, arg_str):
        self.plots[self.current_plot] *= value
        self.last_multiplier_for_plot[self.current_plot] = value
        self.last_graft_arg_for_plot[self.current_plot] = arg_str

    def divide_value(self, value, arg_str):
        current_value = self.plots[self.current_plot]
        if (self.current_plot in self.last_graft_arg_for_plot and 
            self.last_graft_arg_for_plot[self.current_plot] == arg_str):
            divisor = self.last_multiplier_for_plot[self.current_plot]
            if divisor == 0:
                raise ValueError(f"Cannot divide by zero in {self.current_plot}!")
            self.plots[self.current_plot] //= divisor
        else:
            if value == 0:
                raise ValueError(f"Cannot divide by zero in {self.current_plot}!")
            self.plots[self.current_plot] //= value

    def check_soil(self, condition, target, plot_name):
        if plot_name not in self.plots:
            self.plant_seed(plot_name, 0)
        current = self.plots[plot_name]
        if condition == 'rich':
            return current > target
        elif condition == 'poor':
            return current < target
        elif condition == 'balanced':
            return current == target
        return False

    def store_in_greenhouse(self):
        self.greenhouse.append(self.plots[self.current_plot])

    def retrieve_from_greenhouse(self):
        if not self.greenhouse:
            raise IndexError("Greenhouse is empty!")
        return self.greenhouse.pop()

    def set_weather(self, condition):
        self.weather = condition

    def add_to_harvest(self, value):
        self.harvest.append(str(value))

    def get_harvest(self):
        return ' '.join(self.harvest)

def parse_program(source):
    lines = source.split('\n')
    parsed = []
    functions = {}
    function_bodies = {}
    function_args = {}
    function_labels = {}
    current_function = None
    brace_count = 0
    body_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
            
        tokens = tokenize_line(stripped)
        if not tokens:
            continue
            
        if current_function is None:
            if tokens[0] == "function":
                func_name = tokens[1]
                args_str = tokens[2] if len(tokens) > 2 else '[]'
                if args_str.startswith('[') and args_str.endswith(']'):
                    args = [arg.strip() for arg in args_str[1:-1].split(',') if arg.strip()]
                else:
                    args = []
                current_function = func_name
                function_args[func_name] = args
                body_start_index = None
                for i, token in enumerate(tokens):
                    if token == '{':
                        body_start_index = i + 1
                        break
                if body_start_index is not None and body_start_index < len(tokens):
                    body_lines.append(' '.join(tokens[body_start_index:]))
                brace_count = 1
            else:
                if tokens[0].endswith(':'):
                    label_name = tokens[0][:-1]
                    parsed.append(('label', label_name))
                else:
                    parsed.append(tuple(tokens))
        else:
            if '{' in tokens:
                brace_count += tokens.count('{')
            if '}' in tokens:
                brace_count -= tokens.count('}')
            if brace_count <= 0:
                if '}' in tokens:
                    end_index = tokens.index('}')
                    body_lines.append(' '.join(tokens[:end_index]))
                else:
                    body_lines.append(' '.join(tokens))
                body_str = ' '.join(body_lines)
                function_bodies[func_name] = body_str
                current_function = None
                body_lines = []
                brace_count = 0
            else:
                body_lines.append(' '.join(tokens))
                
    for func_name, body in function_bodies.items():
        func_program = parse_function_body(body)
        labels = {}
        for idx, instr in enumerate(func_program):
            if instr and instr[0] == 'label':
                label_name = instr[1]
                labels[label_name] = idx
        function_labels[func_name] = labels
        functions[func_name] = (function_args[func_name], func_program)
    
    main_program = []
    for line in parsed:
        if not line:
            continue
        if line[0] == 'label':
            main_program.append(line)
            continue
            
        cmd = line[0].lower()
        args = line[1:]
        instruction = (cmd,) + tuple(args)
        main_program.append(instruction)
        
    return main_program, functions, function_labels

def parse_function_body(body):
    lines = body.split('\n')
    parsed = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        tokens = tokenize_line(stripped)
        if not tokens:
            continue
        if tokens[0].endswith(':'):
            label_name = tokens[0][:-1]
            parsed.append(('label', label_name))
        else:
            parsed.append(tuple(tokens))
    return parsed

def resolve_value(garden, value_str):
    if value_str is None:
        raise NameError(f"Plot or value '{value_str}' not defined!")
        
    if isinstance(value_str, str):
        value_str = value_str.strip()
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
    
    try:
        return int(value_str)
    except ValueError:
        pass
        
    if value_str in garden.plots:
        return garden.plots[value_str]
        
    if value_str in garden.string_plots:
        return garden.string_plots[value_str]
        
    raise NameError(f"Plot or value '{value_str}' not defined!")

def tokenize_line(line):
    tokens = []
    current = []
    in_quote = False
    escaped = False
    i = 0
    n = len(line)
    
    while i < n:
        char = line[i]
        if in_quote:
            current.append(char)
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                in_quote = False
                tokens.append(''.join(current))
                current = []
            i += 1
        else:
            if char == '#':
                break
            elif char == '"':
                current = [char]
                in_quote = True
                i += 1
            elif char.isspace():
                if current:
                    tokens.append(''.join(current))
                    current = []
                i += 1
            else:
                current.append(char)
                i += 1
    
    if in_quote:
        tokens.append(''.join(current))
    elif current:
        tokens.append(''.join(current))
        
    return tokens

def execute(program, functions, function_labels):
    garden = Garden()
    garden.functions = functions
    garden.function_labels = function_labels
    
    for idx, instr in enumerate(program):
        if instr and instr[0] == 'label':
            label_name = instr[1]
            garden.global_labels[label_name] = idx

    call_stack = []
    current_program = program
    current_labels = garden.global_labels
    pc = 0
    watering_can = 0
    error = None

    while pc < len(current_program):
        instruction = current_program[pc]
        if not instruction:
            pc += 1
            continue
        cmd = instruction[0]
        try:
            if cmd == 'plant':
                plot_name = instruction[1]
                value = resolve_value(garden, instruction[2]) if len(instruction) >= 3 else 0
                garden.plant_seed(plot_name, value)
            elif cmd == 'tend':
                plot_name = instruction[1]
                garden.tend_plot(plot_name)
            elif cmd == 'water':
                amount = resolve_value(garden, instruction[1])
                garden.water_plot(amount)
            elif cmd == 'prune':
                amount = resolve_value(garden, instruction[1])
                garden.prune_plot(amount)
            elif cmd == 'graft':
                arg_str = instruction[1]
                value = resolve_value(garden, arg_str)
                garden.graft_value(value, arg_str)
            elif cmd == 'divide':
                arg_str = instruction[1]
                value = resolve_value(garden, arg_str)
                garden.divide_value(value, arg_str)
            elif cmd == 'concat':
                src_plot = instruction[1]
                garden.concat_plot(src_plot)
            elif cmd == 'slice':
                start = resolve_value(garden, instruction[1])
                end = resolve_value(garden, instruction[2])
                garden.slice_plot(start, end)
            elif cmd == 'check':
                condition = instruction[1]
                plot_name = instruction[2]
                target = resolve_value(garden, instruction[3])
                if not garden.check_soil(condition, target, plot_name):
                    skip_count = 0
                    while pc + skip_count < len(current_program) - 1:
                        skip_count += 1
                        next_instr = current_program[pc + skip_count]
                        if not next_instr:
                            continue
                        next_cmd = next_instr[0]
                        if next_cmd in ('harvest', 'weather', 'check', 'return'):
                            pc += skip_count
                            break
                    else:
                        pc = len(current_program)
                    continue
            elif cmd == 'store':
                garden.store_in_greenhouse()
            elif cmd == 'retrieve':
                value = garden.retrieve_from_greenhouse()
                garden.plots[garden.current_plot] = value
            elif cmd == 'weather':
                condition = instruction[1]
                garden.set_weather(condition)
            elif cmd == 'harvest':
                if len(instruction) >= 2:
                    plot_name = instruction[1]
                    if plot_name in garden.plots:
                        value = garden.plots[plot_name]
                    elif plot_name in garden.string_plots:
                        value = garden.string_plots[plot_name]
                    else:
                        raise NameError(f"Plot '{plot_name}' not defined!")
                else:
                    if garden.current_plot is None:
                        raise ValueError("No current plot selected!")
                    if garden.current_plot_type == 'int':
                        value = garden.plots[garden.current_plot]
                    else:
                        value = garden.string_plots[garden.current_plot]
                garden.add_to_harvest(value)
            elif cmd == 'sow':
                amount = resolve_value(garden, instruction[1])
                watering_can = amount
            elif cmd == 'irrigate':
                plot_name = instruction[1]
                if plot_name not in garden.plots:
                    garden.plant_seed(plot_name, 0)
                garden.plots[plot_name] += watering_can
            elif cmd == 'bloom':
                times = resolve_value(garden, instruction[1])
                label_name = instruction[2]
                if label_name in current_labels:
                    garden.loop_count = times
                    garden.loop_label = label_name
                    if times > 0:
                        pc = current_labels[label_name]
                        continue
                else:
                    raise NameError(f"Label '{label_name}' not found")
            elif cmd == 'label':
                pass
            elif cmd == 'wither':
                garden.loop_count -= 1
                if garden.loop_count > 0:
                    if garden.loop_label in current_labels:
                        pc = current_labels[garden.loop_label]
                        continue
                    else:
                        raise NameError(f"Loop label '{garden.loop_label}' not found")
            elif cmd == 'crossbreed':
                value = resolve_value(garden, instruction[1])
                garden.plots[garden.current_plot] ^= value
            elif cmd == 'rotate':
                degrees = resolve_value(garden, instruction[1])
                value = garden.plots[garden.current_plot] & 0xFF
                degrees = degrees % 8
                rotated = ((value << degrees) | (value >> (8 - degrees))) & 0xFF
                garden.plots[garden.current_plot] = rotated
            elif cmd == 'function':
                pass
            elif cmd == 'call':
                func_name = instruction[1]
                if func_name not in garden.functions:
                    raise NameError(f"Function '{func_name}' not defined")
                args, body = garden.functions[func_name]
                func_labels = garden.function_labels[func_name]
                arg_vals = []
                for arg_expr in instruction[2:]:
                    arg_vals.append(resolve_value(garden, arg_expr))
                new_frame = {
                    'plots': {},
                    'current_plot': None,
                    'loop_count': 0,
                    'loop_label': None,
                    'last_multiplier_for_plot': {},
                    'last_graft_arg_for_plot': {}
                }
                for i, arg_name in enumerate(args):
                    new_frame['plots'][arg_name] = arg_vals[i] if i < len(arg_vals) else 0
                call_stack.append((pc + 1, current_program, current_labels))
                garden.frames.append(new_frame)
                current_program = body
                current_labels = func_labels
                pc = -1
            elif cmd == 'return':
                return_val = 0
                if len(instruction) > 1:
                    return_val = resolve_value(garden, instruction[1])
                
                if call_stack:
                    return_pc, return_prog, return_labels = call_stack.pop()
                    garden.frames.pop()
                    current_program = return_prog
                    current_labels = return_labels
                    garden.plant_seed('return', return_val)
                    pc = return_pc - 1
                else:
                    break
            else:
                raise ValueError(f"Unknown command: {cmd}")
                
        except Exception as error_exc:
            error = f"Error at instruction {pc+1}: {error_exc}\nInstruction: {instruction}"
            break
        pc += 1
        
    return {
        'harvest': garden.get_harvest(),
        'error': error
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gardeners_script.py <filename.garden>")
        sys.exit(1)
        
    try:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
            
        program, functions, function_labels = parse_program(source)
        result = execute(program, functions, function_labels)
        
        if result.get('error'):
            print(result['error'])
            sys.exit(1)
        elif result.get('harvest'):
            print(result['harvest'])
        else:
            print("Program executed but produced no output.")
            
    except Exception as ex:
        print(f"Fatal error: {ex}")
        sys.exit(1)