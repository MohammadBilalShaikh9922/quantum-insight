
"""
Temporary QuantumInsight simulator verification endpoint.

This endpoint tests:
1. X gate
2. Hadamard gate
3. Bell state

It requires authentication and uses the existing
static Qiskit parser and simulation engine.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.auth import current_user
from app.circuit.parser import parse_qiskit_code
from app.simulation.simulator import simulate_circuit


router = APIRouter(tags=["simulation-test"])


def run_test(name: str, source_code: str, shots: int = 1024):
    """
    Parse and simulate one test circuit.
    """

    try:
        parsed, parser_mode = parse_qiskit_code(source_code)

        result = simulate_circuit(
            parsed,
            shots=shots,
        )

        return {
            "name": name,
            "parser": parser_mode,
            "result": result,
        }

    except Exception as exc:
        return {
            "name": name,
            "success": False,
            "error": str(exc),
        }


@router.get("/simulation-test")
def simulation_test(user=Depends(current_user)):
    """
    Run three standard quantum simulation tests.

    Requires a valid QuantumInsight login token.
    """

    shots = 1024

    # -------------------------------------------------
    # TEST 1: X GATE
    # Expected: 100% measurement outcome 1.
    # -------------------------------------------------

    x_code = """
from qiskit import QuantumCircuit

qc = QuantumCircuit(1)
qc.x(0)
"""

    x_test = run_test(
        "X Gate",
        x_code,
        shots,
    )

    # -------------------------------------------------
    # TEST 2: HADAMARD GATE
    # Expected: approximately 50% 0 and 50% 1.
    # -------------------------------------------------

    h_code = """
from qiskit import QuantumCircuit

qc = QuantumCircuit(1)
qc.h(0)
"""

    h_test = run_test(
        "Hadamard Gate",
        h_code,
        shots,
    )

    # -------------------------------------------------
    # TEST 3: BELL STATE
    # Expected: approximately 50% 00 and 50% 11.
    # -------------------------------------------------

    bell_code = """
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
"""

    bell_test = run_test(
        "Bell State",
        bell_code,
        shots,
    )

    # -------------------------------------------------
    # VALIDATE RESULTS
    # -------------------------------------------------

    tests = [
        x_test,
        h_test,
        bell_test,
    ]

    for test in tests:
        if "result" in test:
            test["success"] = test["result"]["success"]

    # X gate validation
    if x_test.get("success"):
        x_counts = x_test["result"]["measurements"]["counts"]

        x_passed = (
            sum(x_counts.values()) == shots
            and x_counts.get("1", 0) == shots
        )
    else:
        x_passed = False

    # Hadamard validation
    if h_test.get("success"):
        h_counts = h_test["result"]["measurements"]["counts"]

        zero_ratio = h_counts.get("0", 0) / shots
        one_ratio = h_counts.get("1", 0) / shots

        h_passed = (
            0.40 <= zero_ratio <= 0.60
            and 0.40 <= one_ratio <= 0.60
        )
    else:
        h_passed = False

    # Bell state validation
    if bell_test.get("success"):
        bell_counts = bell_test["result"]["measurements"]["counts"]

        bell_passed = (
            sum(bell_counts.values()) == shots
            and set(bell_counts).issubset({"00", "11"})
            and 0.40 <= bell_counts.get("00", 0) / shots <= 0.60
            and 0.40 <= bell_counts.get("11", 0) / shots <= 0.60
        )
    else:
        bell_passed = False

    test_status = {
        "x_gate": x_passed,
        "hadamard_gate": h_passed,
        "bell_state": bell_passed,
    }

    all_passed = all(test_status.values())

    return {
        "success": all_passed,
        "message": (
            "All quantum simulator tests passed."
            if all_passed
            else "One or more quantum simulator tests failed."
        ),
        "shots_per_test": shots,
        "tests": test_status,
        "details": tests,
    }
