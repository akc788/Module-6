class HashItem():
    def __init__(self, key, value):
        self.key = key
        self.value = value
    
    def __repr__(self):
        return f'{{{self.key}: {self.value}}}'

class HashTable():
    def __init__(self, size=256):
        self.size = size
        self.slots = [None] * size
        self.used_slots = 0
    
    def __repr__(self):
        text = ''
        for index, slot in enumerate(self.slots):
            if slot:
                text += f', {index}: {slot}'
        plural = '' if self.used_slots == 1 else 's'
        return f'<HashTable ({self.used_slots} element{plural}): [{text.lstrip(", ")}]'

    def _hash(self, key):
        return sum((index+1) * ord(char) * ord(char) for index, char in enumerate(key)) % self.size

    def _find_free_slot(self, start):
        current = start
        while self.slots[current]:
            current = (current + 1) % self.size
            if current == start:
                return None
        return current

    def _find_key(self, start, key):
        current = start
        while self.slots[current] and self.slots[current].key != key:
            current = (current + 1) % self.size
            if current == start:
                return None
        if self.slots[current]:
            return current
        return None

    def put(self, key, value):
        index = self._hash(key)
        existing_index = self._find_key(index, key)
        
        if existing_index is not None:
            # Key exists, update value
            self.slots[existing_index].value = value
        else:
            # Find a free slot
            free_index = self._find_free_slot(index)
            if free_index is None:
                raise MemoryError("HashTable is full")
            self.slots[free_index] = HashItem(key, value)
            self.used_slots += 1