import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NetworkVisualizer(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Network Visualizer")
        self.set_window_size(800, 600)
        self.create_widgets()
        self.graph = {}
        self.configure_fullscreen()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Enter edges (EX: \"A -> B, B -> C\"):")
        self.label.grid(row=0, column=0)

        self.entry = ttk.Entry(self)
        self.entry.grid(row=0, column=1)

        self.visualize_button = ttk.Button(self, text="Visualize", command=self.visualize)
        self.visualize_button.grid(row=1, column=0, columnspan=2)

    def create_graph(self, edges):
        G = nx.DiGraph()
        for edge in edges:
            a, b = edge.split('->')
            if a in list(self.graph.keys()):
                if b not in self.graph[a]:
                    if type(self.graph) == list:
                        self.graph[a].append(b)
                    else:
                        self.graph[a] = [b]
                else:
                    continue

            G.add_edge(a.strip(), b.strip())
        return G

    def plot_graph(self, G):
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray')
        return plt

    def visualize(self):
        input_str = self.entry.get()
        edges = input_str.split(',')
        G = self.create_graph(edges)
        plt = self.plot_graph(G)

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=2, column=0, columnspan=2)
        self.canvas.draw()

    def set_window_size(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.geometry(f'{width}x{height}+{x}+{y}')

    def configure_fullscreen(self):
        self.bind("<Escape>", self.exit_fullscreen)

    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)


if __name__ == "__main__":
    app = NetworkVisualizer()
    app.mainloop()

