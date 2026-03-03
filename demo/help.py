"""
Help documentation for profiling tools: pyinstrument and memray
"""

from rich.console import Console
from rich.markdown import Markdown


def print_help():
    """Print comprehensive help for using pyinstrument and memray."""

    help_text = """
# PROFILING TOOLS HELP

This guide covers how to use **pyinstrument** and **memray** for profiling Python code.

---

## PYINSTRUMENT - CPU/TIME PROFILER

Pyinstrument is a statistical CPU profiler that shows where time is spent in
your code. It uses call stacks to build a hierarchical view of execution time.

### BASIC USAGE IN CODE

```python
from pyinstrument import Profiler

profiler = Profiler()
profiler.start()

# Your code here
my_slow_function()

profiler.stop()

# Print to console
print(profiler.output_text(unicode=True, color=True))

# Save HTML report
with open("profile.html", "w") as f:
    f.write(profiler.output_html())
```

### COMMAND LINE USAGE

```bash
# Profile a script
pyinstrument my_script.py

# Profile a module
pyinstrument -m my_module

# Save HTML output
pyinstrument -o profile.html -r html my_script.py

# Save speedscope JSON (for interactive visualization)
pyinstrument -o profile.json -r speedscope my_script.py

# Show output in console
pyinstrument --unicode my_script.py
```

### OUTPUT FORMATS

- **Text**: Terminal-friendly output with unicode box drawing
- **HTML**: Interactive web report with collapsible call stacks
- **JSON**: Machine-readable format
- **Speedscope**: JSON format for speedscope.app visualization

**Command line:**
```bash
# Generate speedscope JSON
pyinstrument -o profile.json -r speedscope my_script.py

# View with speedscope (install: npm install -g speedscope)
speedscope profile.json
```

**In code:**
```python
from pyinstrument.renderers import SpeedscopeRenderer

# Export for speedscope
with open("profile.json", "w") as f:
    f.write(profiler.output(SpeedscopeRenderer()))
```

### INTERPRETING RESULTS

- **Time %**: Percentage of total execution time
- **Function names**: Indented to show call hierarchy
- **Hot paths**: Functions taking the most time are highlighted
- **Self time**: Time spent in the function itself (not children)

### WHEN TO USE

✓ Code is running slowly
✓ Need to identify performance bottlenecks
✓ Want to see which functions take the most time
✓ Optimizing for speed/latency

---

## MEMRAY - MEMORY PROFILER

Memray is a memory profiler that tracks allocations at the C level. It shows
where memory is allocated, how much, and can detect memory leaks.

### BASIC USAGE IN CODE

```python
import memray

# Basic tracking
with memray.Tracker("output.bin"):
    # Your code here
    my_memory_intensive_function()

# For accurate leak detection, enable Python allocator tracking
with memray.Tracker("output.bin", trace_python_allocators=True):
    my_memory_intensive_function()

# Then analyze with CLI tools (see below)
```

### COMMAND LINE USAGE

```bash
# Run and track a script
memray run -o output.bin my_script.py

# Run with Python allocator tracking (recommended for leak detection)
memray run --trace-python-allocators -o output.bin my_script.py

# Run and track a module
memray run -o output.bin -m my_module
```

### ANALYZING RESULTS

After capturing a profile, use these commands to analyze:

1. **FLAMEGRAPH** - Visual flame graph (opens in browser)
   ```bash
   memray flamegraph output.bin
   ```

2. **TABLE** - Tabular view of allocations
   ```bash
   memray table output.bin
   ```

3. **TREE** - Interactive tree view of call stacks
   ```bash
   memray tree output.bin
   ```

4. **STATS** - Summary statistics
   ```bash
   memray stats output.bin
   ```
   Shows:
   - Total allocations
   - Total memory allocated
   - Peak memory usage
   - Allocation size histogram
   - Top allocating locations

5. **SUMMARY** - High-level overview
   ```bash
   memray summary output.bin
   ```

### FLAMEGRAPH OPTIONS

```bash
# Temporary flame graph (opens browser, cleans up after)
memray flamegraph output.bin

# Save flame graph HTML
memray flamegraph -o report.html output.bin

# Force overwrite existing file
memray flamegraph -f -o report.html output.bin

# Show leaks only
memray flamegraph --leaks output.bin
```

### ADVANCED OPTIONS

```bash
# Track allocations over time
memray run --temporal -o output.bin script.py

# Follow forked processes
memray run --follow-fork -o output.bin script.py

# Aggregate by function (not line)
memray run --aggregate -o output.bin script.py

# Native mode (track C extensions)
memray run --native -o output.bin script.py
```

### INTERPRETING RESULTS

- **Wide bars in flamegraph** = lots of memory allocated
- **Height of stack** = call depth
- **Color coding** shows different code paths
- **Hover** for details (function name, file, line, size)

### MEMORY LEAK DETECTION

**IMPORTANT**: For accurate leak detection, you **must** use `--trace-python-allocators`:

```bash
# Run with Python allocator tracking (required for accurate leak detection)
memray run --trace-python-allocators -o output.bin script.py

# Show only leaked allocations
memray flamegraph --leaks output.bin
```

**Why is this flag needed?**
Without `--trace-python-allocators`, Python's pymalloc allocator retains memory in pools
even after objects are deallocated. Memray cannot distinguish memory set aside for reuse
from truly leaked memory, leading to false positives.

Leaked memory appears as allocations that:
- Were never freed
- Still have references preventing garbage collection
- Accumulate over time (not temporary allocations)

### WHEN TO USE

✓ High memory usage / out of memory errors
✓ Suspected memory leaks
✓ Need to reduce memory footprint
✓ Debugging memory growth over time
✓ Optimizing for memory efficiency

---

## COMPARING THE TWO

|             | PYINSTRUMENT           | MEMRAY                  |
|-------------|------------------------|-------------------------|
| Measures    | Time/CPU usage         | Memory allocations      |
| Overhead    | Low (~2-5%)            | Very low (~1%)          |
| Output      | HTML, JSON, text       | Binary → HTML/text      |
| Use Case    | Slow code              | High memory usage       |
| Best For    | Performance tuning     | Memory optimization     |
| Shows       | Time per function      | Allocation size/count   |

**TIP**: Use both together! Profile time first (cheaper), then memory if needed.

---

## SPEEDSCOPE INTEGRATION

Speedscope is a fast, interactive flame graph viewer for performance profiles.

### INSTALLATION

```bash
npm install -g speedscope
```

### USAGE

```bash
# View a profile (opens local web server)
speedscope profile.json

# Specify port
speedscope -p 8080 profile.json
```

### EXPORTING FROM PYINSTRUMENT

**Command line:**
```bash
# Generate speedscope JSON directly
pyinstrument -o profile.json -r speedscope my_script.py

# Then view it
speedscope profile.json
```

**In code:**
```python
from pyinstrument.renderers import SpeedscopeRenderer

with open("profile.json", "w") as f:
    f.write(profiler.output(SpeedscopeRenderer()))

# Then view it
speedscope profile.json
```

---

## QUICK REFERENCE

### PYINSTRUMENT
```bash
Profile:    pyinstrument script.py
HTML out:   pyinstrument -o report.html -r html script.py
Speedscope: pyinstrument -o profile.json -r speedscope script.py
```

### MEMRAY
```bash
Capture:    memray run -o output.bin script.py
Leaks:      memray run --trace-python-allocators -o output.bin script.py
Flamegraph: memray flamegraph output.bin
Leaks view: memray flamegraph --leaks output.bin
Stats:      memray stats output.bin
Tree:       memray tree output.bin
Table:      memray table output.bin
```

### SPEEDSCOPE
```bash
Install:    npm install -g speedscope
View:       speedscope profile.json
```

---

## For more information

- **Pyinstrument**: https://github.com/joerick/pyinstrument
- **Memray**: https://github.com/bloomberg/memray
- **Speedscope**: https://github.com/jlfwong/speedscope
"""

    console = Console()
    md = Markdown(help_text)

    # Use Rich's pager with Markdown rendering
    with console.pager(styles=True):
        console.print(md)


if __name__ == "__main__":
    print_help()
