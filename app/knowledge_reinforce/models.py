# Import all models from the models package
from .models import Base, class_term_association, Term, Class

# Re-export for backward compatibility
__all__ = ["Base", "class_term_association", "Term", "Class"]
