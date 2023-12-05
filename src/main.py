import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.figure as mplfig


class NetworkVisualizer(tk.Tk):

    def __init__(self, width=800, height=600):
        super().__init__()
        self.title("Network Visualizer")
        self.set_window_size(width, height)
        self.create_widgets()
        self.G = nx.DiGraph()
        self.configure_fullscreen()
        self.initialize_blank_figure()

    def save_graph(self):
        file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("All Files", "*.*")
                ]
            )
        if file_path:
            plt.gcf().savefig(file_path)

    def create_widgets(self):
        # Configure grid expansion
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Widgets
        self.label = ttk.Label(self, text="Enter edges (EX: \"A -> B, B -> C\"):")
        self.label.grid(row=0, column=0, columnspan=2, sticky='n')

        self.entry = ttk.Entry(self)
        self.entry.grid(row=1, column=0, columnspan=2, sticky='new')

        self.add_edges_button = ttk.Button(self, text="Add Edges", command=self.add_edges)
        self.add_edges_button.grid(row=2, column=0, sticky='e')

        self.remove_edges_button = ttk.Button(self, text="Remove Edges", command=self.remove_edges)
        self.remove_edges_button.grid(row=2, column=1, sticky='w')

        self.help_button = ttk.Button(self, text="Help", command=self.show_help)
        self.help_button.grid(row=3, column=0, sticky='e')

        self.save_button = ttk.Button(self, text="Save Graph", command=self.save_graph)
        self.save_button.grid(row=3, column=1, sticky='w')

    def initialize_blank_figure(self):
        self.figure = mplfig.Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=4, column=0, columnspan=2, sticky='nsew')

    def add_edges(self):
        input_str = self.entry.get()
        edges = input_str.split(",")
        for edge in edges:
            parts = edge.split("->")
            if len(parts) == 2:
                a, b = parts
                label = None
                if '-(' in a and ')' in a:
                    a, label = a.split('-(')
                    label = label.rstrip(')')
                self.G.add_edge(a.strip(), b.strip(), label=label if label else '')
        self.visualize()

    def remove_edges(self):
        input_str = self.entry.get()
        edges = input_str.split(",")
        for edge in edges:
            a, b = edge.split("->")
            self.G.remove_edge(a.strip(), b.strip())
            # If the edege of a leaf node is being removed,
            # it is safe to remove that node
            if self.G.out_degree(b.strip()) == 0:
                self.G.remove_node(b.strip())
        self.visualize()

    def plot_graph(self):
        plt.gcf().clf()
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, node_color='skyblue', edge_color='gray')
        edge_labels = nx.get_edge_attributes(self.G, 'label')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        return plt

    def visualize(self):
        plt = self.plot_graph()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=3, column=0, columnspan=2)
        self.canvas.draw()
        self.canvas_widget.grid(row=4, column=0, columnspan=2, sticky='nsew')

    def show_help(self):
        help_text = (
            "RCA Visualizer Help\n\n"
            "Add Edges: Enter edges in the format 'A -> B' or 'A -(label)-> B' and click 'Add Edges'.\n"
            "Remove Edges: Enter edges in the same format and click 'Remove Edges'.\n"
            "Save Graph: Click 'Save Graph' to save the current graph as a PNG image.\n"
            "Exit Fullscreen: Press the Escape key.\n\n"
            "Example Inputs:\n"
            "  A -> B (adds an edge from A to B)\n"
            "  C -(label)-> D (adds an edge from C to D with label)\n\n"
        )
        messagebox.showinfo("Help", help_text)

    def set_window_size(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{x}+{y}")

    def configure_fullscreen(self):
        self.bind("<Escape>", self.exit_fullscreen)

    def exit_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)


if __name__ == "__main__":
    app = NetworkVisualizer()
    app.mainloop()
