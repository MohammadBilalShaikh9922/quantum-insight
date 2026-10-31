
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.auth import current_user
from app.circuit.parser import parse_qiskit_code
from app.simulation.simulator import simulate_circuit

router = APIRouter(tags=["simulation"])


class SimulationRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        max_length=50000,
        description="Qiskit circuit source code"
    )
    shots: int = Field(
        default=1024,
        ge=1,
        le=100000,
        description="Number of measurement shots"
    )


@router.post("/simulate")
def simulate_quantum_circuit(
    request: SimulationRequest,
    user=Depends(current_user)
):
    try:
        # Parse the submitted Qiskit source code
        parsed, parser_mode = parse_qiskit_code(request.code)

        # Run actual quantum simulation
        result = simulate_circuit(
            parsed,
            shots=request.shots
        )

        if not result.get("success", False):
            raise HTTPException(
                status_code=400,
                detail=result.get(
                    "error",
                    "Quantum simulation failed."
                )
            )

        return {
            "success": True,
            "message": "Quantum circuit simulation completed successfully.",
            "parser": parser_mode,
            "result": result
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )
routes_simulation.pyroutes_simulation.pyroutes_simulation.pyroutes_simulation.pyroutes_simulation.pyroutes_simulation.pyroutes_simulation.py
