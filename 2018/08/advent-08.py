class SleighNode:
    def __init__(self, input):
        self.no_of_children = input[0]
        self.no_of_meta = input[1]
        self.children = list()
        self.metadata = list()
        length_of_children = 0
        if self.no_of_children > 0:
            for i in range(0, self.no_of_children):
                starting_index = length_of_children + 2
                child = SleighNode(input[starting_index:])
                self.children.append((child, starting_index))
                length_of_children += child.length
        metadata_start = length_of_children + 2
        for i in range(0, self.no_of_meta):
            self.metadata.append(input[metadata_start + i])
        self.length = 2 + length_of_children + self.no_of_meta
        self.whole = input[: self.length]
        self.meta_sum = sum(self.metadata)
        if self.no_of_children > 0:
            for (child, _) in self.children:
                self.meta_sum += child.meta_sum
            value_list = []
            for entry in self.metadata:
                if entry != 0 and len(self.children) >= entry:
                    entry_ref = self.children[entry - 1][0]
                    value_list.append(entry_ref.value)
                else:
                    value_list.append(0)
            self.value = sum(value_list)
        else:
            self.value = sum(self.metadata)


# with open("test-input.txt") as file:
with open("input.txt") as file:
    content = file.read()

items = [int(x) for x in content.split()]
test = SleighNode(items)
print(f"Sum of all Metadata: {test.meta_sum}")
print(f"Value of Root Node: {test.value}")
