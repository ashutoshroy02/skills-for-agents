# Plotting

**The film's code**

```python
import manimgx as m

def curve(x: float) -> float:
    return 0.25 * x**2 + 0.5

class PlottingHero(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[0, 4, 1], y_range=[0, 5, 1], x_length=8, y_length=5.5)
        axes.add_coordinates()
        graph = axes.plot(curve, color=m.BLUE)
        label = axes.get_graph_label(graph, r"\frac{x^2}{4} + \frac{1}{2}", x_val=3.6)
        rectangles = axes.get_riemann_rectangles(
            graph, x_range=[1, 3], dx=0.25, fill_opacity=0.6
        )
        slope = axes.get_secant_slope_group(
            1.5, graph, dx=1, secant_line_color=m.YELLOW
        )
        self.play(m.Create(axes))
        self.play(m.Create(graph), m.Write(label))
        self.play(
            m.LaggedStart(
                *[m.GrowFromEdge(r, m.DOWN) for r in rectangles], lag_ratio=0.1
            )
        )
        self.play(m.FadeOut(rectangles), m.Create(slope))
        self.wait()
```

plot draws the graph of a Python function of x on axes, in their coordinates: it is a curve, a mobject as any other, to style and animate. The axes then make what explains it: a label at its end, the area under it, rectangles for its integral, its slope at a point, the graph of its derivative.

These methods make new mobjects, and add nothing: add them to the scene, or animate them.

## Graphs

### plot

**Code**

```python
import numpy as np

import manimgx as m

class AxesPlotExample(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[-4, 4], y_range=[-2, 2], y_length=6)
        sine = axes.plot(np.sin, color=m.BLUE)
        parabola = axes.plot(
            lambda x: x**2 - 1.5,
            x_range=[-1.8, 1.8],
            colorscale=[m.GREEN, m.YELLOW, m.RED],
        )
        self.add(axes)
        self.play(m.Create(sine), m.Create(parabola))
```

Plot the graph of a function y = f(x) on the axes, in their coordinates.

The function is sampled over `x_range` and the samples are joined smoothly (see ParametricFunction); on a logarithmic x-axis, x runs over powers. The graph keeps the function as its `underlying_function`, for the methods that work on graphs. With a `colorscale`, the graph's stroke is a gradient, from left to right, of the colors of its values (y, or x), taken at every step of `x_range` (every 0.01 without one).

```python
axes.plot(function, x_range=None, use_vectorized=False, colorscale=None, colorscale_axis=1, **kwargs)
```

**`function`**

The function, from x to y, in the axes' coordinates.

**`x_range`**

The range of x the graph spans, `[x_min, x_max]` or `[x_min, x_max, x_step]`, the function sampled every `x_step`; None for the x-axis's range. Without a step, it is a tenth of the x-axis's.

**`use_vectorized`**

Whether `function` takes all the values of x at once, as an array; it is tried on an array anyway, and called once per value if it does not take one.

**`colorscale`**

Colors to paint the graph with by its value: colors spread evenly over the axis's range, or `(color, value)` pairs, blended between; None for the graph's own color.

**`colorscale_axis`**

The value the colorscale goes by: 1 for y, 0 for x.

**`dt`**

How far short of each discontinuity the curve's pieces stop, in units of its parameter (default 1e-8).

**`discontinuities`**

The values of the parameter where the curve breaks: it is drawn in pieces between them (default None: none).

**`use_smoothing`**

Whether the samples are joined by a smooth curve through them, rather than by straight segments (default True).

**`color`**

The color of both fill and stroke (default white); None for the class's default.

**`fill_color`**

The fill's color; `color` if not given. Several colors make a gradient along `sheen_direction`.

**`fill_opacity`**

The fill's opacity, from 0 to 1 (default 0: no fill).

**`stroke_color`**

The stroke's color; `color` if not given. Several colors make a gradient.

**`stroke_opacity`**

The stroke's opacity, from 0 to 1 (default 1).

**`stroke_width`**

The stroke's width, in hundredths of a scene unit (default 4; 0: no stroke).

**`background_stroke_color`**

The color of an outline drawn behind the fill (default black).

**`background_stroke_opacity`**

The outline's opacity, from 0 to 1 (default 1).

**`background_stroke_width`**

The outline's width, in hundredths of a scene unit (default 0: none).

**`sheen_factor`**

How much the colors lighten toward `sheen_direction`, from -1 to 1 (default 0); a negative factor darkens.

**`sheen_direction`**

The direction the colors lighten toward (default `UL`).

**`joint_type`**

How the stroke is joined where its path turns: round, beveled or mitered, as a two-dimensional scene draws it (see LineJointType; default AUTO: mitered).

**`cap_style`**

How the stroke ends, at each end it shows (an open path's, a dash's): round, butt or square, as a two-dimensional scene draws it (see CapStyleType; default AUTO: butt).

**`shade_in_3d`**

Whether a three-dimensional scene's light shades the mobject.

**`material`**

How its surface reflects the scene's lights in a three-dimensional scene (see Material); None: Manim's shading (default).

**`name`**

A name for the mobject; its class's name if not given.

**`z_index`**

Its place in the drawing order: a higher index is drawn over a lower one (default 0).

**`target`**

The state `MoveToTarget` moves the mobject to.

Returns A new ParametricFunction, not added to the axes.

        import numpy as np

        import manimgx as m

        class AxesPlotExample(m.Scene):
            def construct(self) -> None:
                axes = m.Axes(x_range=[-4, 4], y_range=[-2, 2], y_length=6)
                sine = axes.plot(np.sin, color=m.BLUE)
                parabola = axes.plot(
                    lambda x: x**2 - 1.5,
                    x_range=[-1.8, 1.8],
                    colorscale=[m.GREEN, m.YELLOW, m.RED],
                )
                self.add(axes)
                self.play(m.Create(sine), m.Create(parabola))
        ```
    """
    t_range = np.array(self.x_range, dtype=float)
    if x_range is not None:
        t_range[: len(x_range)] = x_range
    if x_range is None or len(x_range) < 3:
        t_range[2] /= self.num_sampled_graph_points_per_tick

    def point(t: float | np.ndarray) -> np.ndarray:
        """The graph's point at t — or at every t of an array, mapped in one call."""
        if isinstance(t, np.ndarray):
            return self.coords_to_point(t, sample(function, t))
        return self.coords_to_point(t, function(t))

    graph = ParametricFunction(
        point,
        t_range=t_range,
        scaling=self.x_axis.scaling,
        use_vectorized=use_vectorized,
        **kwargs,
    )
    graph.underlying_function = function
    if colorscale:
        resolution = (
            x_range[2] if x_range is not None and len(x_range) == 3 else 0.01
        )
        graph.set_stroke(
            self._colorscale(
                function, colorscale, colorscale_axis, t_range, resolution
            )
        )
        graph.set_sheen_direction(RIGHT)
    return graph
````

### plot\_line\_graph

**Code**

```python
import manimgx as m

class AxesPlotLineGraphExample(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[0, 7], y_range=[0, 5], y_length=6)
        graph = axes.plot_line_graph(
            x_values=[0, 1.5, 2, 2.8, 4, 6.25],
            y_values=[1, 3, 2.25, 4, 2.5, 1.75],
            line_color=m.ORANGE,
            vertex_dot_radius=0.12,
            vertex_dot_style={"color": m.PURPLE},
            stroke_width=6,
        )
        self.add(axes.add_coordinates())
        self.play(m.Create(graph))
```

Plot a line graph: straight segments through points given by their coordinates, with a dot at each point; bright yellow (`PURE_YELLOW`), with white dots, unless styled. Empty inputs produce an empty graph.

```python
axes.plot_line_graph(x_values, y_values, z_values=None, line_color=PURE_YELLOW, add_vertex_dots=True, vertex_dot_radius=DEFAULT_DOT_RADIUS, vertex_dot_style=None, **kwargs)
```

**`x_values`**

The points' x coordinates.

**`y_values`**

Their y coordinates, as many.

**`z_values`**

Their z coordinates, on three-dimensional axes; None for 0.

**`line_color`**

The line's color, unless the keywords give a `color`.

**`add_vertex_dots`**

Whether a dot marks each point.

**`vertex_dot_radius`**

The dots' radius, in scene units.

**`vertex_dot_style`**

Style keywords for the dots; None for none.

**`color`**

The color of both fill and stroke (default white); None for the class's default.

**`fill_color`**

The fill's color; `color` if not given. Several colors make a gradient along `sheen_direction`.

**`fill_opacity`**

The fill's opacity, from 0 to 1 (default 0: no fill).

**`stroke_color`**

The stroke's color; `color` if not given. Several colors make a gradient.

**`stroke_opacity`**

The stroke's opacity, from 0 to 1 (default 1).

**`stroke_width`**

The stroke's width, in hundredths of a scene unit (default 4; 0: no stroke).

**`background_stroke_color`**

The color of an outline drawn behind the fill (default black).

**`background_stroke_opacity`**

The outline's opacity, from 0 to 1 (default 1).

**`background_stroke_width`**

The outline's width, in hundredths of a scene unit (default 0: none).

**`sheen_factor`**

How much the colors lighten toward `sheen_direction`, from -1 to 1 (default 0); a negative factor darkens.

**`sheen_direction`**

The direction the colors lighten toward (default `UL`).

**`joint_type`**

How the stroke is joined where its path turns: round, beveled or mitered, as a two-dimensional scene draws it (see LineJointType; default AUTO: mitered).

**`cap_style`**

How the stroke ends, at each end it shows (an open path's, a dash's): round, butt or square, as a two-dimensional scene draws it (see CapStyleType; default AUTO: butt).

**`shade_in_3d`**

Whether a three-dimensional scene's light shades the mobject.

**`material`**

How its surface reflects the scene's lights in a three-dimensional scene (see Material); None: Manim's shading (default).

**`name`**

A name for the mobject; its class's name if not given.

**`z_index`**

Its place in the drawing order: a higher index is drawn over a lower one (default 0).

**`target`**

The state `MoveToTarget` moves the mobject to.

It also takes the style keywords.

Returns A new VDict, not added to the axes, with the line under `"line_graph"` and the dots, in a group, under `"vertex_dots"`.

        import manimgx as m

        class AxesPlotLineGraphExample(m.Scene):
            def construct(self) -> None:
                axes = m.Axes(x_range=[0, 7], y_range=[0, 5], y_length=6)
                graph = axes.plot_line_graph(
                    x_values=[0, 1.5, 2, 2.8, 4, 6.25],
                    y_values=[1, 3, 2.25, 4, 2.5, 1.75],
                    line_color=m.ORANGE,
                    vertex_dot_radius=0.12,
                    vertex_dot_style={"color": m.PURPLE},
                    stroke_width=6,
                )
                self.add(axes.add_coordinates())
                self.play(m.Create(graph))
        ```
    """
    xs, ys = (
        np.array(list(x_values), dtype=float),
        np.array(list(y_values), dtype=float),
    )
    zs = (
        np.zeros(xs.shape)
        if z_values is None
        else np.array(list(z_values), dtype=float)
    )
    line_graph = VDict()
    if kwargs.get("color") is None:  # not given, None too
        kwargs["color"] = line_color
    graph = VMobject(**kwargs)
    vertices = self.coords_to_point(*np.array((xs, ys, zs))).T
    graph.set_points_as_corners(vertices)
    line_graph["line_graph"] = graph
    if add_vertex_dots:
        line_graph["vertex_dots"] = VGroup(
            *(
                Dot(
                    point=vertex.copy(),  # the dot retains its center
                    radius=vertex_dot_radius,
                    **(vertex_dot_style or Style()),
                )
                for vertex in vertices
            )
        )
    return line_graph
````

### plot\_polar\_graph

**Code**

```python
import numpy as np

import manimgx as m

class AxesPlotPolarGraphExample(m.Scene):
    def construct(self) -> None:
        plane = m.PolarPlane(radius_max=3, size=7.5)
        rose = plane.plot_polar_graph(
            lambda theta: 3 * np.sin(5 * theta), color=m.ORANGE
        )
        self.add(plane)
        self.play(m.Create(rose), run_time=3)
```

Plot a curve in polar coordinates, r = r\_func(θ), on the axes: for each angle θ of its range, the point in the direction θ from the origin, at the distance `r_func(θ)`.

```python
axes.plot_polar_graph(r_func, theta_range=None, **kwargs)
```

**`r_func`**

The function, from the angle θ, in radians, to the distance r, in the axes' units.

**`theta_range`**

The range of θ, `[θ_min, θ_max]` or `[θ_min, θ_max, θ_step]`, in radians, sampled every 0.01 without a step; None for a full turn, \[0, 2π\].

**`dt`**

How far short of each discontinuity the curve's pieces stop, in units of its parameter (default 1e-8).

**`discontinuities`**

The values of the parameter where the curve breaks: it is drawn in pieces between them (default None: none).

**`use_smoothing`**

Whether the samples are joined by a smooth curve through them, rather than by straight segments (default True).

**`color`**

The color of both fill and stroke (default white); None for the class's default.

**`fill_color`**

The fill's color; `color` if not given. Several colors make a gradient along `sheen_direction`.

**`fill_opacity`**

The fill's opacity, from 0 to 1 (default 0: no fill).

**`stroke_color`**

The stroke's color; `color` if not given. Several colors make a gradient.

**`stroke_opacity`**

The stroke's opacity, from 0 to 1 (default 1).

**`stroke_width`**

The stroke's width, in hundredths of a scene unit (default 4; 0: no stroke).

**`background_stroke_color`**

The color of an outline drawn behind the fill (default black).

**`background_stroke_opacity`**

The outline's opacity, from 0 to 1 (default 1).

**`background_stroke_width`**

The outline's width, in hundredths of a scene unit (default 0: none).

**`sheen_factor`**

How much the colors lighten toward `sheen_direction`, from -1 to 1 (default 0); a negative factor darkens.

**`sheen_direction`**

The direction the colors lighten toward (default `UL`).

**`joint_type`**

How the stroke is joined where its path turns: round, beveled or mitered, as a two-dimensional scene draws it (see LineJointType; default AUTO: mitered).

**`cap_style`**

How the stroke ends, at each end it shows (an open path's, a dash's): round, butt or square, as a two-dimensional scene draws it (see CapStyleType; default AUTO: butt).

**`shade_in_3d`**

Whether a three-dimensional scene's light shades the mobject.

**`material`**

How its surface reflects the scene's lights in a three-dimensional scene (see Material); None: Manim's shading (default).

**`name`**

A name for the mobject; its class's name if not given.

**`z_index`**

Its place in the drawing order: a higher index is drawn over a lower one (default 0).

**`target`**

The state `MoveToTarget` moves the mobject to.

Returns A new ParametricFunction, not added to the axes.

        import numpy as np

        import manimgx as m

        class AxesPlotPolarGraphExample(m.Scene):
            def construct(self) -> None:
                plane = m.PolarPlane(radius_max=3, size=7.5)
                rose = plane.plot_polar_graph(
                    lambda theta: 3 * np.sin(5 * theta), color=m.ORANGE
                )
                self.add(plane)
                self.play(m.Create(rose), run_time=3)
        ```
    """
    theta_range = theta_range if theta_range is not None else [0, 2 * PI]
    return ParametricFunction(
        function=lambda th: self.pr2pt(r_func(th), th),
        t_range=theta_range,
        **kwargs,
    )
````

### plot\_implicit\_curve

**Code**

```python
import manimgx as m

class AxesPlotImplicitCurveExample(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[-3, 3], y_range=[-3, 3], y_length=7)
        curve = axes.plot_implicit_curve(
            lambda x, y: y**2 - x**3 + 2 * x - 1, color=m.YELLOW
        )
        self.add(axes)
        self.play(m.Create(curve))
```

Plot the curve where a function of x and y is zero, `func(x, y) = 0`, on the axes, in their coordinates: found within their ranges.

The rectangle of the ranges is divided in four, and each part in four again, finer where the curve passes (see ImplicitFunction). On a logarithmic axis, the function is given powers.

```python
axes.plot_implicit_curve(func, min_depth=5, max_quads=1500, **kwargs)
```

**`func`**

The function of x and y, in the axes' coordinates.

**`min_depth`**

How many times the rectangle is at least divided in four: more finds smaller pieces of the curve.

**`max_quads`**

The most cells the rectangle may be divided into: more follow the curve more closely, and take longer.

**`use_smoothing`**

Whether the curve is smoothed through its points, rather than drawn in straight segments (default True).

**`color`**

The color of both fill and stroke (default white); None for the class's default.

**`fill_color`**

The fill's color; `color` if not given. Several colors make a gradient along `sheen_direction`.

**`fill_opacity`**

The fill's opacity, from 0 to 1 (default 0: no fill).

**`stroke_color`**

The stroke's color; `color` if not given. Several colors make a gradient.

**`stroke_opacity`**

The stroke's opacity, from 0 to 1 (default 1).

**`stroke_width`**

The stroke's width, in hundredths of a scene unit (default 4; 0: no stroke).

**`background_stroke_color`**

The color of an outline drawn behind the fill (default black).

**`background_stroke_opacity`**

The outline's opacity, from 0 to 1 (default 1).

**`background_stroke_width`**

The outline's width, in hundredths of a scene unit (default 0: none).

**`sheen_factor`**

How much the colors lighten toward `sheen_direction`, from -1 to 1 (default 0); a negative factor darkens.

**`sheen_direction`**

The direction the colors lighten toward (default `UL`).

**`joint_type`**

How the stroke is joined where its path turns: round, beveled or mitered, as a two-dimensional scene draws it (see LineJointType; default AUTO: mitered).

**`cap_style`**

How the stroke ends, at each end it shows (an open path's, a dash's): round, butt or square, as a two-dimensional scene draws it (see CapStyleType; default AUTO: butt).

**`shade_in_3d`**

Whether a three-dimensional scene's light shades the mobject.

**`material`**

How its surface reflects the scene's lights in a three-dimensional scene (see Material); None: Manim's shading (default).

**`name`**

A name for the mobject; its class's name if not given.

**`z_index`**

Its place in the drawing order: a higher index is drawn over a lower one (default 0).

**`target`**

The state `MoveToTarget` moves the mobject to.

Returns A new ImplicitFunction, not added to the axes.

        import manimgx as m

        class AxesPlotImplicitCurveExample(m.Scene):
            def construct(self) -> None:
                axes = m.Axes(x_range=[-3, 3], y_range=[-3, 3], y_length=7)
                curve = axes.plot_implicit_curve(
                    lambda x, y: y**2 - x**3 + 2 * x - 1, color=m.YELLOW
                )
                self.add(axes)
                self.play(m.Create(curve))
        ```
    """
    x_scale = self.get_x_axis().scaling
    y_scale = self.get_y_axis().scaling
    graph = ImplicitFunction(
        func=lambda x, y: func(x_scale.function(x), y_scale.function(y)),
        x_range=self.x_range[:2],
        y_range=self.y_range[:2],
        min_depth=min_depth,
        max_quads=max_quads,
        **kwargs,
    )
    graph.stretch(self.get_x_unit_size(), 0, about_point=ORIGIN).stretch(
        self.get_y_unit_size(), 1, about_point=ORIGIN
    ).shift(self.get_origin())
    return graph
````

### plot\_derivative\_graph

**Code**

```python
import manimgx as m

class AxesPlotDerivativeGraphExample(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[-3, 3], y_range=[-3, 4], y_length=6.5)
        cubic = axes.plot(lambda x: x**3 / 6 - x, color=m.BLUE)
        derivative = axes.plot_derivative_graph(cubic)
        labels = m.VGroup(
            axes.get_graph_label(cubic, "f(x)", x_val=-1.4, direction=m.UP),
            axes.get_graph_label(derivative, "f'(x)", x_val=2.5),
        )
        self.add(axes, cubic, labels[0])
        self.play(m.Create(derivative), m.FadeIn(labels[1]))
```

Plot the derivative of a graph: at each x, its slope; green unless styled.

```python
axes.plot_derivative_graph(graph, **kwargs)
```

It also takes the `plot` keywords.

Returns A new ParametricFunction, not added to the axes.

        import manimgx as m

        class AxesPlotDerivativeGraphExample(m.Scene):
            def construct(self) -> None:
                axes = m.Axes(x_range=[-3, 3], y_range=[-3, 4], y_length=6.5)
                cubic = axes.plot(lambda x: x**3 / 6 - x, color=m.BLUE)
                derivative = axes.plot_derivative_graph(cubic)
                labels = m.VGroup(
                    axes.get_graph_label(cubic, "f(x)", x_val=-1.4, direction=m.UP),
                    axes.get_graph_label(derivative, "f'(x)", x_val=2.5),
                )
                self.add(axes, cubic, labels[0])
                self.play(m.Create(derivative), m.FadeIn(labels[1]))
        ```
    """
    if kwargs.get("color") is None:  # not given, None too
        kwargs["color"] = GREEN
    return self.plot(lambda x: self.slope_of_tangent(x, graph), **kwargs)
````

### plot\_antiderivative\_graph

**Code**

```python
import manimgx as m

class AxesPlotAntiderivativeGraphExample(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[-3, 3], y_range=[-3, 3], y_length=6.5)
        graph = axes.plot(lambda x: (x**2 - 2) / 3, color=m.RED)
        antiderivative = axes.plot_antiderivative_graph(
            graph, y_intercept=1, color=m.BLUE
        )
        self.add(axes, graph)
        self.play(m.Create(antiderivative))
```

Plot an antiderivative of a graph: at each x, the integral of the graph from 0 to x, plus `y_intercept`.

Each value is a trapezoidal sum of the graph's values at `samples` points from 0 to x.

```python
axes.plot_antiderivative_graph(graph, y_intercept=0, samples=50, **kwargs)
```

**`y_intercept`**

The antiderivative's value at 0.

**`samples`**

How many of the graph's values each integral sums.

It also takes the `plot` keywords.

Returns A new ParametricFunction, not added to the axes.

        import manimgx as m

        class AxesPlotAntiderivativeGraphExample(m.Scene):
            def construct(self) -> None:
                axes = m.Axes(x_range=[-3, 3], y_range=[-3, 3], y_length=6.5)
                graph = axes.plot(lambda x: (x**2 - 2) / 3, color=m.RED)
                antiderivative = axes.plot_antiderivative_graph(
                    graph, y_intercept=1, color=m.BLUE
                )
                self.add(axes, graph)
                self.play(m.Create(antiderivative))
        ```
    """
    axis = 1 if kwargs.get("use_vectorized", False) else 0
    f_vec = np.vectorize(
        graph.underlying_function
        or (lambda x: self.input_to_graph_coords(x, graph)[1])
    )

    def antideriv(x: float) -> float:
        x_vals = np.linspace(0, x, samples, axis=axis)
        return float(np.trapezoid(f_vec(x_vals), x_vals) + y_intercept)

    return self.plot(antideriv, **kwargs)
````

## Points on a graph

### input\_to\_graph\_point

**Code**

```python
import numpy as np

import manimgx as m

class AxesInputToGraphPointExample(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[0, 7], y_range=[-1.5, 1.5, 0.5])
        curve = axes.plot(np.cos, color=m.BLUE)
        dots = m.VGroup(
            *(m.Dot(axes.i2gp(x, curve), radius=0.12) for x in range(7))
        )
        self.add(axes, curve, dots.set_color(m.YELLOW))
```

Find the point of a graph at an input: at x, for a graph of plot; at a value of its parameter, for another curve.

`i2gp` is its short name. The input may be past the graph's ends: the point is then its function's, beyond what is drawn.

```python
axes.input_to_graph_point(x, graph)
```

**`x`**

The input: x, in the axes' coordinates, for a graph.

**`graph`**

The graph, or curve.

Returns The point, in scene coordinates.

        import numpy as np

        import manimgx as m

        class AxesInputToGraphPointExample(m.Scene):
            def construct(self) -> None:
                axes = m.Axes(x_range=[0, 7], y_range=[-1.5, 1.5, 0.5])
                curve = axes.plot(np.cos, color=m.BLUE)
                dots = m.VGroup(
                    *(m.Dot(axes.i2gp(x, curve), radius=0.12) for x in range(7))
                )
                self.add(axes, curve, dots.set_color(m.YELLOW))
        ```
    """
    return graph.function(x)
````

### i2gp

input\_to\_graph\_point, by a shorter name.

### input\_to\_graph\_coords

Find the coordinates of a graph's point at an input: (x, f(x)), for a graph of plot; for another curve, those of its point at a value of its parameter.

```python
axes.input_to_graph_coords(x, graph)
```

**`x`**

The input: x, for a graph.

**`graph`**

The graph, or curve.

Returns The point's coordinates, (x, y).

### get\_graph\_label

**Code**

```python
import numpy as np

import manimgx as m

class AxesGetGraphLabelExample(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[-4, 4], y_range=[-2, 4], x_length=11)
        parabola = axes.plot(lambda x: x**2 / 4, color=m.BLUE)
        sine = axes.plot(np.sin, color=m.YELLOW)
        parabola_label = axes.get_graph_label(parabola, "x^2 / 4")
        sine_label = axes.get_graph_label(
            sine, r"\sin x", x_val=m.PI / 2, direction=m.UP, dot=True
        )
        self.add(axes, parabola, sine, parabola_label, sine_label)
```

Make a label for a graph, by one of its points: in the graph's color, unless given another.

A string or a number is typeset with the axes' `label_constructor` (as math, with MathTex, by default); a mobject is used as it is, and recolored too. The label is put next to the graph's point at `x_val`, toward `direction`, then moved onto the screen if it is off it. Without `x_val`, the point is the rightmost, of a hundred over the x-axis's range, that is below the top of the frame.

```python
axes.get_graph_label(graph, label='f(x)', x_val=None, direction=RIGHT, buff=MED_SMALL_BUFF, color=None, dot=False, dot_config=None)
```

**`label`**

The label: a string or a number, typeset as math, or a mobject.

**`x_val`**

The x of the point the label is put by; None for the rightmost on screen.

**`direction`**

The direction the label is put toward, from the point.

**`buff`**

The gap between the point and the label, in scene units.

**`color`**

The label's color; None for the graph's.

**`dot`**

Whether a dot marks the point, as part of the label.

**`dot_config`**

Style keywords for the dot; None for none.

Returns The label, not added to the axes.

        import numpy as np

        import manimgx as m

        class AxesGetGraphLabelExample(m.Scene):
            def construct(self) -> None:
                axes = m.Axes(x_range=[-4, 4], y_range=[-2, 4], x_length=11)
                parabola = axes.plot(lambda x: x**2 / 4, color=m.BLUE)
                sine = axes.plot(np.sin, color=m.YELLOW)
                parabola_label = axes.get_graph_label(parabola, "x^2 / 4")
                sine_label = axes.get_graph_label(
                    sine, r"\sin x", x_val=m.PI / 2, direction=m.UP, dot=True
                )
                self.add(axes, parabola, sine, parabola_label, sine_label)
        ```
    """
    label_object: Mobject = self.x_axis._create_label_tex(label).set_color(
        graph.get_color() if color is None else color
    )
    if x_val is None:  # the rightmost point of the graph that is on screen
        xs = np.linspace(self.x_range[1], self.x_range[0], 100)
        points = (self.input_to_graph_point(x, graph) for x in xs)
        point = next(
            (p for p in points if p[1] < config["frame_y_radius"]),
            self.input_to_graph_point(xs[-1], graph),
        )
    else:
        point = self.input_to_graph_point(x_val, graph)
    label_object.next_to(point, direction, buff=buff)
    label_object.shift_onto_screen()
    if dot:
        label_object.add(Dot(point=point, **(dot_config or Style())))
    return label_object
````

### get\_T\_label

**Code**

```python
import numpy as np

import manimgx as m

class AxesGetTLabelExample(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[0, 10], y_range=[0, 10], y_length=6)
        graph = axes.plot(lambda x: 3 * np.sqrt(x), color=m.BLUE)
        t_label = axes.get_T_label(4, graph, label=m.MathTex("x = 4"))
        self.add(axes, graph)
        self.play(m.FadeIn(t_label))
```

Make a T-label for a value of x: a small triangle under the x-axis pointing up at the value, a label below the triangle, and a line from the x-axis up to the graph.

```python
axes.get_T_label(x_val, graph, label=None, label_color=None, triangle_size=MED_SMALL_BUFF, triangle_color=WHITE, line_func=Line, line_color=PURE_YELLOW)
```

**`x_val`**

The value of x it marks.

**`graph`**

The graph the line reaches.

**`label`**

The label below the triangle: a string or a number, typeset as math, or a mobject; None for none.

**`label_color`**

The label's color; None to leave it as it is.

**`triangle_size`**

The triangle's height, in scene units.

**`triangle_color`**

The triangle's color.

**`line_func`**

The class of the line: Line (solid), DashedLine, ….

**`line_color`**

The line's color.

Returns A new group of the label (if any), the triangle and the line; not added to the axes.

        import numpy as np

        import manimgx as m

        class AxesGetTLabelExample(m.Scene):
            def construct(self) -> None:
                axes = m.Axes(x_range=[0, 10], y_range=[0, 10], y_length=6)
                graph = axes.plot(lambda x: 3 * np.sqrt(x), color=m.BLUE)
                t_label = axes.get_T_label(4, graph, label=m.MathTex("x = 4"))
                self.add(axes, graph)
                self.play(m.FadeIn(t_label))
        ```
    """
    T_label_group = VGroup()
    triangle = RegularPolygon(n=3, start_angle=np.pi / 2, stroke_width=0).set_fill(
        color=triangle_color, opacity=1
    )
    triangle.height = triangle_size
    triangle.move_to(self.coords_to_point(x_val, 0), UP)
    if label is not None:
        t_label = self.x_axis._create_label_tex(label)
        if label_color is not None:
            t_label.set_color(label_color)
        t_label.next_to(triangle, DOWN)
        T_label_group.add(t_label)
    v_line = self.get_vertical_line(
        self.i2gp(x_val, graph), color=line_color, line_func=line_func
    )
    T_label_group.add(triangle, v_line)
    return T_label_group
````

### get\_vertical\_lines\_to\_graph

**Code**

```python
import numpy as np

import manimgx as m

class AxesGetVerticalLinesToGraphExample(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[0, 8], y_range=[-1, 1, 0.5], y_length=5)
        curve = axes.plot(
            lambda x: np.sin(2 * x) * np.exp(-x / 4), color=m.YELLOW
        )
        lines = axes.get_vertical_lines_to_graph(
            curve, x_range=[0.5, 7.5], num_lines=15, color=m.BLUE
        )
        self.add(axes, curve)
        self.play(m.Create(lines))
```

Make lines from the x-axis to a graph, evenly spaced over a range of x: dashed, white and thin unless styled.

```python
axes.get_vertical_lines_to_graph(graph, x_range=None, num_lines=20, **kwargs)
```

**`x_range`**

The range of x, `[x_min, x_max]`: the first line at x\_min, the last at x\_max; None for the x-axis's range.

**`num_lines`**

How many lines.

**`line_func`**

The class of the line (default DashedLine; a Line is solid).

**`line_config`**

Dashed line keywords for the line, but its color and width, which `color` and `stroke_width` set (default None: none).

**`color`**

The line's color (default None: white).

**`stroke_width`**

The line's width, in hundredths of a scene unit (default 2).

Returns A new group of the lines, from left to right; not added to the axes.

        import numpy as np

        import manimgx as m

        class AxesGetVerticalLinesToGraphExample(m.Scene):
            def construct(self) -> None:
                axes = m.Axes(x_range=[0, 8], y_range=[-1, 1, 0.5], y_length=5)
                curve = axes.plot(
                    lambda x: np.sin(2 * x) * np.exp(-x / 4), color=m.YELLOW
                )
                lines = axes.get_vertical_lines_to_graph(
                    curve, x_range=[0.5, 7.5], num_lines=15, color=m.BLUE
                )
                self.add(axes, curve)
                self.play(m.Create(lines))
        ```
    """
    x_range = x_range if x_range is not None else self.x_range
    return VGroup(
        *(
            self.get_vertical_line(self.i2gp(x, graph), **kwargs)
            for x in np.linspace(x_range[0], x_range[1], num_lines)
        )
    )
````

## Areas

### get\_area

**Code**

```python
import manimgx as m

class AxesGetAreaExample(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[0, 5], y_range=[0, 6], y_length=6.5)
        curve = axes.plot(lambda x: 5 - (x - 2.5) ** 2 / 2, color=m.BLUE)
        line = axes.plot(lambda x: x / 2, color=m.YELLOW)
        under = axes.get_area(curve, x_range=(0.5, 2))
        between = axes.get_area(
            curve, x_range=(3, 4.5), bounded_graph=line, color=m.RED
        )
        self.add(axes, under, between, curve, line)
```

Make the area between a graph and the x-axis, or between two graphs, over a range of x: a polygon, blue to green and translucent unless styled.

The area's edge follows the graph's own points, and closes along the x-axis, or back along `bounded_graph`; its fill and outline both take `color` and `opacity`. Two graphs whose ranges do not meet raise a ValueError.

```python
axes.get_area(graph, x_range=None, color=(BLUE, GREEN), opacity=0.3, bounded_graph=None, **kwargs)
```

**`x_range`**

The range of x, `(x_min, x_max)`; None for the graph's.

**`color`**

The area's color, or colors for a gradient.

**`opacity`**

The area's opacity, from 0 to 1.

**`bounded_graph`**

A second graph the area reaches to, rather than the x-axis; None for the x-axis. Only the range both graphs span is covered.

**`fill_color`**

The fill's color; `color` if not given. Several colors make a gradient along `sheen_direction`.

**`fill_opacity`**

The fill's opacity, from 0 to 1 (default 0: no fill).

**`stroke_color`**

The stroke's color; `color` if not given. Several colors make a gradient.

**`stroke_opacity`**

The stroke's opacity, from 0 to 1 (default 1).

**`stroke_width`**

The stroke's width, in hundredths of a scene unit (default 4; 0: no stroke).

**`background_stroke_color`**

The color of an outline drawn behind the fill (default black).

**`background_stroke_opacity`**

The outline's opacity, from 0 to 1 (default 1).

**`background_stroke_width`**

The outline's width, in hundredths of a scene unit (default 0: none).

**`sheen_factor`**

How much the colors lighten toward `sheen_direction`, from -1 to 1 (default 0); a negative factor darkens.

**`sheen_direction`**

The direction the colors lighten toward (default `UL`).

**`joint_type`**

How the stroke is joined where its path turns: round, beveled or mitered, as a two-dimensional scene draws it (see LineJointType; default AUTO: mitered).

**`cap_style`**

How the stroke ends, at each end it shows (an open path's, a dash's): round, butt or square, as a two-dimensional scene draws it (see CapStyleType; default AUTO: butt).

**`shade_in_3d`**

Whether a three-dimensional scene's light shades the mobject.

**`material`**

How its surface reflects the scene's lights in a three-dimensional scene (see Material); None: Manim's shading (default).

**`name`**

A name for the mobject; its class's name if not given.

**`z_index`**

Its place in the drawing order: a higher index is drawn over a lower one (default 0).

**`target`**

The state `MoveToTarget` moves the mobject to.

It also takes the style keywords.

Returns A new Polygon, not added to the axes.

        import manimgx as m

        class AxesGetAreaExample(m.Scene):
            def construct(self) -> None:
                axes = m.Axes(x_range=[0, 5], y_range=[0, 6], y_length=6.5)
                curve = axes.plot(lambda x: 5 - (x - 2.5) ** 2 / 2, color=m.BLUE)
                line = axes.plot(lambda x: x / 2, color=m.YELLOW)
                under = axes.get_area(curve, x_range=(0.5, 2))
                between = axes.get_area(
                    curve, x_range=(3, 4.5), bounded_graph=line, color=m.RED
                )
                self.add(axes, under, between, curve, line)
        ```
    """
    if x_range is None:
        a = graph.t_min
        b = graph.t_max
    else:
        a, b = x_range
    if bounded_graph is not None:
        if bounded_graph.t_min > b:
            raise ValueError(f"Ranges not matching: {bounded_graph.t_min} < {b}")
        if bounded_graph.t_max < a:
            raise ValueError(f"Ranges not matching: {bounded_graph.t_max} > {a}")
        a = max(a, bounded_graph.t_min)
        b = min(b, bounded_graph.t_max)
    if bounded_graph is None:
        points = (
            [self.c2p(a), graph.function(a)]
            + [p for p in graph.points if a <= self.p2c(p)[0] <= b]
            + [graph.function(b), self.c2p(b)]
        )
    else:
        graph_points, bounded_graph_points = (
            [g.function(a)]
            + [p for p in g.points if a <= self.p2c(p)[0] <= b]
            + [g.function(b)]
            for g in (graph, bounded_graph)
        )
        points = graph_points + bounded_graph_points[::-1]
    return Polygon(*points, **kwargs).set_opacity(opacity).set_color(color)
````

### get\_riemann\_rectangles

**Code**

```python
import manimgx as m

class AxesGetRiemannRectanglesExample(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[-3, 3], y_range=[-2, 4], y_length=6.5)
        graph = axes.plot(lambda x: x**2 / 2 - 1, color=m.YELLOW)
        coarse, fine = (
            axes.get_riemann_rectangles(graph, x_range=[-2.5, 2.5], dx=dx)
            for dx in (0.5, 0.1)
        )
        self.add(axes, coarse, graph)
        self.play(m.Transform(coarse, fine), run_time=2)
```

Make Riemann rectangles for a graph: from the x-axis (or a second graph) up to the graph, `dx` wide, their colors a gradient; outlined thinly in black unless styled.

A rectangle begins at every `dx` from the start of `x_range`, the last before its end. Each rises from the x-axis — or from `bounded_graph`, at its left edge — to the graph at its left edge, its right edge or its center (`input_sample_type`). With `show_signed_area`, a rectangle where the graph is below its base takes the inverse of its color.

```python
axes.get_riemann_rectangles(graph, x_range=None, dx=0.1, input_sample_type='left', stroke_width=1, stroke_color=BLACK, fill_opacity=1, color=(BLUE, GREEN), show_signed_area=True, bounded_graph=None, blend=False, width_scale_factor=1.001)
```

**`graph`**

The graph, of plot.

**`x_range`**

The range of x the rectangles cover, `[x_min, x_max]`; None for the graph's (and `bounded_graph`'s, where both are).

**`dx`**

The rectangles' width, in the axes' units.

**`input_sample_type`**

Where each rectangle meets the graph: `"left"`, `"right"` or `"center"`.

**`stroke_width`**

The width of the rectangles' outlines, in hundredths of a scene unit.

**`stroke_color`**

The outlines' color (unless `blend`).

**`fill_opacity`**

The rectangles' opacity, from 0 to 1.

**`color`**

The rectangles' color, or colors for a gradient from the first rectangle to the last.

**`show_signed_area`**

Whether a rectangle where the graph is below its base takes the inverse of its color.

**`bounded_graph`**

A second graph, of plot, the rectangles rise from; None for the x-axis.

**`blend`**

Whether each outline takes its rectangle's color, rather than `stroke_color`.

**`width_scale_factor`**

How much wider than `dx` each rectangle is made, so that neighbours meet without a seam.

Returns A new group of the rectangles, from left to right; not added to the axes.

        import manimgx as m

        class AxesGetRiemannRectanglesExample(m.Scene):
            def construct(self) -> None:
                axes = m.Axes(x_range=[-3, 3], y_range=[-2, 4], y_length=6.5)
                graph = axes.plot(lambda x: x**2 / 2 - 1, color=m.YELLOW)
                coarse, fine = (
                    axes.get_riemann_rectangles(graph, x_range=[-2.5, 2.5], dx=dx)
                    for dx in (0.5, 0.1)
                )
                self.add(axes, coarse, graph)
                self.play(m.Transform(coarse, fine), run_time=2)
        ```
    """
    if x_range is None:
        if bounded_graph is None:
            x_range = [graph.t_min, graph.t_max]
        else:
            x_min = max(graph.t_min, bounded_graph.t_min)
            x_max = min(graph.t_max, bounded_graph.t_max)
            x_range = [x_min, x_max]
    rectangles = VGroup()
    x_range_array = np.arange(x_range[0], x_range[1], dx)
    colors = color_gradient(parse_colors(color), len(x_range_array))
    for x, color_x in zip(x_range_array, colors, strict=True):
        if input_sample_type == "left":
            sample_input = x
        elif input_sample_type == "right":
            sample_input = x + dx
        elif input_sample_type == "center":
            sample_input = x + 0.5 * dx
        else:
            raise ValueError("Invalid input sample type")
        graph_point = self.input_to_graph_point(sample_input, graph)
        if bounded_graph is None or bounded_graph.underlying_function is None:
            y_point = _origin_shift(self.y_range)
        else:
            y_point = bounded_graph.underlying_function(x)
        points = np.array(
            [
                self.coords_to_point(x, y_point),
                self.coords_to_point(x + width_scale_factor * dx, y_point),
                graph_point,
            ]
        )
        low, high = points.min(axis=0), points.max(axis=0)
        rect = Rectangle()
        rect.stretch_to_fit_width(high[0] - low[0])
        rect.stretch_to_fit_height(high[1] - low[1])
        rect.shift((low + high) / 2 - rect.get_center())
        rectangles.add(rect)
        if self.p2c(graph_point)[1] < y_point and show_signed_area:
            color_x = invert_color(color_x)
        if blend:
            stroke_color = color_x
        rect.set_style(
            fill_color=color_x,
            fill_opacity=fill_opacity,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
        )
    return rectangles
````

## Slopes

### slope\_of\_tangent

Find the slope of a graph's tangent at an input: its derivative, dy/dx, in the axes' coordinates.

It is the tangent of angle\_of\_tangent's angle.

```python
axes.slope_of_tangent(x, graph, dx=1e-08)
```

**`x`**

The input: x, for a graph of plot.

**`dx`**

The step the tangent is taken over, in the axes' units.

### angle\_of\_tangent

Find the angle of a graph's tangent at an input, in the axes' coordinates.

The tangent is taken from the graph's point at `x` to its point at `x + dx`.

```python
axes.angle_of_tangent(x, graph, dx=1e-08)
```

**`x`**

The input: x, for a graph of plot.

**`dx`**

The step the tangent is taken over, in the axes' units.

Returns The angle, in radians, counterclockwise from the direction of the x-axis, measured in the axes' coordinates: not as drawn, where their units differ.

### get\_secant\_slope\_group

**Code**

```python
import manimgx as m

class AxesGetSecantSlopeGroupExample(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[0, 5], y_range=[0, 7], y_length=6.5)
        graph = axes.plot(lambda x: x**2 / 4, color=m.BLUE)
        secant = axes.get_secant_slope_group(
            2,
            graph,
            dx=2,
            dx_label="dx",
            dy_label="dy",
            secant_line_length=7,
            secant_line_color=m.RED,
        )
        self.add(axes, graph)
        self.play(m.Create(secant))
```

Make a secant's construction on a graph, between its points at `x` and `x + dx`: the legs dx and df, their labels, and the secant through both points.

The dx leg runs across from the first point, and the df leg up (or down) to the second, in the graph's color unless given another. The labels, typeset as math unless mobjects, are scaled down together to fit their legs (to 80% of the dx leg's width and of the df leg's height), and put below the dx leg and right of the df leg (above and left, for a negative `dx`), each in its leg's color. The secant is `secant_line_length` long, centered between the points.

```python
axes.get_secant_slope_group(x, graph, dx=None, dx_line_color=PURE_YELLOW, dy_line_color=None, dx_label=None, dy_label=None, include_secant_line=True, secant_line_color=GREEN, secant_line_length=10)
```

**`x`**

The input of the first point: its x.

**`dx`**

The step to the second point, in the axes' units; None for a tenth of the x-axis's range.

**`dx_line_color`**

The dx leg's color.

**`dy_line_color`**

The df leg's color; None for the graph's.

**`dx_label`**

The dx leg's label: a string, a number or a mobject; None for none.

**`dy_label`**

The df leg's label, likewise; None for none.

**`include_secant_line`**

Whether the construction includes the secant.

**`secant_line_color`**

The secant's color.

**`secant_line_length`**

The secant's length, in scene units.

Returns A new SecantSlopeGroup, not added to the axes: its parts are its `dx_line`, `df_line`, `dx_label`, `df_label` and `secant_line`.

        import manimgx as m

        class AxesGetSecantSlopeGroupExample(m.Scene):
            def construct(self) -> None:
                axes = m.Axes(x_range=[0, 5], y_range=[0, 7], y_length=6.5)
                graph = axes.plot(lambda x: x**2 / 4, color=m.BLUE)
                secant = axes.get_secant_slope_group(
                    2,
                    graph,
                    dx=2,
                    dx_label="dx",
                    dy_label="dy",
                    secant_line_length=7,
                    secant_line_color=m.RED,
                )
                self.add(axes, graph)
                self.play(m.Create(secant))
        ```
    """
    group = SecantSlopeGroup()
    dx = dx or float(self.x_range[1] - self.x_range[0]) / 10
    dy_line_color = dy_line_color or graph.get_color()
    p1 = self.input_to_graph_point(x, graph)
    p2 = self.input_to_graph_point(x + dx, graph)
    interim_point = p2[0] * RIGHT + p1[1] * UP
    group.dx_line = Line(p1, interim_point, color=dx_line_color)
    group.df_line = Line(interim_point, p2, color=dy_line_color)
    group.add(group.dx_line, group.df_line)
    labels = VGroup()
    if dx_label is not None:
        group.dx_label = self.x_axis._create_label_tex(dx_label)
        labels.add(group.dx_label)
        group.add(group.dx_label)
    if dy_label is not None:
        group.df_label = self.x_axis._create_label_tex(dy_label)
        labels.add(group.df_label)
        group.add(group.df_label)
    if len(labels) > 0:
        max_width = 0.8 * group.dx_line.width
        max_height = 0.8 * group.df_line.height
        if labels.width > max_width:
            labels.width = max_width
        if labels.height > max_height:
            labels.height = max_height
    if dx_label is not None:
        group.dx_label.next_to(
            group.dx_line, np.sign(dx) * DOWN, buff=group.dx_label.height / 2
        )
        group.dx_label.set_color(group.dx_line.get_color())
    if dy_label is not None:
        group.df_label.next_to(
            group.df_line, np.sign(dx) * RIGHT, buff=group.df_label.height / 2
        )
        group.df_label.set_color(group.df_line.get_color())
    if include_secant_line:
        group.secant_line = Line(p1, p2, color=secant_line_color)
        group.secant_line.scale(secant_line_length / group.secant_line.get_length())
        group.add(group.secant_line)
    return group
````

### SecantSlopeGroup

A secant's construction, as get\_secant\_slope\_group makes it: its dx and df legs, their labels and the secant line, each by name.

#### dx\_line

The horizontal leg: from the first point of the graph across to below (or above) the second.

#### df\_line

The vertical leg: from the end of `dx_line` to the second point.

#### dx\_label

The horizontal leg's label, if it has one.

#### df\_label

The vertical leg's label, if it has one.

#### secant\_line

The secant: the line through both points, if it has one.
