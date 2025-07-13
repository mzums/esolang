import sys

class Garden:
    def __init__(self):
        self.plots = {}
        self.greenhouse = []
        self.weather = 'sunny'
        self.current_plot = None
        self.labels = {}
        self.harvest = []
        self.loop_count = 0
        self.loop_label = None
        self.last_multiplier_for_plot = {}
        self.last_graft_arg_for_plot = {}

    def plant_seed(self, plot_name, value):
        self.plots[plot_name] = value

    def tend_plot(self, plot_name):
        if plot_name not in self.plots:
            self.plant_seed(plot_name, 0)
        self.current_plot = plot_name

    def water_plot(self, amount):
        self.plots[self.current_plot] += amount

    def prune_plot(self, amount):
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
    
    for line in lines:
        line = line.split('#')[0].strip()
        if not line:
            continue
            
        if line.endswith(':'):
            label_name = line[:-1].strip()
            parsed.append(('label', label_name))
            continue
            
        tokens = line.split()
        if not tokens:
            continue
            
        cmd = tokens[0].lower()
        args = tokens[1:]
        parsed.append(tuple([cmd] + args))
            
    return parsed

def resolve_value(garden, value_str):
    if value_str is None:
        return 0
        
    if value_str.replace('-', '').isdigit():
        return int(value_str)
    elif value_str in garden.plots:
        return garden.plots[value_str]
    else:
        garden.plant_seed(value_str, 0)
        return 0

def execute(program):
    garden = Garden()
    pc = 0
    watering_can = 0
    
    for idx, instr in enumerate(program):
        if len(instr) > 0 and instr[0] == 'label':
            label_name = instr[1]
            garden.labels[label_name] = idx

    while pc < len(program):
        instruction = program[pc]
        if not instruction:
            pc += 1
            continue
            
        cmd = instruction[0]
        
        try:
            if cmd == 'plant':
                plot_name = instruction[1]
                value = resolve_value(garden, instruction[2] if len(instruction) >= 3 else '0')
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
                
            elif cmd == 'check':
                condition = instruction[1]
                plot_name = instruction[2]
                target = resolve_value(garden, instruction[3])
                if not garden.check_soil(condition, target, plot_name):
                    skip_count = 0
                    while pc + skip_count < len(program) - 1:
                        skip_count += 1
                        next_instr = program[pc + skip_count]
                        if not next_instr:
                            continue
                        next_cmd = next_instr[0]
                        
                        if next_cmd in ('harvest', 'weather', 'check'):
                            pc += skip_count
                            break
                    else:
                        pc = len(program)
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
                    if plot_name not in garden.plots:
                        garden.plant_seed(plot_name, 0)
                    value = garden.plots[plot_name]
                else:
                    value = garden.plots[garden.current_plot]
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
                if label_name in garden.labels:
                    garden.loop_count = times
                    garden.loop_label = label_name
                    if times > 0:
                        pc = garden.labels[label_name]
                        continue
                
            elif cmd == 'label':
                pass
                
            elif cmd == 'wither':
                garden.loop_count -= 1
                if garden.loop_count > 0:
                    pc = garden.labels[garden.loop_label]
                    continue
                
            elif cmd == 'crossbreed':
                value = resolve_value(garden, instruction[1])
                garden.plots[garden.current_plot] ^= value
                
            elif cmd == 'rotate':
                degrees = resolve_value(garden, instruction[1])
                value = garden.plots[garden.current_plot] & 0xFF
                rotated = ((value << degrees) | (value >> (8 - degrees))) & 0xFF
                garden.plots[garden.current_plot] = rotated
                
        except Exception as e:
            print(f"Error at instruction {pc+1}: {e}")
            break
            
        pc += 1
        
    print("Final Harvest:", garden.get_harvest())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gardeners_script.py <filename.garden>")
        sys.exit(1)
        
    with open(sys.argv[1], 'r') as f:
        source = f.read()
        
    program = parse_program(source)
    execute(program)