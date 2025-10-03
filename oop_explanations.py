# oop_explanations.py

explanations = """
OOP Concepts Explanation:

• Multiple Inheritance:
  The App class in gui.py inherits from Tk (tk.Tk) and can also mix in 
  other classes (e.g., utility classes). This demonstrates multiple inheritance.

• Encapsulation:
  Each model (TextModel, ImageModel) is wrapped inside a class, hiding 
  the internal pipeline setup. Users of these classes only call the run() 
  method without worrying about the implementation.

• Polymorphism:
  Both TextModel and ImageModel define a run() method. 
  Even though the underlying logic is different, they can be used 
  interchangeably in the GUI (same method name, different behavior).

• Method Overriding:
  The App class overrides methods like __init__() (inherited from tk.Tk) 
  and defines custom implementations (run_model1, run_model2, clear_output).

• Multiple Decorators:
  In utils.py you can add decorators (e.g., @log_execution, @handle_errors) 
  to wrap around model calls. This allows functionality like logging 
  and error handling without changing the original methods.
"""
