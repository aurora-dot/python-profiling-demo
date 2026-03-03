"""
CLI entry point for profiling demos
"""

import argparse
import sys


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="python-profile-demo",
        description="Profiling demos for pyinstrument and memray",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python-profile-demo --help                       # Show this help
  python-profile-demo --guide                      # Show comprehensive profiling tools guide
  python-profile-demo --run-time-complex-code      # Run time profiling demo
  python-profile-demo --run-memory-complex-code    # Run memory profiling demo
  python-profile-demo --run-time-complex-code --run-memory-complex-code  # Run both
        """,
    )

    parser.add_argument(
        "--guide",
        action="store_true",
        help="Show comprehensive guide for using pyinstrument and memray (usage, output formats, interpretation)",
    )

    parser.add_argument(
        "--run-time-complex-code",
        action="store_true",
        help="Run time complexity profiling demo (O(n²), O(n³) algorithms)",
    )

    parser.add_argument(
        "--run-memory-complex-code",
        action="store_true",
        help="Run memory consumption profiling demo (with memory leaks)",
    )

    args = parser.parse_args()

    # If --guide requested, show comprehensive profiling tools help
    if args.guide:
        from demo.help import print_help

        print_help()
        return 0

    # If no demo arguments provided, show regular help
    if not args.run_time_complex_code and not args.run_memory_complex_code:
        parser.print_help()
        return 0

    # Run the requested demos
    ran_something = False

    if args.run_time_complex_code:
        print("\n" + "=" * 80)
        print("RUNNING TIME COMPLEXITY DEMO")
        print("=" * 80 + "\n")
        from demo.time import main as time_main

        time_main()
        ran_something = True

    if args.run_memory_complex_code:
        if ran_something:
            print("\n\n")  # Space between demos
        print("\n" + "=" * 80)
        print("RUNNING MEMORY CONSUMPTION DEMO")
        print("=" * 80 + "\n")
        from demo.memory import main as memory_main

        memory_main()
        ran_something = True

    return 0


if __name__ == "__main__":
    sys.exit(main())
