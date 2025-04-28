import json
import os
from typing import List, Dict


def save_to_json(instruments: List, rentals: List, filename: str) -> None:
    from instruments.musical_instrument import MusicalInstrument
    from rental import Rental
    data = {
        'instruments': [inst.to_dict() for inst in instruments],
        'rentals': [rental.to_dict() for rental in rentals]
    }
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_from_json(filename: str) -> tuple[List, List]:
    from instruments.musical_instrument import MusicalInstrument
    from rental import Rental
    if not os.path.exists(filename):
        return [], []
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    instruments = [MusicalInstrument.from_dict(inst) for inst in data.get('instruments', [])]
    rentals = [Rental.from_dict(rental) for rental in data.get('rentals', [])]
    return instruments, rentals