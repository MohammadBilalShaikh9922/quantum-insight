
"""
QuantumInsight - Quantum Circuit Simulation Engine

This module reconstructs a Qiskit QuantumCircuit from the
existing static parser output.

Important:
- Submitted Python source code is never executed.
- Only parsed gate names and qubit indices are used.
- Parameterized gates are rejected until the parser supports
  safely extracting their numerical parameters.
"""

from typing import Any

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator


# ---------------------------------------------------------
# SUPPORTED PARAMETER-FREE GATES
# ---------------------------------------------------------

SINGLE_QUBIT_GATES = {
    "h",
    "x",
    "y",
    "z",
    "s",
    "sdg",
    "t",
    "tdg",
}

TWO_QUBIT_GATES = {
    "cx",
    "cy",
    "cz",
    "ch",
    "swap",
    "iswap",
}

THREE_QUBIT_GATES = {
    "ccx",
    "cswap",
}

PARAMETERIZED_GATES = {
    "rx",
    "ry",
    "rz",
    "p",
    "u",
    "u1",
    "u2",
    "u3",
    "crx",
    "cry",
    "crz",
    "cp",
    "rxx",
    "ryy",
    "rzz",
}


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

def validate_shots(shots: int) -> int:
    """
    Validate the number of measurement shots.
    """

    if isinstance(shots, bool) or not isinstance(shots, int):
        raise ValueError(
            "Shots must be an integer."
        )

    if shots < 1 or shots > 1_000_000:
        raise ValueError(
            "Shots must be between 1 and 1,000,000."
        )

    return shots


def validate_parsed_circuit(
    parsed: dict[str, Any],
) -> tuple[int, list[dict[str, Any]]]:
    """
    Validate the structure returned by parse_qiskit_code().
    """

    if not isinstance(parsed, dict):
        raise ValueError(
            "Invalid parsed circuit."
        )

    qubits = parsed.get("qubits")
    gates = parsed.get("gates")

    if (
        isinstance(qubits, bool)
        or not isinstance(qubits, int)
        or qubits < 1
    ):
        raise ValueError(
            "Circuit must contain at least one qubit."
        )

    if qubits > 30:
        raise ValueError(
            "Simulation is limited to 30 qubits."
        )

    if not isinstance(gates, list):
        raise ValueError(
            "Invalid circuit gate list."
        )

    for index, gate in enumerate(gates):

        if not isinstance(gate, dict):
            raise ValueError(
                f"Invalid gate at position {index}."
            )

        name = gate.get("name")
        indices = gate.get("qubits")

        if not isinstance(name, str):
            raise ValueError(
                f"Invalid gate name at position {index}."
            )

        if not isinstance(indices, list):
            raise ValueError(
                f"Invalid qubit list for gate {name}."
            )

        for qubit in indices:

            if (
                isinstance(qubit, bool)
                or not isinstance(qubit, int)
            ):
                raise ValueError(
                    f"Invalid qubit index for gate {name}."
                )

            if qubit < 0 or qubit >= qubits:
                raise ValueError(
                    f"Qubit index {qubit} is outside "
                    f"the circuit range."
                )

    return qubits, gates


# ---------------------------------------------------------
# CIRCUIT RECONSTRUCTION
# ---------------------------------------------------------

def build_circuit(
    parsed: dict[str, Any],
) -> QuantumCircuit:
    """
    Reconstruct a Qiskit QuantumCircuit from parser output.

    The function does not execute submitted Python code.

    Measurement operations are deferred and applied consistently
    to all qubits during simulation.
    """

    qubit_count, gates = validate_parsed_circuit(
        parsed
    )

    circuit = QuantumCircuit(qubit_count)

    for position, gate in enumerate(gates):

        name = gate["name"].lower()
        indices = gate["qubits"]

        # -------------------------------------------------
        # Ignore measurements here.
        #
        # The simulation engine applies measure_all()
        # after reconstructing the quantum operations.
        # -------------------------------------------------

        if name in {
            "measure",
            "measure_all",
        }:
            continue

        # -------------------------------------------------
        # Ignore empty barriers.
        # -------------------------------------------------

        if name == "barrier":

            if indices:
                circuit.barrier(*indices)
            else:
                circuit.barrier()

            continue

        # -------------------------------------------------
        # Reset operation.
        # -------------------------------------------------

        if name == "reset":

            if not indices:
                raise ValueError(
                    "Reset operation has no target qubit."
                )

            for qubit in indices:
                circuit.reset(qubit)

            continue

        # -------------------------------------------------
        # Parameterized gates.
        #
        # The existing parser does not preserve rotation
        # angles, so these must not be simulated yet.
        # -------------------------------------------------

        if name in PARAMETERIZED_GATES:

            raise ValueError(
                f"Gate '{name}' requires numerical parameters. "
                "Parameterized gate support will be added "
                "after extending the circuit parser."
            )

        # -------------------------------------------------
        # One-qubit gates.
        # -------------------------------------------------

        if name in SINGLE_QUBIT_GATES:

            if len(indices) != 1:
                raise ValueError(
                    f"Gate '{name}' requires exactly one qubit."
                )

            getattr(circuit, name)(
                indices[0]
            )

            continue

        # -------------------------------------------------
        # Two-qubit gates.
        # -------------------------------------------------

        if name in TWO_QUBIT_GATES:

            if len(indices) != 2:
                raise ValueError(
                    f"Gate '{name}' requires exactly two qubits."
                )

            if indices[0] == indices[1]:
                raise ValueError(
                    f"Gate '{name}' cannot use the same qubit twice."
                )

            getattr(circuit, name)(
                indices[0],
                indices[1],
            )

            continue

        # -------------------------------------------------
        # Three-qubit gates.
        # -------------------------------------------------

        if name in THREE_QUBIT_GATES:

            if len(indices) != 3:
                raise ValueError(
                    f"Gate '{name}' requires exactly three qubits."
                )

            if len(set(indices)) != 3:
                raise ValueError(
                    f"Gate '{name}' requires three distinct qubits."
                )

            getattr(circuit, name)(
                *indices
            )

            continue

        # -------------------------------------------------
        # Unsupported gate.
        # -------------------------------------------------

        raise ValueError(
            f"Unsupported gate '{name}' at position {position}."
        )

    return circuit


# ---------------------------------------------------------
# STATEVECTOR SIMULATION
# ---------------------------------------------------------

def calculate_statevector(
    circuit: QuantumCircuit,
) -> dict[str, Any] | None:
    """
    Calculate the ideal quantum statevector.

    Statevector calculation is skipped when the circuit
    contains non-unitary operations such as reset.
    """

    if any(
        instruction.operation.name == "reset"
        for instruction in circuit.data
    ):
        return None

    state = Statevector.from_instruction(
        circuit
    )

    amplitudes = []

    for index, amplitude in enumerate(state.data):

        amplitudes.append({
            "basis_state": format(
                index,
                f"0{circuit.num_qubits}b",
            ),
            "real": float(amplitude.real),
            "imaginary": float(amplitude.imag),
            "probability": float(
                abs(amplitude) ** 2
            ),
        })

    return {
        "dimension": len(state.data),
        "amplitudes": amplitudes,
    }


# ---------------------------------------------------------
# MEASUREMENT SIMULATION
# ---------------------------------------------------------

def simulate_measurements(
    circuit: QuantumCircuit,
    shots: int = 1024,
) -> dict[str, Any]:
    """
    Run measurement simulation using Qiskit Aer.
    """

    shots = validate_shots(shots)

    measured_circuit = circuit.copy()

    measured_circuit.measure_all()

    simulator = AerSimulator()

    job = simulator.run(
        measured_circuit,
        shots=shots,
    )

    result = job.result()

    counts = result.get_counts()

    # Convert NumPy/integer-like values to standard Python ints.
    counts = {
        str(state): int(count)
        for state, count in counts.items()
    }

    probabilities = {
        state: round(count / shots, 6)
        for state, count in counts.items()
    }

    return {
        "shots": shots,
        "counts": counts,
        "probabilities": probabilities,
    }


# ---------------------------------------------------------
# MAIN SIMULATION FUNCTION
# ---------------------------------------------------------

def simulate_circuit(
    parsed: dict[str, Any],
    shots: int = 1024,
) -> dict[str, Any]:
    """
    Perform ideal quantum circuit simulation.

    Returns:
    - Circuit information
    - Statevector when available
    - Measurement counts
    - Measurement probabilities
    """

    shots = validate_shots(shots)

    circuit = build_circuit(
        parsed
    )

    statevector = calculate_statevector(
        circuit
    )

    measurements = simulate_measurements(
        circuit,
        shots,
    )

    return {
        "success": True,
        "simulation_type": "ideal",
        "qubits": circuit.num_qubits,
        "classical_bits": circuit.num_qubits,
        "shots": measurements["shots"],
        "statevector": statevector,
        "measurements": {
            "counts": measurements["counts"],
            "probabilities": measurements["probabilities"],
        },
        "note": (
            "Measurement simulation performed using Qiskit Aer. "
            "Statevector is unavailable for circuits containing reset."
            if statevector is None
            else "Ideal simulation completed using Qiskit Aer."
        ),
    }
