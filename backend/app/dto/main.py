from pydantic import BaseModel

class SearchRequestDTO(BaseModel):
    term: str

class CompanyBasicDetails(BaseModel):
    corporateName: str
    documentNumber: str
    status: str
