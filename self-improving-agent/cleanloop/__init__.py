"""CleanLoop — A Self-Healing Data Engineer Agent.

This is the complete example project for the Self-Improving Agents course.
CleanLoop autonomously cleans messy CSV files by iteratively rewriting its
own code until all binary assertions pass.

Course alignment:
    - Lesson 01: mutation engine (`util.py`, `verify.py`, `status_snapshot.py`)
    - Lesson 02: pipeline genome (`clean_data.py`, `clean_data_runtime.py`)
    - Lesson 03: orchestrator loop (`loop.py`)
    - Lesson 04: observability (`dashboard.py`, history artifacts)
    - Lesson 05: fixed judge and self-challenging (`prepare.py`, `challenger.py`)
    - Lesson 06: test-time search (`reranker.py`)
    - Lesson 07: production safety (`sandbox.py`, `autonomy.py`, `reset_workflow.py`)

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
