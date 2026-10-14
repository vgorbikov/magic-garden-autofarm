from dataclasses import dataclass
from pathlib import Path
from typing import Union

import yaml



@dataclass
class AuthConfig():
    user_name: str
    saved_auth_state_path: Path

    def __post_init__(self):
        self.saved_auth_state_path = Path(self.saved_auth_state_path)


@dataclass
class Config():
    auth: AuthConfig

    def __post_init__(self):
        if not isinstance(self.auth, AuthConfig):
            self.auth = AuthConfig(**self.auth)
    
    @classmethod
    def loads_from_yaml(cls, path: Union[Path, str]):
        if isinstance(path, Path):
            path = path.as_posix()
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return cls(**config)
