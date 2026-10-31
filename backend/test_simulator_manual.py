
from app.simulation.simulator import simulate_circuit


# Test 1: X gate
x_circuit = {
    "qubits": 1,
    "gates": [
        {"name": "x", "qubits": [0]}
    ]
}

x_result = simulate_circuit(
    x_circuit,
    shots=1024,
)

print("\nTEST 1: X GATE")
print(x_result["measurements"]["counts"])


# Test 2: Hadamard gate
h_circuit = {
    "qubits": 1,
    "gates": [
        {"name": "h", "qubits": [0]}
    ]
}

h_result = simulate_circuit(
    h_circuit,
    shots=1024,
)

print("\nTEST 2: HADAMARD GATE")
print(h_result["measurements"]["counts"])


# Test 3: Bell state
bell_circuit = {
    "qubits": 2,
    "gates": [
        {"name": "h", "qubits": [0]},
        {"name": "cx", "qubits": [0, 1]}
    ]
}

bell_result = simulate_circuit(
    bell_circuit,
    shots=1024,
)

print("\nTEST 3: BELL STATE")
print(bell_result["measurements"]["counts"])

print("\nSTATEVECTOR")
print(bell_result["statevector"])
