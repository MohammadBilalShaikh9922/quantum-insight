"""
QuantumInsight - Quantum Circuit Simulation Engine

Supports:
- Ideal quantum circuit simulation
- Depolarizing noise
- Bit-flip noise
- Phase-flip noise
- Measurement errors

Submitted Python source code is never executed.
Only the output of the existing static parser is used.
"""

from typing import Any

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    ReadoutError,
    depolarizing_error,
    pauli_error,
)


# ---------------------------------------------------------
# SUPPORTED GATES
# ---------------------------------------------------------

SINGLE_QUBIT_GATES = {
    "h", "x", "y", "z", "s", "sdg", "t", "tdg"
}

TWO_QUBIT_GATES = {
    "cx", "cy", "cz", "ch", "swap", "iswap"
}

THREE_QUBIT_GATES = {
    "ccx", "cswap"
}

PARAMETERIZED_GATES = {
    "rx", "ry", "rz", "p", "u", "u1", "u2", "u3",
    "crx", "cry", "crz", "cp", "rxx", "ryy", "rzz"
}


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

def validate_shots(shots: int) -> int:
    if isinstance(shots, bool) or not isinstance(shots, int):
        raise ValueError("Shots must be an integer.")

    if shots < 1 or shots > 1_000_000:
        raise ValueError(
            "Shots must be between 1 and 1,000,000."
        )

    return shots


def validate_probability(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number.")

    value = float(value)

    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1.")

    return value


def validate_parsed_circuit(
    parsed: dict[str, Any],
) -> tuple[int, list[dict[str, Any]]]:

    if not isinstance(parsed, dict):
        raise ValueError("Invalid parsed circuit.")

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
        raise ValueError("Invalid circuit gate list.")

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
                    "the circuit range."
                )

    return qubits, gates


# ---------------------------------------------------------
# CIRCUIT RECONSTRUCTION
# ---------------------------------------------------------

def build_circuit(
    parsed: dict[str, Any],
) -> QuantumCircuit:

    qubit_count, gates = validate_parsed_circuit(parsed)

    circuit = QuantumCircuit(qubit_count)

    for position, gate in enumerate(gates):

        name = gate["name"].lower()
        indices = gate["qubits"]

        if name in {"measure", "measure_all"}:
            continue

        if name == "barrier":

            if indices:
                circuit.barrier(*indices)
            else:
                circuit.barrier()

            continue

        if name == "reset":

            if not indices:
                raise ValueError(
                    "Reset operation has no target qubit."
                )

            for qubit in indices:
                circuit.reset(qubit)

            continue

        if name in PARAMETERIZED_GATES:
            raise ValueError(
                f"Gate '{name}' requires numerical parameters. "
                "Parameterized gate support will be added "
                "after extending the circuit parser."
            )

        if name in SINGLE_QUBIT_GATES:

            if len(indices) != 1:
                raise ValueError(
                    f"Gate '{name}' requires exactly one qubit."
                )

            getattr(circuit, name)(indices[0])
            continue

        if name in TWO_QUBIT_GATES:

            if len(indices) != 2:
                raise ValueError(
                    f"Gate '{name}' requires exactly two qubits."
                )

            if indices[0] == indices[1]:
                raise ValueError(
                    f"Gate '{name}' cannot use the same qubit twice."
                )

            getattr(circuit, name)(indices[0], indices[1])
            continue

        if name in THREE_QUBIT_GATES:

            if len(indices) != 3:
                raise ValueError(
                    f"Gate '{name}' requires exactly three qubits."
                )

            if len(set(indices)) != 3:
                raise ValueError(
                    f"Gate '{name}' requires three distinct qubits."
                )

            getattr(circuit, name)(*indices)
            continue

        raise ValueError(
            f"Unsupported gate '{name}' at position {position}."
        )

    return circuit


# ---------------------------------------------------------
# IDEAL STATEVECTOR
# ---------------------------------------------------------

def calculate_statevector(
    circuit: QuantumCircuit,
) -> dict[str, Any] | None:

    if any(
        instruction.operation.name == "reset"
        for instruction in circuit.data
    ):
        return None

    state = Statevector.from_instruction(circuit)

    amplitudes = []

    for index, amplitude in enumerate(state.data):

        amplitudes.append({
            "basis_state": format(
                index,
                f"0{circuit.num_qubits}b",
            ),
            "real": float(amplitude.real),
            "imaginary": float(amplitude.imag),
            "probability": float(abs(amplitude) ** 2),
        })

    return {
        "dimension": len(state.data),
        "amplitudes": amplitudes,
    }


# ---------------------------------------------------------
# IDEAL MEASUREMENT SIMULATION
# ---------------------------------------------------------

def simulate_measurements(
    circuit: QuantumCircuit,
    shots: int = 1024,
) -> dict[str, Any]:

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
# IDEAL SIMULATION
# ---------------------------------------------------------

def simulate_circuit(
    parsed: dict[str, Any],
    shots: int = 1024,
) -> dict[str, Any]:

    shots = validate_shots(shots)

    circuit = build_circuit(parsed)

    statevector = calculate_statevector(circuit)

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


# ---------------------------------------------------------
# NOISE ERROR GENERATOR
# ---------------------------------------------------------

def create_quantum_error(
    noise_type: str,
    probability: float,
    qubit_count: int,
):

    if probability == 0:
        return None

    if noise_type == "depolarizing":

        return depolarizing_error(
            probability,
            qubit_count,
        )

    if noise_type == "bit_flip":

        error = pauli_error([
            ("X", probability),
            ("I", 1 - probability),
        ])

    elif noise_type == "phase_flip":

        error = pauli_error([
            ("Z", probability),
            ("I", 1 - probability),
        ])

    else:
        raise ValueError(
            "Unsupported noise type. Choose depolarizing, "
            "bit_flip, or phase_flip."
        )

    combined_error = error

    for _ in range(qubit_count - 1):
        combined_error = combined_error.tensor(error)

    return combined_error


# ---------------------------------------------------------
# NOISE MODEL BUILDER
# ---------------------------------------------------------

def build_noise_model(
    noise_type: str = "depolarizing",
    gate_error_probability: float = 0.01,
    measurement_error_probability: float = 0.02,
) -> NoiseModel:

    allowed_types = {
        "depolarizing",
        "bit_flip",
        "phase_flip",
    }

    if noise_type not in allowed_types:
        raise ValueError(
            "Noise type must be depolarizing, bit_flip, "
            "or phase_flip."
        )

    gate_error_probability = validate_probability(
        gate_error_probability,
        "Gate error probability",
    )

    measurement_error_probability = validate_probability(
        measurement_error_probability,
        "Measurement error probability",
    )

    noise_model = NoiseModel()

    # Apply one-qubit noise to supported one-qubit gates.
    one_qubit_error = create_quantum_error(
        noise_type,
        gate_error_probability,
        1,
    )

    if one_qubit_error is not None:
        noise_model.add_all_qubit_quantum_error(
            one_qubit_error,
            sorted(SINGLE_QUBIT_GATES),
        )

    # Apply two-qubit noise to supported two-qubit gates.
    two_qubit_error = create_quantum_error(
        noise_type,
        gate_error_probability,
        2,
    )

    if two_qubit_error is not None:
        noise_model.add_all_qubit_quantum_error(
            two_qubit_error,
            sorted(TWO_QUBIT_GATES),
        )

    # Apply three-qubit noise to supported three-qubit gates.
    three_qubit_error = create_quantum_error(
        noise_type,
        gate_error_probability,
        3,
    )

    if three_qubit_error is not None:
        noise_model.add_all_qubit_quantum_error(
            three_qubit_error,
            sorted(THREE_QUBIT_GATES),
        )

    # Add measurement readout errors.
    if measurement_error_probability > 0:

        readout_error = ReadoutError([
            [
                1 - measurement_error_probability,
                measurement_error_probability,
            ],
            [
                measurement_error_probability,
                1 - measurement_error_probability,
            ],
        ])

        noise_model.add_all_qubit_readout_error(
            readout_error
        )

    return noise_model


# ---------------------------------------------------------
# NOISY SIMULATION
# ---------------------------------------------------------

def simulate_noisy_circuit(
    parsed: dict[str, Any],
    shots: int = 1024,
    noise_type: str = "depolarizing",
    gate_error_probability: float = 0.01,
    measurement_error_probability: float = 0.02,
) -> dict[str, Any]:

    shots = validate_shots(shots)

    circuit = build_circuit(parsed)

    noise_model = build_noise_model(
        noise_type=noise_type,
        gate_error_probability=gate_error_probability,
        measurement_error_probability=measurement_error_probability,
    )

    measured_circuit = circuit.copy()
    measured_circuit.measure_all()

    simulator = AerSimulator(
        noise_model=noise_model
    )

    compiled_circuit = transpile(
        measured_circuit,
        simulator,
    )

    job = simulator.run(
        compiled_circuit,
        shots=shots,
    )

    result = job.result()

    counts = result.get_counts()

    counts = {
        str(state): int(count)
        for state, count in counts.items()
    }

    probabilities = {
        state: round(count / shots, 6)
        for state, count in counts.items()
    }

    return {
        "success": True,
        "simulation_type": "noisy",
        "noise_model": {
            "type": noise_type,
            "gate_error_probability": gate_error_probability,
            "measurement_error_probability": measurement_error_probability,
        },
        "qubits": circuit.num_qubits,
        "classical_bits": circuit.num_qubits,
        "shots": shots,
        "statevector": None,
        "measurements": {
            "counts": counts,
            "probabilities": probabilities,
        },
        "note": (
            "Noisy quantum simulation completed using Qiskit Aer. "
            "Statevector is not returned because this simulation "
            "includes a noise model."
        ),
    }


# ---------------------------------------------------------
# IDEAL VS NOISY COMPARISON
# ---------------------------------------------------------

def compare_ideal_and_noisy(
    parsed: dict[str, Any],
    shots: int = 1024,
    noise_type: str = "depolarizing",
    gate_error_probability: float = 0.01,
    measurement_error_probability: float = 0.02,
) -> dict[str, Any]:

    ideal_result = simulate_circuit(
        parsed,
        shots,
    )

    noisy_result = simulate_noisy_circuit(
        parsed,
        shots,
        noise_type,
        gate_error_probability,
        measurement_error_probability,
    )

    ideal_counts = ideal_result["measurements"]["counts"]
    noisy_counts = noisy_result["measurements"]["counts"]

    all_states = sorted(
        set(ideal_counts) | set(noisy_counts)
    )

    comparison = []

    for state in all_states:

        ideal_probability = ideal_counts.get(state, 0) / shots
        noisy_probability = noisy_counts.get(state, 0) / shots

        comparison.append({
            "state": state,
            "ideal_probability": round(ideal_probability, 6),
            "noisy_probability": round(noisy_probability, 6),
            "absolute_difference": round(
                abs(ideal_probability - noisy_probability),
                6,
            ),
        })

    return {
        "success": True,
        "message": "Ideal and noisy simulations compared successfully.",
        "ideal": ideal_result,
        "noisy": noisy_result,
        "comparison": comparison,
    }
