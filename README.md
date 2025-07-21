# Gardeners' Script

Gardeners' Script is an esoteric programming language (esolang) that uses gardening metaphors as its core programming paradigm. Variables become plots, operations become gardening tasks, and program flow mimics the seasonal cycles of a garden.

## Key Features
- **Gardening Metaphors**: All programming concepts map to gardening activities
- **Plot-based Variables**: Store values in named garden plots
- **Greenhouse Stack**: Temporary storage for plot values
- **Harvest Output**: Collect program output through harvest commands
- **Seasonal Loops**: `bloom` and `wither` commands for loop control

## Online Interpreter
Try Gardeners' Script in your browser:  
[Online Interpreter](https://garden.mzums.hackclub.app/)

## Documentation
Full language documentation is available at:  
[Documentation](https://garden.mzums.hackclub.app/documentation)

## Installation
To run Gardeners' Script locally:
```bash
python garden_interpreter.py your_program
```

## Core Concepts

### Plots (Variables)
Plots store values and come in two types:
- **Integer Plots**: Store numerical values
- **String Plots**: Store text values

### Gardening Commands
| Command | Example | Description |
|---------|---------|-------------|
| `plant` | `plant rose 5` | Create a new plot with initial value |
| `tend`  | `tend rose` | Set current plot for operations |
| `water` | `water 3` | Increase current plot value |
| `prune` | `prune 2` | Decrease current plot value |
| `graft` | `graft 4` | Multiply current plot value |
| `divide`| `divide 2` | Divide current plot value |
| `concat`| `concat lily` | Concatenate string plots |
| `slice` | `slice 0 5` | Slice string plot |

## Example Programs

### Hello World
```garden
plant msg "Hello, World!"
tend msg
harvest msg
```

### Basic arithmetic operations
```plant a 10
plant b 5

tend a
water 15     # a = 10 + 15 = 25
prune 7      # a = 25 - 7 = 18
harvest a

tend b
graft 3      # b = 5 * 3 = 15
divide 2     # b = 15 / 2 = 7 (integer division)
harvest b
```

### Fibonacci Sequence
```garden
plant a 0
plant b 1
plant count 10
plant temp 0
plant step 1

harvest a
harvest b

bloom count FibLoop

label FibLoop
tend a
store
tend b
store

tend a
retrieve
tend temp
retrieve

tend b
water temp
tend b
harvest

tend count
prune step
wither
```

### Function Example
```garden
function test [a] {
    return 42
}

call test 0
harvest return
```

## Language Specification
- **Case-insensitive** commands
- **#** for single-line comments
- **" "** for string literals
- **Functions** defined with `function` keyword and braces

## Resources
- [Online Interpreter](https://garden.mzums.hackclub.app/)
- [Official Documentation](https://garden.mzums.hackclub.app/documentation)
