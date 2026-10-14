import json
from typing import Dict
import inspect



def dict_to_pretty_json_string(d: Dict) -> str:
    return json.dumps(
        d,
        indent=4
    )


class ReprMixin:
    def __repr__(self):
        cls = type(self)
        props = dict(inspect.getmembers(cls, lambda x: isinstance(x, property)))
        
        parts = []
        
        # 1. Обычные атрибуты экземпляра (кроме приватных)
        for key, value in vars(self).items():
            if key.startswith("_"):
                continue
            parts.append(f"{key}={value!r}")
        
        # 2. Property (кроме тех, что дублируют атрибуты)
        for name in props:
            if name in vars(self):
                continue
            try:
                value = getattr(self, name)
            except Exception as e:
                value = f"<error: {e!r}>"
            parts.append(f"{name}={value!r}")
        
        return f"{cls.__name__}({', '.join(parts)})"
