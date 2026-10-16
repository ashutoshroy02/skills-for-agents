# Networks

**The film's code**

```python
import manimgx as m

class NetworksHero(m.Scene):
    def construct(self) -> None:
        vertices = [1, 2, 3, 4, 5, 6]
        edges = [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (6, 4)]
        graph = m.Graph(vertices, edges, layout="spring", labels=True, layout_scale=3)
        self.play(m.Create(graph))
        self.play(graph.animate.change_layout("circular", layout_scale=3))
        self.wait()
```

A network is vertices, joined by edges: a graph, as graph theory says it. (For the graph of a function, see [Plotting](<https://manimgx.academa.ai/reference/mobjects/graphs/plotting/index.md>).) Graph joins its vertices with lines, DiGraph with arrows, from each edge's first vertex to its second. Each lays its vertices out for you (`layout="spring"`, `"circular"`, `"tree"`, …), or where you place them; a vertex is a dot unless you give another mobject.

Both can do what follows: add and remove vertices and edges, change their layout, and read a network from NetworkX.

## Graph

**Code**

```python
import manimgx as m

class GraphExample(m.Scene):
    def construct(self) -> None:
        vertices = [1, 2, 3, 4, 5, 6]
        edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (1, 4), (2, 5)]
        graph = m.Graph(
            vertices,
            edges,
            layout="circular",
            layout_scale=3,
            labels=True,
            vertex_config={1: {"fill_color": m.RED}},
            edge_config={(1, 4): {"stroke_color": m.YELLOW}},
        )
        self.play(m.Create(graph))
        self.play(graph[3].animate.move_to([0, 0, 0]))
```

An undirected graph: vertices joined by edges, laid out automatically or by hand; white dots and lines unless styled.

Each edge runs from the center of one vertex to the center of the other, behind them, and follows them as they move. It takes the arguments of a GenericGraph, which lists what a graph can do.

```python
m.Graph(vertices, edges, labels=False, label_fill_color=BLACK, layout='spring', layout_scale=2, layout_config=None, vertex_type=Dot, vertex_config=None, vertex_mobjects=None, edge_type=Line, partitions=None, root_vertex=None, edge_config=None)
```

## DiGraph

**Code**

```python
import manimgx as m

class DiGraphExample(m.Scene):
    def construct(self) -> None:
        edge_config = {
            "stroke_width": 3,
            "tip_config": {"tip_length": 0.2, "tip_width": 0.2},
            (3, 4): {
                "color": m.RED,
                "tip_config": {"tip_shape": m.ArrowSquareTip},
            },
        }
        graph = m.DiGraph(
            [0, 1, 2, 3, 4],
            [(0, 1), (1, 2), (3, 2), (3, 4), (4, 0)],
            labels=True,
            layout="circular",
            layout_scale=3,
            edge_config=edge_config,
        )
        self.play(m.Create(graph))
```

A directed graph: vertices joined by arrows, from the first vertex of each edge to the second; white dots and arrows unless styled.

Each edge runs from the outline of one vertex to the outline of the other and ends in a tip, which the `"tip_config"` of `edge_config` shapes (see TipConfig), for every edge or an edge's own; it follows its vertices as they move. It takes the arguments of a GenericGraph, which lists what a graph can do.

```python
m.DiGraph(vertices, edges, labels=False, label_fill_color=BLACK, layout='spring', layout_scale=2, layout_config=None, vertex_type=Dot, vertex_config=None, vertex_mobjects=None, edge_type=Line, partitions=None, root_vertex=None, edge_config=None)
```

### TipConfig

The tip of a DiGraph's edge, given as `"tip_config"` in its `edge_config`: for every edge, or an edge's own (see add\_tip).

**`tip_shape`**

The class of the tip (default None: ArrowTriangleFilledTip).

**`tip_length`**

The tip's length, in scene units (default None: the edge's default).

**`tip_width`**

The tip's width, in scene units, for the default filled triangle (default None: its length).

#### tip\_shape

The class of the tip (default None: ArrowTriangleFilledTip).

#### tip\_length

The tip's length, in scene units (default None: the edge's default).

#### tip\_width

The tip's width, in scene units, for the default filled triangle (default None: its length).

## What a network can do

Graph and DiGraph are both made from GenericGraph, which holds what they can do.

### GenericGraph

#### vertices

The vertices' mobjects, by vertex.

#### edges

The edges' mobjects, by pair of vertices.

#### add\_vertices

**Code**

```python
import manimgx as m

class GraphAddVerticesExample(m.Scene):
    def construct(self) -> None:
        graph = m.Graph(
            [1, 2, 3],
            [(1, 2), (2, 3)],
            layout={1: [-4, -1, 0], 2: [0, -2, 0], 3: [4, -1, 0]},
            vertex_config={"radius": 0.15},
        )
        self.add(graph)
        top = graph.add_vertices(
            4, positions={4: [0, 2.5, 0]}, vertex_config={"color": m.YELLOW}
        )
        self.play(m.FadeIn(top, scale=3))
        self.play(m.Create(graph.add_edges((1, 4), (3, 4))))
```

Add vertices to the graph, without edges.

Each is made as the graph makes its vertices, with the keywords given over the graph's own, and placed at its position, or at the graph's center. A vertex already in the graph raises a ValueError.

```python
generic_graph.add_vertices(*vertices, **kwargs)
```

**`*vertices`**

The new vertices: hashable values, each a vertex's name.

**`positions`**

Where new vertices go, by vertex (default None: at the graph's center).

**`labels`**

Whether each new vertex is labeled with its name, typeset as math: True for all, or by vertex, True or a label of one's own (default False).

**`label_fill_color`**

The color of the labels made from names (default black).

**`vertex_type`**

The class of the new vertices (default Dot; a labeled one is a LabeledDot).

**`vertex_config`**

Keywords for the new vertices, over the graph's: for all of them, and a vertex's own under its name, in place of those for all (default None: none).

**`vertex_mobjects`**

Mobjects to be vertices themselves, by vertex (default None: none).

Returns A new group of the new vertices' mobjects.

        import manimgx as m

        class GraphAddVerticesExample(m.Scene):
            def construct(self) -> None:
                graph = m.Graph(
                    [1, 2, 3],
                    [(1, 2), (2, 3)],
                    layout={1: [-4, -1, 0], 2: [0, -2, 0], 3: [4, -1, 0]},
                    vertex_config={"radius": 0.15},
                )
                self.add(graph)
                top = graph.add_vertices(
                    4, positions={4: [0, 2.5, 0]}, vertex_config={"color": m.YELLOW}
                )
                self.play(m.FadeIn(top, scale=3))
                self.play(m.Create(graph.add_edges((1, 4), (3, 4))))
        ```
    """
    return Group(
        *(
            self._add_created_vertex(*v)
            for v in self._create_vertices(*vertices, **kwargs)
        )
    )
````

#### remove\_vertices

**Code**

```python
import manimgx as m

class GraphRemoveVerticesExample(m.Scene):
    def construct(self) -> None:
        graph = m.Graph(
            [1, 2, 3, 4, 5],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3)],
            layout="circular",
            layout_scale=3,
        )
        self.add(graph)
        self.play(m.FadeOut(graph.remove_vertices(3)))
```

Remove vertices from the graph, and the edges that touch them.

A vertex not in the graph raises a ValueError.

```python
generic_graph.remove_vertices(*vertices)
```

**`*vertices`**

The vertices to remove.

Returns A new group of the removed mobjects (for each vertex, its edges, then the vertex), to fade out, for instance.

        import manimgx as m

        class GraphRemoveVerticesExample(m.Scene):
            def construct(self) -> None:
                graph = m.Graph(
                    [1, 2, 3, 4, 5],
                    [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3)],
                    layout="circular",
                    layout_scale=3,
                )
                self.add(graph)
                self.play(m.FadeOut(graph.remove_vertices(3)))
        ```
    """
    return Group(*(m for v in vertices for m in self._remove_vertex(v).submobjects))
````

#### add\_edges

Add edges to the graph, and the vertices they name that it lacks.

The missing vertices are added first, as add\_vertices adds them, with the vertex keywords given; each edge is then made as the graph makes its edges, with the edge keywords given over the graph's own.

```python
generic_graph.add_edges(*edges, edge_type=Line, edge_config=None, **kwargs)
```

**`*edges`**

The new edges, each a pair of vertices.

**`edge_type`**

The class of the new edges.

**`edge_config`**

Keywords for the new edges, over the graph's: for all of them, and an edge's own under its pair of vertices, in place of those for all; None for none.

It also takes the `add_vertices` keywords.

Returns A new group of the new mobjects, the vertices added and then the edges.

#### remove\_edges

Remove edges from the graph, keeping their vertices.

An edge not in the graph raises a ValueError.

```python
generic_graph.remove_edges(*edges)
```

**`*edges`**

The edges to remove, each a pair of vertices.

Returns A new group of the removed edges' mobjects.

#### change\_layout

**Code**

```python
import manimgx as m

class GraphChangeLayoutExample(m.Scene):
    def construct(self) -> None:
        graph = m.Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (1, 4)],
            layout={v: [2 * v - 7, 0, 0] for v in range(1, 7)},
        )
        circle = graph.copy().change_layout("circular", layout_scale=3)
        self.add(graph)
        self.play(
            *(graph[v].animate.move_to(circle[v]) for v in graph.vertices)
        )
```

Lay the graph out anew: move each vertex to its place in a layout.

The vertices move at once, and the edges follow them at the next frame, as the graph's updater moves them. To animate the change, animate each vertex to its place in a changed copy (as below): the edges follow all the way.

A layout function gets a fresh NetworkX graph of the current vertices and edges. Its node, edge and graph attributes belong to that call, not to later layouts.

```python
generic_graph.change_layout(layout='spring', layout_scale=2, layout_config=None, partitions=None, root_vertex=None)
```

**`layout`**

Where the vertices go: a layout's name, their positions, or a layout function (see GenericGraph).

**`layout_scale`**

How far the layout reaches from the center, in scene units.

**`layout_config`**

Keywords for the layout function; None for none.

**`partitions`**

For the `"partite"` layout: the vertices of each column; None for none.

**`root_vertex`**

For the `"tree"` layout: the vertex at its top; None for none.

        import manimgx as m

        class GraphChangeLayoutExample(m.Scene):
            def construct(self) -> None:
                graph = m.Graph(
                    [1, 2, 3, 4, 5, 6],
                    [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (1, 4)],
                    layout={v: [2 * v - 7, 0, 0] for v in range(1, 7)},
                )
                circle = graph.copy().change_layout("circular", layout_scale=3)
                self.add(graph)
                self.play(
                    *(graph[v].animate.move_to(circle[v]) for v in graph.vertices)
                )
        ```
    """
    return self._place_vertices(
        self.edges,
        layout=layout,
        layout_scale=layout_scale,
        layout_config=layout_config,
        partitions=partitions,
        root_vertex=root_vertex,
    )
````

#### from\_networkx

**Code**

```python
import networkx as nx

import manimgx as m

class GraphFromNetworkxExample(m.Scene):
    def construct(self) -> None:
        petersen = nx.petersen_graph()
        graph = m.Graph.from_networkx(
            petersen,
            layout="shell",
            layout_scale=3,
            layout_config={"nlist": [range(5, 10), range(5)]},
        )
        self.play(m.Create(graph), run_time=2)
```

Make a graph of a [NetworkX](<https://networkx.org>) graph's nodes and edges.

```python
GenericGraph.from_networkx(nxgraph, **kwargs)
```

**`nxgraph`**

The NetworkX graph (a `Graph`, or a `DiGraph`).

**`labels`**

Whether each vertex is labeled with its name, typeset as math, or a label for each (default False).

**`label_fill_color`**

The color of the labels made from names (default black).

**`layout`**

Where the vertices go: a layout's name, their positions, or a layout function (default `"spring"`).

**`layout_scale`**

How far the layout reaches from the center, in scene units (default 2).

**`layout_config`**

Keywords for the layout function: a `"spring"` layout's `seed`, … (default None: none).

**`vertex_type`**

The class of the vertices (default Dot; a labeled one is a LabeledDot).

**`vertex_config`**

Keywords for the vertices: for all of them, and a vertex's own under its name, in place of those for all (default None: none).

**`vertex_mobjects`**

Mobjects to be vertices themselves, by vertex (default None: none).

**`edge_type`**

The class of the edges (default Line).

**`partitions`**

For the `"partite"` layout: the vertices of each column, in order (default None: none).

**`root_vertex`**

For the `"tree"` layout: the vertex at its top (default None: none).

**`edge_config`**

Keywords for the edges: for all of them, and an edge's own under its pair of vertices, in place of those for all (default None: none).

Returns A new graph.

        import networkx as nx

        import manimgx as m

        class GraphFromNetworkxExample(m.Scene):
            def construct(self) -> None:
                petersen = nx.petersen_graph()
                graph = m.Graph.from_networkx(
                    petersen,
                    layout="shell",
                    layout_scale=3,
                    layout_config={"nlist": [range(5, 10), range(5)]},
                )
                self.play(m.Create(graph), run_time=2)
        ```
    """
    return cls(list(nxgraph.nodes), list(nxgraph.edges), **kwargs)
````

#### update\_edges

Put each edge back on its vertices, where they are now: the updater a graph runs every frame, so that its edges follow its vertices.

Each kind of graph sets its edges' ends its own way: an undirected graph's from center to center, a directed graph's from outline to outline, with its tip. Only edges that are lines (Line and its kinds) follow.

```python
generic_graph.update_edges(graph)
```

**`graph`**

The mobject the updater runs for (the graph); unused.
