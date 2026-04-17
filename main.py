from simulation import Simulation


def run_with_visuals():
    """Single run with live visualisation"""
    sim = Simulation()
    sim.run(max_turns=50)


def run_without_visuals():
    """Single run text only - no graphics"""
    import io
    import sys
    sim = Simulation()

    # Temporarily disable visualiser
    old_stdout = sys.stdout
    sim.run(max_turns=50)


if __name__ == "__main__":
    print("=" * 50)
    print("PROJECT HAIL MARY SIMULATION")
    print("=" * 50)
    print("\nChoose mode:")
    print("1. Run with live visualisation")
    print("2. Run statistics (20 runs, no graphics)")
    print("3. Single run text only")

    choice = input("\nEnter choice (1/2/3): ").strip()

    if choice == "1":
        run_with_visuals()
    elif choice == "2":
        from run_statistics import run_multiple_simulations
        from run_statistics import print_statistics
        from run_statistics import plot_statistics
        results = run_multiple_simulations(20)
        print_statistics(results, 20)
        plot_statistics(results, 20)
    elif choice == "3":
        sim = Simulation()
        sim.run(max_turns=50)
    else:
        print("Invalid choice!")