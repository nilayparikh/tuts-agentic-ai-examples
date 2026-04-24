"""CleanLoop — A Self-Healing Data Engineer Agent.

This is the complete example project for the Self-Improving Agents course.
CleanLoop autonomously cleans messy CSV files by iteratively rewriting its
own code until all binary assertions pass.

Lesson 03 introduces the arena pattern.
Lesson 06 builds the full loop.
Lesson 07 adds the dashboard.
Lesson 09 adds the challenger.
Lesson 10 adds the reranker.
Lesson 11 adds safety controls.

Usage:
    python -m cleanloop.loop              # Run the self-improving loop
    python -m cleanloop.prepare           # Generate messy data + evaluate
    streamlit run cleanloop/dashboard.py  # Launch monitoring dashboard
    python -m cleanloop.challenger        # Generate adversarial data
    python -m cleanloop.reranker          # Best-of-N candidate selection
    python -m cleanloop.sandbox           # Run genome in isolation
    python -m cleanloop.autonomy          # Graduated trust simulation
"""
