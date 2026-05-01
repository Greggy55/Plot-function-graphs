# Plot-function-graphs
A small Python program for rendering text-based function graphs in the console.

## Prerequisites
- Python 3.8 or later
- No external dependencies required (uses the standard library only)

## Run the project
1. Open a terminal.
2. Change to the project directory:
   ```bash
   cd /path/to/Plot-function-graphs
   ```
3. Run the script:
   ```bash
   python draw.py
   ```

## Usage
When you run `draw.py`, the program will prompt you for:
- `Enter a function f(x) =` — a math expression in terms of `x`
- `Enter domain start:` — integer start value for the x domain
- `Enter domain end:` — integer end value for the x domain
- `Enter x axis scale:` — numeric scale factor for x values
- `Enter y axis scale:` — numeric scale factor for y values

The program accepts expressions such as:
- `x^2`
- `sin(x)`
- `cos(x)`
- `sqrt(x)`
- `abs(x)`
- `fact(x)`
- `gamma(x)`

## Example
```text
Enter a function f(x) = x^2
Enter domain start: -2
Enter domain end: 2
Enter x axis scale: 5
Enter y axis scale: 5
```

The script will then print a text-based graph using `*` for points and `|` / `-` for the axes.

## Notes
- Use Python-style function notation where needed.
- Multiplication is inferred in many cases, but explicit `*` can improve reliability.
- If parentheses are mismatched or unsupported characters are used, the program will ask you to correct the function format.

