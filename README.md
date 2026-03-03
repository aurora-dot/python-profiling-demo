# Python Profiling Demo

Demo programs showing how to use **pyinstrument** (CPU profiler) and **memray** (memory profiler).


## Setup

```bash
# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate
```

## Usage

```bash
# Show help
python-profile-demo --help

# Show profiling tools guide
python-profile-demo --guide

# Run time complexity demo
python-profile-demo --run-time-complex-code

# Run memory consumption demo
python-profile-demo --run-memory-complex-code

# Run both
python-profile-demo --run-time-complex-code --run-memory-complex-code
```

## Output Files

Each demo generates:
- `*_profile_pyinstrument.html` - Interactive HTML report
- `*_profile_pyinstrument.json` - Speedscope format (view with `speedscope`)
- `*_profile_memray.bin` - Memory profile (view with `memray flamegraph`)

## Viewing Results

```bash
# Pyinstrument HTML (opens in browser)
open time_profile_pyinstrument.html

# Speedscope (interactive flame graph)
speedscope time_profile_pyinstrument.json

# Memray flamegraph
memray flamegraph time_profile_memray.bin
memray stats time_profile_memray.bin
memray tree time_profile_memray.bin
```

