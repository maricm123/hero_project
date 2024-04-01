from django.core.exceptions import ValidationError

def count_pills_from_request(data):
    if data.get('pills'):
        pills_count = len(data.get('pills', []))
        return pills_count
    else:
        pills_count = len(data.get('consumables', []))
        return pills_count

# Check if there is same number of consumables and slots objects in request
def check_same_pill_and_slot(data):
    consumables = data.get('consumables', [])
    slots = data.get('slots', [])

    if len(consumables) != len(slots):
        raise ValidationError("Invalid data, not same consumables and slots")

    consumables_slots_pairs = []
    for consumable in consumables:
        consumable_id = consumable.get('id')
        slot = next((s for s in slots if s.get('id') == consumable_id), None)

        if slot is None:
            raise ValidationError(f"No slot found for consumable with ID {consumable_id}")

        # Remove id from consumables because when creating Pill we dont need ID
        consumable.pop("id")
        slot.pop("id")
        combined_object = {**consumable, **slot}
        consumables_slots_pairs.append(combined_object)

    return consumables_slots_pairs
