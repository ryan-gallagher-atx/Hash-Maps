# Name: Ryan Gallagher
# OSU Email: gallagry@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: March 11
# Description: HashMap Implementation


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """Clears the hashmap."""
        temp = HashMap(self.capacity, self.hash_function)
        self.buckets = temp.buckets
        self.size = 0

    def get(self, key: str) -> object:
        """Determines if a key is in the hashmap, and if so, returns the value. If not, returns None."""
        if self.buckets.length() <= 0:
            return None
        hashed_index = self.hash_function(key) % self.capacity
        result = self.get_quadratic_probe(hashed_index, key)
        return result
        # quadratic probing required

    def get_quadratic_probe(self, initial_index, key) -> int or None:
        """Quadratically probes the hashmap for the key."""
        j = 1
        index = (initial_index + j ** 2) % self.capacity
        while self.buckets.get_at_index(index) is not None:
            if self.buckets.get_at_index(index).key == key:
                return self.buckets.get_at_index(index).value
            j += 1
            index = (initial_index + j ** 2) % self.capacity
        return None

    def put(self, key: str, value: object) -> None:   # needs to handle tombstone
        """Adds a key value pair to the hash map. If the key already exists, it overwrites the value."""
        if self.table_load() >= 0.5:   # resize check, if needed
            self.resize_table(self.capacity * 2)
        hashed_index = self.hash_function(key) % self.capacity
        hashed_index = self.put_quadratic_probe(hashed_index, key)
        item = HashEntry(key, value)
        self.buckets.set_at_index(hashed_index, item)
        self.size += 1

        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        #
        # quadratic probing required

    def put_quadratic_probe(self, initial_index, key) -> int:
        """Quadratically probes the Dynamic Array as a helper method."""
        j = 1
        index = (initial_index + j ** 2) % self.capacity
        while self.buckets.get_at_index(index) is not None:
            if self.buckets.get_at_index(index).key == key:
                self.size -= 1
                return index
            j += 1
            index = (initial_index + j ** 2) % self.capacity
        return index

    def remove(self, key: str) -> None:
        """Removes the provided key and its value, if it is in the hashmap. Otherwise, does nothing."""
        if self.buckets.length() <= 0:
            return None
        hashed_index = self.hash_function(key) % self.capacity
        self.remove_quadratic_probe(hashed_index, key)
        # quadratic probing required

    def remove_quadratic_probe(self, initial_index, key) -> None:
        """Quadratically probes the hashmap for the key."""
        j = 1
        index = (initial_index + j ** 2) % self.capacity
        while self.buckets.get_at_index(index) is not None:
            if self.buckets.get_at_index(index).key == key:
                self.buckets.get_at_index(index).key = None
                self.buckets.get_at_index(index).value = None
                self.buckets.get_at_index(index).is_tombstone = True
                self.size -= 1
                return None
            j += 1
            index = (initial_index + j ** 2) % self.capacity

    def contains_key(self, key: str) -> bool:   # retest after remove is implemented
        """Determines if the hashmap contains a key, and returns True if found or False if not."""
        if self.buckets.length() <= 0:
            return False
        hashed_index = self.hash_function(key) % self.capacity
        result = self.contains_key_quadratic_probe(hashed_index, key)
        return result
        # quadratic probing required

    def contains_key_quadratic_probe(self, initial_index, key) -> bool:
        """Quadratically probes the hashmap for the key."""
        j = 1
        index = (initial_index + j ** 2) % self.capacity
        while self.buckets.get_at_index(index) is not None:
            if self.buckets.get_at_index(index).key == key:
                return True
            j += 1
            index = (initial_index + j ** 2) % self.capacity
        return False

    def empty_buckets(self) -> int:
        """Returns the number of empty buckets in the hash table."""
        index = 0
        empty_count = 0
        while index < self.capacity:
            bucket = self.buckets.get_at_index(index)
            if bucket is None:
                empty_count += 1
            index += 1
        return empty_count

    def table_load(self) -> float:
        """Returns the current hash table load factor."""
        load_factor = self.size / self.capacity
        return load_factor

    def resize_table(self, new_capacity: int) -> None:
        """Resize the table and rehash all entries."""
        temp = HashMap(new_capacity, self.hash_function)
        if new_capacity < 1 or new_capacity < self.size:
            return   # handles impossible resizes
        index = 0
        while index < self.capacity:
            hash_entry = self.buckets.get_at_index(index)
            if hash_entry is None or hash_entry.is_tombstone is True:
                pass
            else:
                key, value = hash_entry.key, hash_entry.value
                temp.put(key, value)
            index += 1
        self.buckets = temp.buckets
        self.capacity = temp.capacity
        self.table_load()
        # remember to rehash non-deleted entries into new table

    def get_keys(self) -> DynamicArray:
        """Returns a DynamicArray containing all keys stored in the hash map."""
        target_keys = DynamicArray()
        index = 0
        while index < self.capacity:
            hash_entry = self.buckets.get_at_index(index)
            if hash_entry is None or hash_entry.is_tombstone is True:
                pass
            else:
                target_keys.append(hash_entry.key)
            index += 1
        return target_keys


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")   # works with current iteration
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")  # will work after remove is implemented
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))
    #
    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    #
    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
