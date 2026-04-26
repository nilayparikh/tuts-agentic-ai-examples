"""CleanLoop — A Self-Healing Data Engineer Agent.

This is the complete example project for the Self-Improving Agents course.
CleanLoop autonomously cleans messy CSV files by iteratively rewriting its
own code until all binary assertions pass.

Course alignment:
    - Lesson 03: arena and baseline (`.input/`, `.gold/`, `prepare.py`)
    - Lesson 04: orchestrator loop (`loop.py`)
    - Lesson 05: genome improvement (`clean_data.py`)
    - Lesson 06: observability (`dashboard.py`, history artifacts)
    - Lesson 07: self-challenging (`challenger.py`)
    - Lesson 08: test-time search (`reranker.py`)
    - Lesson 09: safety and autonomy (`sandbox.py`, `autonomy.py`)

Usage:
    cd cleanloop
    python util.py verify                 # Verify local environment + LLM access
    python util.py loop                   # Run the self-improving loop
    python util.py evaluate               # Evaluate the current genome output
    python util.py challenge --levels 1   # Generate adversarial data
    python util.py dashboard              # Launch monitoring dashboard
    python util.py sandbox --timeout 10   # Run genome in isolation
    python util.py autonomy --rounds 5    # Graduated trust simulation
    python util.py reset                  # Restore the starter genome
"""
