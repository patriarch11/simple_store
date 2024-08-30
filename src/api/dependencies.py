from fastapi            import Depends

from src.api.validators import CategoryValidator

validate_category = Depends(CategoryValidator())
