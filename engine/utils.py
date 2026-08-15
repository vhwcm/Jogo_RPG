import random
from typing import List

def generate_fallback_embedding(text: str, dimensions: int = 128) -> List[float]:
    """Generates a deterministic float vector based on string hash without external dependencies."""
    seed = abs(hash(text)) % (2**32)
    rng = random.Random(seed)
    return [round(rng.uniform(-1.0, 1.0), 4) for _ in range(dimensions)]
