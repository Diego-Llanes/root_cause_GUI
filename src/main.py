import tkinter as tk
from tkinter import ttk
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

    def create_widgets(self):
        # Configure grid expansion
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Widgets
        self.label = ttk.Label(self, text="Enter edges (EX: \"A -> B, B -> C\"):")
        self.label.grid(row=0, column=0, columnspan=2, sticky='n')

        self.entry = ttk.Entry(self)
        self.entry.grid(row=1, column=0, columnspan=2, sticky='new')

        self.add_edges_button = ttk.Button(self, text="Add Edges", command=self.add_edges)
        self.add_edges_button.grid(row=2, column=0, sticky='e')

        self.remove_edges_button = ttk.Button(self, text="Remove Edges", command=self.remove_edges)
        self.remove_edges_button.grid(row=2, column=1, sticky='w')

    def initialize_blank_figure(self):
        self.figure = mplfig.Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=3, column=0, columnspan=2, sticky='nsew')

    def add_edges(self):
        input_str = self.entry.get()
        edges = input_str.split(",")
        for edge in edges:
            a, b = edge.split("->")
            self.G.add_edge(a.strip(), b.strip())
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
        nx.draw(self.G, pos, with_labels=True, node_color="skyblue", edge_color="gray")
        return plt

    def visualize(self):
        plt = self.plot_graph()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=2, column=0, columnspan=2)
        self.canvas.draw()
        self.canvas_widget.grid(row=3, column=0, columnspan=2, sticky='nsew')

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
