class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent is not None:
            return self.parent.get_variable(name)
        else:
            raise NameError(f"Variable '{name}' not found in scope.")
        
        
class Memory:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope

    def enter_scope(self):
        new_scope = Scope(parent=self.current_scope)
        self.current_scope = new_scope

    def exit_scope(self):
        if self.current_scope.parent is not None:
            self.current_scope = self.current_scope.parent
        else:
            raise Exception("Cannot exit global scope.")

    def set_variable(self, name, value):
        if self.current_scope is not None:
            self.current_scope.set_variable(name, value)

    def get_variable(self, name):
        return self.current_scope.get_variable(name)
    
    
ram = Memory()
ram.set_variable('x', 10)
ram.enter_scope()
ram.set_variable('y', 20)
print(ram.get_variable('x'))  # Output: 10
print(ram.get_variable('y'))  #Output: 20
ram.exit_scope()
ram.get_variable('y')  # This will raise an exception since 'y' is not in the global scope