class TreeNode:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        if child_node.parent is not None:
            raise Exception('Node already has a parent')
        self.children.append(child_node)
        child_node.parent = self

def build_tree():
    # Define parent node
    specification_node = TreeNode("Specification")

    # Define child nodes
    power_consumption_node = TreeNode("Power Consumption")
    dimensions_node = TreeNode("Dimensions")

    # Add child nodes to parent node
    specification_node.add_child(power_consumption_node)
    specification_node.add_child(dimensions_node)

    # Return root node
    return specification_node

def export_tree_to_file(node, filename):
    with open(filename, "w") as f:
        # Write the root node to the file
        f.write(f"{node.value}\n")

        # Traverse the tree using depth-first search and write each node to the file
        stack = [node]
        while stack:
            current_node = stack.pop()
            for child_node in current_node.children:
                f.write(f"{current_node.value} -> {child_node.value}\n")
                stack.append(child_node)

def import_tree_from_file(filename):
    # Read the file and create a dictionary mapping node values to node objects
    nodes = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if "->" not in line:
                node_value = line
                if node_value not in nodes:
                    nodes[node_value] = TreeNode(node_value)
            else:
                parent_value, child_value = line.split("->")
                if parent_value not in nodes:
                    nodes[parent_value] = TreeNode(parent_value)
                if child_value not in nodes:
                    nodes[child_value] = TreeNode(child_value)
                parent_node = nodes[parent_value]
                child_node = nodes[child_value]
                parent_node.add_child(child_node)

    # Find the root node (the node with no parent)
    root_node = None
    for node in nodes.values():
        if node.parent is None:
            root_node = node
            break

    # Return the root node
    return root_node

def display_tree(node, indent=0):
    print(" " * indent + node.value)
    for child_node in node.children:
        display_tree(child_node, indent + 2)

# Build the tree
root_node = build_tree()

# Export the tree to a file
export_tree_to_file(root_node, "mindmap.txt")

# Import the tree from a file
# root_node = import_tree_from_file("mindmap.txt")

# Display the tree
display_tree(root_node)