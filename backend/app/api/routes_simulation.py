from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.auth import current_user
from app.circuit.parser import parse_qiskit_code
from app.simulation.simulator import (
    simulate_circuit,
    simulate_noisy_circuit,
    compare_ideal_and_noisy,
)

router = APIRouter(tags=["simulation"])


class SimulationRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=50000)
    shots: int = Field(default=1024, ge=1, le=100000)

    # ideal = normal simulation, noisy = noise model,
    # compare = ideal and noisy results together
    simulation_mode: Literal["ideal", "noisy", "compare"] = "ideal"

    noise_type: Literal[
        "depolarizing", "bit_flip", "phase_flip"
    ] = "depolarizing"

    gate_error_probability: float = Field(default=0.01, ge=0, le=1)
    measurement_error_probability: float = Field(default=0.02, ge=0, le=1)


@router.post("/simulate")
def simulate_quantum_circuit(
    request: SimulationRequest,
    user=Depends(current_user)
):
    try:
        parsed, parser_mode = parse_qiskit_code(request.code)

        if request.simulation_mode == "compare":
            result = compare_ideal_and_noisy(
                parsed,
                shots=request.shots,
                noise_type=request.noise_type,
                gate_error_probability=request.gate_error_probability,
                measurement_error_probability=request.measurement_error_probability,
            )

        elif request.simulation_mode == "noisy":
            result = simulate_noisy_circuit(
                parsed,
                shots=request.shots,
                noise_type=request.noise_type,
                gate_error_probability=request.gate_error_probability,
                measurement_error_probability=request.measurement_error_probability,
            )

        else:
            result = simulate_circuit(
                parsed,
                shots=request.shots
            )

        if not result.get("success", False):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Quantum simulation failed.")
            )

        return {
            "success": True,
            "message": "Quantum circuit simulation completed successfully.",
            "parser": parser_mode,
            "simulation_mode": request.simulation_mode,
            "result": result
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
