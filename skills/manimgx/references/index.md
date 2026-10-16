# ManimGX references: index

Docs from https://manimgx.academa.ai/llms-full.txt (ManimGX 0.1.1), one file per page.
Implementation `**Source**` blocks are dropped. Find a name: `grep -rn "^### Name" references/api/`.

## Overview (`intro/`)

The llms.txt agent instructions: install, the scene loop, the API cheat sheet.

- `intro/llms.md`: ManimGX

## User guide (`guide/`)

How a scene works, page by page. Read these first for a new kind of task.

- `guide/animations.md`: Animations
- `guide/camera-and-3d.md`: Camera and 3D
- `guide/coming-from-manim-ce.md`: Coming from Manim CE
- `guide/graphs.md`: Graphs
- `guide/mobjects.md`: Mobjects
- `guide/positions.md`: Positions
- `guide/quickstart.md`: Quickstart
- `guide/rendering-and-sharing.md`: Rendering and sharing
- `guide/sound-and-voice.md`: Sound and voice
- `guide/text-and-math.md`: Text and math
- `guide/the-basics.md`: The basics
- `guide/updaters.md`: Updaters
- `guide/welcome.md`: User Guide

## API reference (`api/`)

Every class, its keywords, defaults and a runnable example. `### Name` = one class/function.

- `api/3d-scenes.md`: **3D scenes**: set_camera_orientation, begin_ambient_camera_rotation, stop_ambient_camera_rotation, begin_3dillusion_camera_rotation, stop_3dillusion_camera_rotation, move_camera, add_fixed_in_frame_mobjects
- `api/animate-a-change.md`: **Animate a change**: MoveToTarget, Restore
- `api/animations.md`: **Animations**: AnimationOptions, Animation
- `api/annotations.md`: **Annotations**: Brace, BraceBetweenPoints, ArcBrace, BraceLabel, BraceText, SurroundingRectangle, BackgroundRectangle, FrameOptions, Underline, Cross, AnnotationDot, Label, LabeledDot, LabeledLine, LabeledArrow, LabeledPolygram, Angle, RightAngle, Elbow
- `api/appear-and-disappear.md`: **Appear and disappear**: Create, Uncreate, DrawBorderThenFill, Write, Unwrite, FadeIn, FadeOut, GrowFromCenter, GrowFromPoint, GrowFromEdge, GrowArrow, SpinInFromNothing, ShrinkToCenter, SpiralIn, ShowIncreasingSubsets, ShowSubmobjectsOneByOne, AddTextLetterByLetter, RemoveTextLetterByLetter, AddTextWordByWord, TypeWithCursor, UntypeWithCursor
- `api/axes.md`: **Axes**: x_range, y_range, x_axis, y_axis, axes, coords_to_point, point_to_coords, polar_to_point, get_origin, get_x_unit_size, get_y_unit_size, get_x_axis, get_y_axis, get_z_axis, get_axis, get_axes, add_coordinates, get_axis_labels, get_x_axis_label, get_y_axis_label, get_vertical_line, get_horizontal_line, get_lines_to_point, ThreeDAxes
- `api/camera-and-3d.md`: **Camera and 3D**
- `api/camera.md`: **Camera**: frame, frame_center, frame_width, frame_height, auto_zoom, background_color, background_opacity, exposure, tone_mapping, bloom, ambient_occlusion, ambient_occlusion_radius, light_source, fixed_in_frame_mobjects, add_fixed_in_frame_mobjects, three_d, get_phi, get_theta, get_gamma, get_zoom, get_focal_distance, set_phi, set_theta, set_gamma
- `api/charts.md`: **Charts**: values, bars, get_bar_labels, change_bar_values, get_division_along_dimension, get_vertical_division, divide_vertically
- `api/circles-and-arcs.md`: **Circles and arcs**: surround, point_at_angle, from_three_points, get_arc_center, move_arc_center_to, stop_angle
- `api/colors.md`: **Colors**: m.PALETTE, ManimColor, HSV, interpolate_color, color_gradient, average_color, invert_color, colors_by_value, random_color, random_bright_color, RandomColorGenerator
- `api/combining-shapes.md`: **Combining shapes**
- `api/command-line.md`: **Command line**
- `api/configuration.md`: **Configuration**: pixel_width, pixel_height, frame_rate, simulation_rate, background_color, background_opacity, frame_height, frame_width, frame_x_radius, frame_y_radius, top, bottom, right_side, left_side, aspect_ratio, background
- `api/copies-and-states.md`: **Copies and states**: save_state, restore, generate_target, target, become, match_points
- `api/curves.md`: **Curves**: x_range, parametric_function, underlying_function, function, get_function, get_point_from_function
- `api/emphasis.md`: **Emphasis**
- `api/from-python.md`: **From Python**: fps, video, frames, frame_count, plays, sections, subcaptions, clips, export, soundtrack, cut, subtitles, captions, failure, open, wait, close, Frame, Play, Section, Export, Cut, Take, FrameSink, PlayHook, manimgx.audio.sound.RATE
- `api/graphs.md`: **Graphs**
- `api/groups.md`: **Groups**: submobjects, add, add_to_back, insert, remove, get_family, family_members_with_points, arrange, arrange_in_grid, sort, shuffle, invert, VDict, index_labels
- `api/images-and-svg.md`: **Images and SVG**: pixel_array, set_color, set_opacity, set_resampling_algorithm, m.RESAMPLING_ALGORITHMS, Resampling, id_to_vgroup_dict, PathOptions
- `api/lights-and-materials.md`: **Lights and materials**: Light, SunLight, PointLight, SpotLight, AmbientLight, EnvironmentLight, Material, set_material, set_shade_in_3d
- `api/lines-and-arrows.md`: **Lines and arrows**: set_path_arc, put_start_and_end_on, get_vector, get_unit_vector, get_angle, get_projection, get_slope, set_angle, set_length, scale, coordinate_label, TipableVMobject, TippedBase
- `api/math.md`: **Math**: tex_strings, tex_string, get_parts_by_tex, get_part_by_tex, index_of_part, set_color_by_tex, set_color_by_tex_to_color_map, typst_code, typst_preamble, font_size, select, scale, TypstGlyph, manimgx.drawing.typesetting.TypstError
- `api/matrices-and-tables.md`: **Matrices and tables**: entry, entry_config, elements, get_rows, get_columns, set_row_colors, set_column_colors, get_entries, get_brackets, DecimalMatrix, IntegerMatrix, MobjectMatrix, row_labels, col_labels, top_left_entry, row_dim, col_dim, v_buff, h_buff, elements_without_labels, get_horizontal_lines, get_vertical_lines, get_entries_without_labels, get_row_labels, get_col_labels, get_labels, add_background_to_entries, get_cell, get_highlighted_cell, add_highlighted_cell, create, DecimalTable, IntegerTable, MathTable, MobjectTable
- `api/mobjects.md`: **Mobjects**: Mobject
- `api/move-and-deform.md`: **Move and deform**: Rotate, Rotating, MoveAlongPath, ApplyFunction, ApplyPointwiseFunction, ApplyMatrix, ApplyComplexFunction, Homotopy, ComplexHomotopy, ApplyWave, PhaseFlow
- `api/networks.md`: **Networks**: TipConfig, GenericGraph
- `api/number-lines.md`: **Number lines**: x_range, x_min, x_max, x_step, unit_size, scaling, rotate_about_zero, rotate_about_number, number_to_point, point_to_number, n2p, get_unit_size, get_unit_vector, get_number_mobject, add_numbers, add_labels, LinearBase, LogBase
- `api/numbers.md`: **Numbers**: font_size, get_value, increment_value, set_value, label, tracker, value, ChangeDecimalToValue, ChangingDecimal
- `api/overview.md`: **Reference**
- `api/paths.md`: **Paths**: set_points_as_corners, set_points_smoothly, start_new_path, add_line_to, add_points_as_corners, add_smooth_curve_to, add_cubic_bezier_curve_to, add_quadratic_bezier_curve_to, add_cubic_bezier_curve, add_cubic_bezier_curves, add_subpath, append_vectorized_mobject, close_path, is_closed, make_smooth, make_jagged, insert_n_curves, get_start, get_end, get_midpoint, point_from_proportion, proportion_from_point, get_arc_length, get_subcurve, get_direction, reverse_direction, force_direction, points, set_points, reset_points, has_points, append_points, get_anchors, get_subpaths, get_num_curves, bezier, CubicBezier, DashedVMobject, CurvesAsSubmobjects, VectorizedPoint
- `api/planes.md`: **Planes**: prepare_for_nonlinear_transform, number_to_point, point_to_number, get_coordinate_labels, add_coordinates, get_radian_label, complex_to_R3, R3_to_complex, complex_func_to_R3_func
- `api/plotting.md`: **Plotting**: plot, plot_line_graph, plot_polar_graph, plot_implicit_curve, plot_derivative_graph, plot_antiderivative_graph, input_to_graph_point, i2gp, input_to_graph_coords, get_graph_label, get_T_label, get_vertical_lines_to_graph, get_area, get_riemann_rectangles, slope_of_tangent, angle_of_tangent, get_secant_slope_group, SecantSlopeGroup
- `api/point-clouds.md`: **Point clouds**: add_points, thin_out
- `api/polygons.md`: **Polygons**: get_vertices, get_vertex_groups, round_corners, side_length, grid_lines, arcs, ScreenRectangle, FullScreenRectangle
- `api/positions.md`: **Positions**: m.ORIGIN, m.UP, m.DOWN, m.LEFT, m.RIGHT, m.UL, m.UR, m.DL, m.DR, m.IN, m.OUT, m.X_AXIS, m.Y_AXIS, m.Z_AXIS, get_center, get_top, get_bottom, get_left, get_right, get_corner, get_critical_point, get_boundary_point, get_x, get_y, get_z, boundary_box, move_to, shift, center, set_x, set_y, set_z, m.SMALL_BUFF, m.MED_SMALL_BUFF, m.MED_LARGE_BUFF, m.LARGE_BUFF, m.DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, m.DEFAULT_MOBJECT_TO_EDGE_BUFFER, next_to, align_to, match_x, match_y, match_z, to_edge, to_corner, shift_onto_screen, is_off_screen, interpolate, midpoint, normalize, rotate_vector, angle_of_vector, angle_between_vectors, line_intersection, perpendicular_bisector, polylabel, inverse_interpolate
- `api/rate-functions.md`: **Rate functions**: smooth, linear, rush_into, rush_from, slow_into, double_smooth, there_and_back, there_and_back_with_pause, running_start, lingering, wiggle, exponential_decay, smoothstep, smootherstep, ease_in_back, ease_in_bounce, ease_in_circ, ease_in_cubic, ease_in_elastic, ease_in_expo, ease_in_out_back, ease_in_out_bounce, ease_in_out_circ, ease_in_out_cubic, ease_in_out_elastic, ease_in_out_expo, ease_in_out_quad, ease_in_out_quart, ease_in_out_quint, ease_in_out_sine, ease_in_quad, ease_in_quart, ease_in_quint, ease_in_sine, ease_out_back, ease_out_bounce, ease_out_circ, ease_out_cubic, ease_out_elastic, ease_out_expo, ease_out_quad, ease_out_quart, ease_out_quint, ease_out_sine, squish_rate_func, not_quite_there, unit_interval, zero
- `api/ready-made-scenes.md`: **Ready-made scenes**: plane, grows_vectors, add_plane, add_axes, get_vector, add_vector, write_vector_coordinates, get_basis_vectors, get_basis_vector_labels, get_vector_label, label_vector, vector_to_coords, ghost_vectors, setup, add_background_mobject, add_foreground_mobject, add_transformable_mobject, add_moving_mobject, get_ghost_vectors, get_unit_square, add_unit_square, add_transformable_label, add_title, apply_matrix, apply_inverse, apply_transposed_matrix, apply_inverse_transpose, apply_nonlinear_transformation, apply_function, activate_zooming, get_zoom_in_animation, get_zoomed_display_pop_out_animation, get_zoom_factor, ZoomedCameraConfig
- `api/rendering.md`: **Rendering**
- `api/scene.md`: **Scene**: construct, setup, tear_down, play, wait, pause, wait_until, time, add, remove, clear, replace, bring_to_front, bring_to_back, add_foreground_mobjects, remove_foreground_mobjects, mobjects, foreground_mobjects, add_updater, remove_updater, next_section, camera, frame, three_d, film, num_plays
- `api/scenes.md`: **Scenes**
- `api/shapes.md`: **Shapes**
- `api/size-and-angle.md`: **Size and angle**: width, height, scale, scale_to_fit_width, scale_to_fit_height, match_width, match_height, stretch, stretch_to_fit_width, stretch_to_fit_height, replace, m.PI, m.TAU, m.DEGREES, rotate, flip, rotation_matrix, put_start_and_end_on, apply_matrix, apply_function, apply_complex_function, set
- `api/sound.md`: **Sound**: samples, duration, run_time, gain, fade_in, fade_out, trim, loop, speed, pan, duck, of, stop
- `api/style.md`: **Style**: color, fill_color, fill_opacity, stroke_color, stroke_opacity, stroke_width, background_stroke_color, background_stroke_opacity, background_stroke_width, sheen_factor, sheen_direction, joint_type, cap_style, shade_in_3d, material, z_index, name, target, set_color, set_fill, set_stroke, set_opacity, fade, fade_to, set_style, match_style, match_color, Repaint, set_color_by_gradient, set_colors_by_radial_gradient, set_submobject_colors_by_radial_gradient, set_sheen, set_sheen_direction, CapStyleType, LineJointType, set_cap_style, set_z_index, add_background_rectangle, background_rectangle, set_default
- `api/surfaces-and-solids.md`: **Surfaces and solids**: Surface, Sphere, Torus, Cylinder, Cone, Cube, Prism, Polyhedron, Tetrahedron, Octahedron, Dodecahedron, Icosahedron, ConvexHull3D, Line3D, Arrow3D, Dot3D, MeshMobject, spherical_to_cartesian, cartesian_to_spherical
- `api/text-and-math.md`: **Text and math**
- `api/text.md`: **Text**: text, lines_text, underline, fade_all_but, default_background_config, default_paragraph_config, code_lines, line_numbers, background, CodeText, m.NORMAL, m.ITALIC, m.OBLIQUE, m.THIN, m.ULTRALIGHT, m.LIGHT, m.SEMILIGHT, m.BOOK, m.MEDIUM, m.SEMIBOLD, m.BOLD, m.ULTRABOLD, m.HEAVY, m.ULTRAHEAVY
- `api/together-and-in-turn.md`: **Together and in turn**: run_time, add_updater
- `api/transforms.md`: **Transforms**: path_arc, path_func, TransformMatchingTex, TransformMatchingShapes, Swap, CyclicReplace, TransformOptions, straight_path, path_along_arc, clockwise_path, counterclockwise_path, spiral_path, path_along_circles, Path, m.STRAIGHT_PATH_THRESHOLD
- `api/updaters.md`: **Updaters**: add_updater, remove_updater, clear_updaters, get_updaters, suspend_updating, resume_updating, update, always, flow, record, always_redraw, always_rotate, always_shift, turn_animation_into_updater, cycle_animation, UpdateFromFunc, UpdateFromAlphaFunc, MaintainPositionRelativeTo, TracedPath, AnimatedBoundary
- `api/value-trackers.md`: **Value trackers**: get_value, set_value, increment_value
- `api/vector-fields.md`: **Vector fields**: func, pos_to_color, shift_func, scale_func, fit_to_coordinate_system, nudge, nudge_submobjects, get_nudge_updater, start_submobject_movement, stop_submobject_movement, get_vector, virtual_time, stream_lines, create, start_animation, end_animation
- `api/voice.md`: **Voice**: words, Fal, Models, add_subcaption, Voice, Word, timed, estimate, cached

## Gallery (`gallery/`)

Complete code of 48 finished films. Copy patterns (3D, simulations, updaters) from here.

- `gallery/a-circle-draws-sine-and-cosine.md`: A circle draws sine and cosine
- `gallery/a-coral-of-random-walkers.md`: A coral of random walkers
- `gallery/a-galton-board.md`: A Galton board
- `gallery/a-harmonic-drive.md`: A harmonic drive
- `gallery/a-kaleidoscope-on-the-sphere.md`: A kaleidoscope on the sphere
- `gallery/a-matrix-moves-the-plane.md`: A matrix moves the plane
- `gallery/a-network-untangles-spirals.md`: A network untangles spirals
- `gallery/a-spinning-top.md`: A spinning top
- `gallery/a-torus-turned-inside-out.md`: A torus turned inside out
- `gallery/a-traffic-jam-from-nowhere.md`: A traffic jam from nowhere
- `gallery/bending-without-stretching.md`: Bending without stretching
- `gallery/cherenkov-light.md`: Cherenkov light
- `gallery/circle-or-square.md`: Circle or square?
- `gallery/circles-draw.md`: Circles draw π
- `gallery/complex-functions-bend-the-plane.md`: Complex functions bend the plane
- `gallery/crystals-and-cones.md`: Crystals and cones
- `gallery/cubes-and-the-arctic-circle.md`: Cubes and the arctic circle
- `gallery/euler-s-identity-as-a-walk.md`: Euler's identity as a walk
- `gallery/fireflies-in-sync.md`: Fireflies in sync
- `gallery/hilbert-s-space-filling-curve.md`: Hilbert's space-filling curve
- `gallery/index.md`: Gallery
- `gallery/lagrange-points.md`: Lagrange points
- `gallery/landscapes-from-formulas.md`: Landscapes from formulas
- `gallery/leapfrogging-smoke-rings.md`: Leapfrogging smoke rings
- `gallery/miura-ori.md`: Miura-ori
- `gallery/noise-into-a-word.md`: Noise into a word
- `gallery/period-doubling-in-the-mandelbrot-set.md`: Period doubling in the Mandelbrot set
- `gallery/polynomials-become-the-sine.md`: Polynomials become the sine
- `gallery/prime-spirals.md`: Prime spirals
- `gallery/prince-rupert-s-cube.md`: Prince Rupert's cube
- `gallery/pythagoras-by-rearrangement.md`: Pythagoras by rearrangement
- `gallery/quantum-tunneling.md`: Quantum tunneling
- `gallery/rectangles-become-an-integral.md`: Rectangles become an integral
- `gallery/stacking-oranges.md`: Stacking oranges
- `gallery/stars-in-the-menger-sponge.md`: Stars in the Menger sponge
- `gallery/steering-a-beam-with-phase.md`: Steering a beam with phase
- `gallery/the-game-of-life-in-spacetime.md`: The Game of Life in spacetime
- `gallery/the-hopf-fibration.md`: The Hopf fibration
- `gallery/the-lorenz-attractor.md`: The Lorenz attractor
- `gallery/the-quadratic-formula.md`: The quadratic formula
- `gallery/the-tennis-racket-flip.md`: The tennis racket flip
- `gallery/the-van-allen-belts.md`: The Van Allen belts
- `gallery/times-tables-on-a-circle.md`: Times tables on a circle
- `gallery/turing-patterns-on-a-torus.md`: Turing patterns on a torus
- `gallery/two-blocks-count.md`: Two blocks count π
- `gallery/unrolling-a-circle.md`: Unrolling a circle
- `gallery/what-a-derivative-measures.md`: What a derivative measures
- `gallery/where-z-lives.md`: Where √z lives
- `gallery/why-a-taylor-series-stops.md`: Why a Taylor series stops
