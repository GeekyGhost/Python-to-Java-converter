import ast
import tkinter as tk
from tkinter import filedialog

class PythonToJavaConverter(ast.NodeVisitor):
    def __init__(self):
        self.converted_code = []
        self.indent_level = 0

    def indent(self):
        return '    ' * self.indent_level

    def visit_Module(self, node):
        for stmt in node.body:
            self.visit(stmt)

    def visit_FunctionDef(self, node):
        self.converted_code.append(f"{self.indent()}public static void {node.name}() {{")
        self.indent_level += 1
        self.generic_visit(node)
        self.indent_level -= 1
        self.converted_code.append(f"{self.indent()}}}")

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'print':
            self.converted_code.append(f"{self.indent()}System.out.println({self.visit(node.value.args[0])});")
        else:
            self.generic_visit(node)

    def visit_Assign(self, node):
        target = self.visit(node.targets[0])
        value = self.visit(node.value)
        self.converted_code.append(f"{self.indent()}{target} = {value};")

    def visit_Name(self, node):
        return node.id

    def visit_Num(self, node):
        return str(node.n)

    def visit_Str(self, node):
        return f'"{node.s}"'

    def visit_For(self, node):
        target = self.visit(node.target)
        iterable = self.visit(node.iter)
        self.converted_code.append(f"{self.indent()}for ({target} : {iterable}) {{")
        self.indent_level += 1
        self.generic_visit(node)
        self.indent_level -= 1
        self.converted_code.append(f"{self.indent()}}}")

    def visit_While(self, node):
        test = self.visit(node.test)
        self.converted_code.append(f"{self.indent()}while ({test}) {{")
        self.indent_level += 1
        self.generic_visit(node)
        self.indent_level -= 1
        self.converted_code.append(f"{self.indent()}}}")

    def visit_If(self, node):
        test = self.visit(node.test)
        self.converted_code.append(f"{self.indent()}if ({test}) {{")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.converted_code.append(f"{self.indent()}}}")

        for elif_clause in node.orelse:
            if isinstance(elif_clause, ast.If):
                self.visit(elif_clause)
            else:
                self.converted_code.append(f"{self.indent()}else {{")
                self.indent_level += 1
                self.visit(elif_clause)
                self.indent_level -= 1
                self.converted_code.append(f"{self.indent()}}}")

    # Add other node conversion methods here

    def convert(self, code):
        tree = ast.parse(code)
        self.visit(tree)
        return '\n'.join(self.converted_code)

def python_to_java(code):
    converter = PythonToJavaConverter()
    return converter.convert(code)

def browse_file():
    file_path.set(filedialog.askopenfilename())

def convert_file():
    input_file = file_path.get()
    if input_file:
        with open(input_file, 'r') as f:
            code = f.read()
            converted_code = python_to_java(code)
            output.delete(1.0, tk.END)
            output.insert(tk.END, converted_code)

root = tk.Tk()
root.title("Python to Java Converter")

file_path = tk.StringVar()

file_frame = tk.LabelFrame(root, text="Select a File", padx=5, pady=5)
file_frame.grid(row=0, column=0, padx=10, pady=10)

tk.Label(file_frame, text="File Path:").grid(row=0, column=0)
tk.Entry(file_frame, textvariable=file_path).grid(row=0, column=1)
tk.Button(file_frame, text="Browse", command=browse_file).grid(row=0, column=2)

output = tk.Text(root, wrap=tk.WORD, width=80, height=20)
output.grid(row=1, column=0, padx=10, pady=10)

button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, padx=10, pady=10)

tk.Button(button_frame, text="Convert", command=convert_file).grid(row=0, column=0)

root.mainloop()
