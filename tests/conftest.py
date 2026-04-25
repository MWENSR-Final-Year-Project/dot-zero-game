import sys
from unittest.mock import MagicMock

sys.modules.setdefault("torch", MagicMock())
