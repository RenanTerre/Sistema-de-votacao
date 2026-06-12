from pydantic import BaseModel, field_validator

# As opções válidas no sistema
OPCOES_VALIDAS = ["python", "javascript"]

class VotoDTO(BaseModel):
    opcao: str

    @field_validator('opcao')
    @classmethod
    def validar_opcao(cls, v: str) -> str:
        v_lower = v.lower()
        if v_lower not in OPCOES_VALIDAS:
            raise ValueError(f"Opção inválida. Escolha entre: {', '.join(OPCOES_VALIDAS)}")
        return v_lower