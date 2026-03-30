from manim import * 
import numpy as np 

class SpiralSink(Scene):
    def construct(self):
        # Title screen 
        titleTex = Tex(r"A Gallery of Phase Portraits")
        titleTex.scale(1.2)
        titleTex.move_to(ORIGIN)

        definition = Tex( 
            r"A phase portrait is a visual and geometric representation of a dynamical ",
            r"system governed by differential equations. Using vector fields and solution ", 
            r"curves, it shows how a system evolves over time and reveals the qualitative ", 
            r"behavior of the system."
        )
        definition.scale(0.7)
        definition.set_width(config.frame_width - 2)
        definition.next_to(titleTex, DOWN, buff=0.6)

        transition = Tex(r"Now, let's step into the gallery...")
        transition.scale(0.8)
        transition.next_to(definition, DOWN, buff=0.7)

        self.play(FadeIn(titleTex), run_time=1.5)
        self.wait(2)

        self.play( 
            titleTex.animate.to_edge(UP).shift(DOWN * 0.4), 
            run_time=1, 
            rate_func=smooth
        )

        definition.next_to(titleTex, DOWN, buff=0.6)

        self.play(FadeIn(definition), buff=1.5)
        self.wait(3)

        transition.next_to(definition, DOWN, buff=0.7)

        self.play(FadeIn(transition), run_time=1)
        self.wait(2)

        self.play( 
            FadeOut(definition), 
            FadeOut(transition), 
            FadeOut(titleTex), 
            run_time=0.8
        )
        self.wait(0.5)

        # Create the plane 
        plane = NumberPlane(
            x_range=[-6, 6, 1], 
            y_range=[-4, 4, 1],
            background_line_style={ 
                "stroke_color": BLUE_D, 
                "stroke_width": 5, 
                "stroke_opacity": 0.8,
            }, 
            axis_config={ 
                "stroke_color": WHITE,
            },
        )
        plane.scale(1.1)
        self.play(Create(plane))

        # Define sprial matrix
        spiralMatrix = np.array([ 
            [-1, -2], 
            [ 2, -1]
        ])

        # Vector field function 
        def vectorFieldFunction(point): 
            x, y = point[0], point[1]
            dx, dy = spiralMatrix @ np.array([x, y])
            return np.array([dx, dy, 0])
        
        # Create vector field 
        field = ArrowVectorField( 
            vectorFieldFunction, 
            x_range=[-6, 6, 1], 
            y_range=[-4, 4, 1],
            length_func=lambda norm: 0.7 * np.tanh(norm)
        )
        field.set_opacity(0.85)

        for arrow in field: 
            center = arrow.get_center()
            radius = np.linalg.norm(center[:2]) / 5.5
            radius = min(radius, 1.0)
            arrow.set_color(interpolate_color(YELLOW, RED, radius))

        self.play(FadeIn(field))
        self.wait(1)

        def rk4Step(f, point, dt): 
            k1 = f(point)
            k2 = f(point + dt/2 * k1)
            k3 = f(point + dt/2 * k2)
            k4 = f(point + dt * k3) 
            return point + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
        
        def generateTrajectory(f, start, steps=300, dt=0.05): 
            points = [np.array(start, dtype=float)]
            current = np.array(start, dtype=float) 

            for _ in range(steps): 
                if np.linalg.norm(current[:2]) < 0.1: 
                    break

                if abs(current[0] > 7 or abs(current[1])) > 5: 
                    break

                current = rk4Step(f, current, dt)
                points.append(current)

            return points 
        
        initialPoints = []

        radius = 4.5
        numPoints = 10

        for i in range(numPoints): 
            angle = 2 * np.pi * i / numPoints
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            initialPoints.append(np.array([x, y, 0]))

        trajectories = VGroup()
        for p in initialPoints: 
            forwardPoints = generateTrajectory(vectorFieldFunction, p, steps=300, dt=0.05)
            backwardsPoints = generateTrajectory(vectorFieldFunction, p, steps=300, dt=-0.05)

            fullTrajectory = backwardsPoints[::-1] + forwardPoints[1:]

            curve = VMobject()
            curve.set_points_smoothly(fullTrajectory)
            curve.set_stroke(width=2)
            curve.set_stroke(color=LIGHT_PINK, width=2)

            trajectories.add(curve)
        
        self.play(Create(trajectories), run_time=3)
        self.wait(1)

        # Create solution text for spiral
        solutionTex = MathTex( 
            r"\vec{x}(t)=e^{-t}", 
            r"\begin{bmatrix}", 
            r"c_1\cos(2t)-c_2\sin(2t)", 
            r"\\", 
            r"c_1\sin(2t)+c_2\cos(2t)"
            r"\end{bmatrix}"
        )
        solutionTex.scale(0.7)
        solutionBox = SurroundingRectangle( 
            solutionTex, 
            buff=0.3, 
            color=WHITE, 
            stroke_width=2
        )
        solutionBox.set_fill(BLACK, opacity=0.7)

        solutionGroup = VGroup(solutionBox, solutionTex)
        solutionGroup.to_edge(UP)
        solutionGroup.shift(DOWN * 0.5)

        # Prepare for transition to center
        self.play(FadeIn(solutionGroup), run_time=1)
        self.wait(4)
        self.play(FadeOut(solutionGroup), run_time=1)
        self.wait(0.5)

        self.play(FadeOut(trajectories), run_time=1)

        # Center Matrix
        centerMatrix = np.array([ 
            [0, -2], 
            [2, 0]
        ])

        # Center Vector field
        def centerVectorFieldFunction(point): 
            x, y = point[0], point[1]
            dx, dy = centerMatrix @ np.array([x, y])
            return np.array([dx, dy, 0], dtype=float)
        
        centerField = ArrowVectorField( 
            centerVectorFieldFunction, 
            x_range=[-6, 6, 1], 
            y_range=[-4, 4, 1], 
            length_func=lambda norm: 0.7 * np.tanh(norm)
        )
        centerField.set_opacity(0.85)

        for arrow in centerField: 
            center = arrow.get_center()
            radius = np.linalg.norm(center[:2]) / 5.5
            radius = min(radius, 1.0)
            arrow.set_color(interpolate_color(YELLOW, RED, radius))

        self.play(ReplacementTransform(field, centerField), run_time=2.5)
        self.wait(1)

        centerInitialPoints = [ 
            np.array([0.8, 0, 0], dtype=float), 
            np.array([1.2, 0, 0], dtype=float), 
            np.array([1.6, 0, 0], dtype=float), 
            np.array([2.0, 0, 0], dtype=float), 
            np.array([2.4, 0, 0], dtype=float),
            np.array([2.8, 0, 0], dtype=float),
            np.array([3.2, 0, 0], dtype=float),
            np.array([3.6, 0, 0], dtype=float),
            np.array([4.0, 0, 0], dtype=float),
            np.array([4.4, 0, 0], dtype=float),
            np.array([4.8, 0, 0], dtype=float),
        ]

        centerTrajectories = VGroup()

        dt = 0.01 
        period = np.pi 
        steps = int(period/ dt) 

        for i,  p in enumerate(centerInitialPoints): 
            trajPoints = generateTrajectory( 
                centerVectorFieldFunction, 
                p, 
                steps=steps, 
                dt=dt
            )

            trajPoints.append(trajPoints[0])

            curve = VMobject()
            curve.set_points_smoothly(trajPoints)
            opacity = 0.7 + 0.3 * (i / (len(centerInitialPoints) - 1))
            curve.set_stroke(color=LIGHT_PINK, width=2.5, opacity=opacity)

            centerTrajectories.add(curve)

        self.play(
            LaggedStart(*[Create(curve) for curve in centerTrajectories], lag_ratio=0.12),
            run_time=4
        )
        self.wait(1)

        centerSolutionTex = MathTex( 
            r"\vec{x}(t)=", 
            r"\begin{bmatrix}", 
            r"c_1\cos(2t)-c_2\sin(2t)", 
            r"\\", 
            r"c_1\sin(2t)+c_2\cos(2t)", 
            r"\end{bmatrix}"
        )
        centerSolutionTex.scale(0.7)

        centerSolutionBox = SurroundingRectangle( 
            centerSolutionTex, 
            buff=0.3, 
            color=WHITE, 
            stroke_width=2
        )
        centerSolutionBox.set_fill(BLACK, opacity=0.7)

        centerSolutionGroup = VGroup(centerSolutionBox, centerSolutionTex)
        centerSolutionGroup.to_edge(UP)
        centerSolutionGroup.shift(DOWN * 0.5)

        self.play(FadeIn(centerSolutionGroup), run_time=1)
        self.wait(4)
        self.play(FadeOut(centerSolutionGroup), run_time=1)

        self.wait(1)

        self.play(FadeOut(centerTrajectories), run_time=2)
        self.wait(0.5)

        saddleMatrix = np.array([ 
            [1, 0], 
            [0, -1]
        ])

        alpha = ValueTracker(0)

        def transitionFieldFunction(point): 
            x, y = point[0], point[1] 

            currentMatrix = ( 
                (1 - alpha.get_value()) * centerMatrix 
                + alpha.get_value() * saddleMatrix
            )

            dx, dy = currentMatrix @ np.array([x, y])
            return np.array([dx, dy, 0], dtype=float)

        def coloredField(): 
            field = ArrowVectorField( 
                transitionFieldFunction, 
                x_range=[-6, 6, 1], 
                y_range=[-4, 4, 1],
                length_func=lambda norm: 0.7 * np.tanh(norm)
            )
            field.set_opacity(0.85)

            for arrow in field: 
                center = arrow.get_center()
                radius = np.clip(np.linalg.norm(center[:2]) / 5.5, 0, 1)
                arrow.set_color(interpolate_color(YELLOW, RED, radius))

            return field 
        
        transitionField = always_redraw(coloredField)

        self.play( 
            FadeOut(centerField), 
            FadeIn(transitionField), 
            run_time=1
        )

        self.play(
            alpha.animate.set_value(1),
            run_time=4,
            rate_func=smooth
        )

        self.wait(1)

        def saddleVectorFieldFunction(point): 
            x, y = point[0], point[1]
            dx, dy = saddleMatrix @ np.array([x, y])
            return np.array([dx, dy, 0], dtype=float)
        
        def generateBoundedTrajectory(f, start, steps=250, dt=0.03, xBound=7.5, yBound=5.5): 
            points = [np.array(start, dtype=float)]
            current = np.array(start, dtype=float)

            for _ in range(steps):
                current = rk4Step(f, current, dt)

                if abs(current[0]) > xBound or abs(current[1]) > yBound:
                    break

                points.append(current)

            return points
        
        saddleInitialPoints = [
            np.array([ 0.6,  0.2, 0], dtype=float),
            np.array([ 0.6, -0.2, 0], dtype=float),
            np.array([-0.6,  0.2, 0], dtype=float),
            np.array([-0.6, -0.2, 0], dtype=float),

            np.array([ 0.9,  0.35, 0], dtype=float),
            np.array([ 0.9, -0.35, 0], dtype=float),
            np.array([-0.9,  0.35, 0], dtype=float),
            np.array([-0.9, -0.35, 0], dtype=float),

            np.array([ 1.2,  0.55, 0], dtype=float),
            np.array([ 1.2, -0.55, 0], dtype=float),
            np.array([-1.2,  0.55, 0], dtype=float),
            np.array([-1.2, -0.55, 0], dtype=float),

            np.array([ 1.8,  0.9, 0], dtype=float),
            np.array([ 1.8, -0.9, 0], dtype=float),
            np.array([-1.8,  0.9, 0], dtype=float),
            np.array([-1.8, -0.9, 0], dtype=float),
        ]

        saddleTrajectories = VGroup()

        for p in saddleInitialPoints:
            if abs(p[1]) < 0.25: 
                continue 
            if abs(p[0]) < 0.25: 
                continue 

            forwardPoints = generateBoundedTrajectory(
                saddleVectorFieldFunction,
                p,
                steps=250,
                dt=0.03,
                xBound=7.5,
                yBound=5.5
            )

            backwardPoints = generateBoundedTrajectory(
                saddleVectorFieldFunction,
                p,
                steps=250,
                dt=-0.03,
                xBound=7.5,
                yBound=5.5
            )

            fullTrajectory = backwardPoints[::-1] + forwardPoints[1:]

            if len(fullTrajectory) < 2:
                continue

            curve = VMobject()
            curve.set_points_smoothly(fullTrajectory)
            opacity = 0.6 + 0.4 * (i / (len(saddleInitialPoints) - 1))
            curve.set_stroke(color=LIGHT_PINK, width=2.5, opacity=opacity)

            saddleTrajectories.add(curve)

        xAxisLine = Line(
            start=np.array([-7, 0, 0], dtype=float),
            end=np.array([7, 0, 0], dtype=float)
        )
        xAxisLine.set_stroke(color=LIGHT_PINK, width=2.5, opacity=0.8)

        yAxisLine = Line(
            start=np.array([0, -5.5, 0], dtype=float),
            end=np.array([0, 5.5, 0], dtype=float)
        )
        yAxisLine.set_stroke(color=LIGHT_PINK, width=2.5, opacity=0.8)

        self.play(
            LaggedStart(*[Create(curve) for curve in saddleTrajectories], lag_ratio=0.08),
            run_time=4
        )

        self.play( 
            Create(xAxisLine), 
            Create(yAxisLine), 
            run_time=2
        )
        self.wait(1)

        saddleSolutionTex = MathTex( 
            r"\vec{x}(t)=", 
            r"\begin{bmatrix}", 
            r"c_1 e^t", 
            r"\\", 
            r"c_2 e^{-t}", 
            r"\end{bmatrix}"
        )
        saddleSolutionTex.scale(0.7)

        saddleBackgroundBox = SurroundingRectangle(
            saddleSolutionTex, 
            buff=0.3, 
            color=WHITE, 
            stroke_width=2
        )
        saddleBackgroundBox.set_fill(BLACK, opacity=0.7)

        saddleSolutionGroup = VGroup(saddleBackgroundBox, saddleSolutionTex)
        saddleSolutionGroup.to_edge(UP)
        saddleSolutionGroup.shift(DOWN * 0.5)

        self.play(FadeIn(saddleSolutionGroup), run_time=1)
        self.wait(4)
        self.play(FadeOut(saddleSolutionGroup), run_time=1)

        self.play(FadeOut(saddleTrajectories), FadeOut(xAxisLine), FadeOut(yAxisLine), run_time=2)
        self.wait(0.5)

        defectiveMatrix = np.array([ 
            [-1, 1], 
            [0, -1]
        ])

        beta = ValueTracker(0)

        def defectiveTransitionFieldFunction(point): 
            x, y = point[0], point[1]

            currentMatrix = ( 
                (1 - beta.get_value()) * saddleMatrix
                + beta.get_value() * defectiveMatrix
            )

            dx, dy = currentMatrix @ np.array([x, y])
            return np.array([dx, dy, 0], dtype=float)
        
        def defectiveColoredField(): 
            field = ArrowVectorField( 
                defectiveTransitionFieldFunction, 
                x_range=[-6, 6, 1],
                y_range=[-4, 4, 1], 
                length_func=lambda norm: 0.7 * np.tanh(norm) 
            )
            field.set_opacity(0.85)

            for arrow in field: 
                center = arrow.get_center()
                radius = np.clip(np.linalg.norm(center[:2]) / 5.5, 0, 1)
                arrow.set_color(interpolate_color(YELLOW, RED, radius))

            return field 
        
        defectiveTransitionField = always_redraw(defectiveColoredField)

        self.play(
            FadeOut(transitionField),
            FadeIn(defectiveTransitionField),
            run_time=1
        )

        self.play(
            beta.animate.set_value(1),
            run_time=4,
            rate_func=smooth
        )
        
        def defectiveVectorFieldFunction(point): 
            x, y = point[0], point[1]
            dx, dy = defectiveMatrix @ np.array([x, y])
            return np.array([dx, dy, 0], dtype=float)
        
        def generateBoundedDefectiveTrajectory(f, start, steps=500, dt=0.025, xBound=7.5, yBound=5.5): 
                points = [np.array(start, dtype=float)]
                current = np.array(start, dtype=float)

                for _ in range(steps):
                    current = rk4Step(f, current, dt)

                    if abs(current[0]) > xBound or abs(current[1]) > yBound:
                        break

                    points.append(current)

                return points
        
        defectiveInitialPoints = [
            np.array([-5.5,  2.5, 0], dtype=float),
            np.array([-4.0,  2.0, 0], dtype=float),
            np.array([-3.0,  1.2, 0], dtype=float),
            np.array([-2.0,  0.6, 0], dtype=float),

            np.array([-5.5, -2.5, 0], dtype=float),
            np.array([-4.0, -2.0, 0], dtype=float),
            np.array([-3.0, -1.2, 0], dtype=float),
            np.array([-2.0, -0.6, 0], dtype=float),

            np.array([ 4.0,  2.5, 0], dtype=float),
            np.array([ 3.0,  1.5, 0], dtype=float),
            np.array([ 4.0, -2.5, 0], dtype=float),
            np.array([ 3.0, -1.5, 0], dtype=float),

            np.array([-5.5,  1.0, 0], dtype=float),
            np.array([-5.5, -1.0, 0], dtype=float),

            np.array([ 2.5,  2.5, 0], dtype=float),
            np.array([ 2.5, -2.5, 0], dtype=float),

            np.array([-5.5,  1.0, 0], dtype=float),
            np.array([5.5, -1.0, 0], dtype=float),

            np.array([ 3.5,  2.2, 0], dtype=float),
            np.array([ 3.5, -2.2, 0], dtype=float),
        ]

        defectiveTrajectories = VGroup() 

        for p in defectiveInitialPoints:
            forwardPoints = generateBoundedDefectiveTrajectory(
                defectiveVectorFieldFunction,
                p,
                steps=500,
                dt=0.025,
                xBound=7.5,
                yBound=5.5
            )

            backwardPoints = generateBoundedDefectiveTrajectory(
                defectiveVectorFieldFunction,
                p,
                steps=500,
                dt=-0.025,
                xBound=7.5,
                yBound=5.5
            )

            fullTrajectory = backwardPoints[::-1] + forwardPoints[1:]

            if len(fullTrajectory) < 2:
                continue

            curve = VMobject()
            curve.set_points_smoothly(fullTrajectory)
            curve.set_stroke(color=LIGHT_PINK, width=2.5)

            defectiveTrajectories.add(curve)

        self.play( 
            LaggedStart(*[Create(curve) for curve in defectiveTrajectories], lag_ratio=0.12), 
            run_time=4
        )
        self.wait(1)

        defectiveSolutionTex = MathTex( 
            r"\vec{x}(t)=", 
            r"e^{t}",
            r"\begin{bmatrix}", 
            r"c_1 + c_2 t",
            r"\\",
            r"c_2", 
            r"\end{bmatrix}"
        )
        defectiveSolutionTex.scale(0.7)
        
        defectiveSolutionBox = SurroundingRectangle( 
            defectiveSolutionTex, 
            buff=0.3, 
            color=WHITE, 
            stroke_width=2
        )
        defectiveSolutionBox.set_fill(BLACK, opacity=0.7) 

        defectiveSolutionGroup = VGroup(defectiveSolutionBox, defectiveSolutionTex) 
        defectiveSolutionGroup.to_edge(UP) 
        defectiveSolutionGroup.shift(DOWN * 0.5) 

        self.play(FadeIn(defectiveSolutionGroup), run_time=1)
        self.wait(4)
        self.play(FadeOut(defectiveSolutionGroup), run_time=1)

        self.play(FadeOut(defectiveTrajectories), run_time=2)
        
        self.wait(1)

        rotatedDefectiveMatrix = np.array([ 
            [2, 1], 
            [-1, 4]
        ])

        gamma = ValueTracker(0)

        def rotatedTransitionFieldFunction(point):
            x, y = point[0], point[1]

            currentMatrix = (
                (1 - gamma.get_value()) * defectiveMatrix
                + gamma.get_value() * rotatedDefectiveMatrix
            )

            dx, dy = currentMatrix @ np.array([x, y])
            return np.array([dx, dy, 0], dtype=float)
        
        def rotatedColoredField():
            field = ArrowVectorField(
                rotatedTransitionFieldFunction,
                x_range=[-6, 6, 1],
                y_range=[-4, 4, 1],
                length_func=lambda norm: 0.7 * np.tanh(norm)
            )
            field.set_opacity(0.85)

            for arrow in field:
                center = arrow.get_center()
                radius = np.clip(np.linalg.norm(center[:2]) / 5.5, 0, 1)
                arrow.set_color(interpolate_color(YELLOW, RED, radius))

            return field
        
        rotatedTransitionField = always_redraw(rotatedColoredField) 

        self.play(
            FadeOut(defectiveTransitionField),
            FadeIn(rotatedTransitionField),  
            run_time=1
        )

        self.play(
            gamma.animate.set_value(1),
            run_time=4,
            rate_func=smooth
        )

        self.wait(2)

        def rotatedDefectiveVectorFieldFunction(point):
            x, y = point[0], point[1]
            dx, dy = rotatedDefectiveMatrix @ np.array([x, y])
            return np.array([dx, dy, 0], dtype=float)
        
        def generateRotatedDefectiveTrajectory(f, start, steps=800, dt=0.01, xBound=7.5, yBound=5.5):
            points = [np.array(start, dtype=float)]
            current = np.array(start, dtype=float)

            for _ in range(steps):
                current = rk4Step(f, current, dt)

                if abs(current[0]) > xBound or abs(current[1]) > yBound:
                    break

                points.append(current)

            return points
        
        rotatedDefectiveInitialPoints = [
            np.array([-1.4,  0.8, 0], dtype=float),
            np.array([-1.0,  0.5, 0], dtype=float),
            np.array([-0.7,  0.2, 0], dtype=float),

            np.array([-1.4, -0.8, 0], dtype=float),
            np.array([-1.0, -0.5, 0], dtype=float),
            np.array([-0.7, -0.2, 0], dtype=float),

            np.array([ 0.5,  0.9, 0], dtype=float),
            np.array([ 0.8,  0.4, 0], dtype=float),

            np.array([ 0.5, -0.9, 0], dtype=float),
            np.array([ 0.8, -0.4, 0], dtype=float),

            np.array([-2.5,  1.5, 0], dtype=float),
            np.array([-2.5, -1.5, 0], dtype=float),

            np.array([-3.5,  0.8, 0], dtype=float),
            np.array([-3.5, -0.8, 0], dtype=float),

            np.array([ 1.5,  1.8, 0], dtype=float),
            np.array([ 1.5, -1.8, 0], dtype=float),

            np.array([2.5,  1.2, 0], dtype=float),
            np.array([2.5, -1.2, 0], dtype=float),

            np.array([3.5,  0.5, 0], dtype=float),
        ]

        rotatedDefectiveTrajectories = VGroup()

        for p in rotatedDefectiveInitialPoints:

            forwardPoints = generateRotatedDefectiveTrajectory(
                rotatedDefectiveVectorFieldFunction,
                p,
                steps=800,
                dt=0.01,
                xBound=7.5,
                yBound=5.5
            )

            backwardPoints = generateRotatedDefectiveTrajectory(
                rotatedDefectiveVectorFieldFunction,
                p,
                steps=800,
                dt=-0.01,
                xBound=7.5,
                yBound=5.5
            )

            fullTrajectory = backwardPoints[::-1] + forwardPoints[1:]

            if len(fullTrajectory) < 5:
                continue

            curve = VMobject()
            curve.set_points_smoothly(fullTrajectory)
            curve.set_stroke(color=LIGHT_PINK, width=2.5)

            rotatedDefectiveTrajectories.add(curve)
            
        self.play(
            LaggedStart(*[Create(curve) for curve in rotatedDefectiveTrajectories], lag_ratio=0.12),
            run_time=4
        )
        self.wait(1)

        rotatedDefectiveSolutionTex = MathTex( 
            r"\vec{x}(t)=", 
            r"e^{3t}", 
            r"\begin{bmatrix}", 
            r"c_1 \cos(t) + c_2 \sin(t)", 
            r"\\", 
            r"-c_1 \sin(t) + c_2 \cos(t)", 
            r"\end{bmatrix}"
        )

        rotatedDefectiveSolutionBox = SurroundingRectangle( 
            rotatedDefectiveSolutionTex, 
            buff=0.3, 
            color=WHITE, 
            stroke_width=2
        )
        rotatedDefectiveSolutionBox.set_fill(BLACK, opacity=0.7) 

        rotatedDefectiveSolutionGroup = VGroup(rotatedDefectiveSolutionBox, rotatedDefectiveSolutionTex) 
        rotatedDefectiveSolutionGroup.to_edge(UP) 
        rotatedDefectiveSolutionGroup.shift(DOWN * 0.5)

        self.play(FadeIn(rotatedDefectiveSolutionGroup), run_time=1) 
        self.wait(4)
        self.play(FadeOut(rotatedDefectiveSolutionGroup), run_time=1)

        self.wait(0.5)

        self.play(FadeOut(rotatedDefectiveTrajectories), run_time=2)
        self.wait(1)

        pendulumEpsilon = ValueTracker(0)

        def pendulumTransitionFieldFunction(point):
            x, y = point[0], point[1]

            linearDx, linearDy = rotatedDefectiveMatrix @ np.array([x, y], dtype=float)

            damping = 0.35
            nonlinearDx = y
            nonlinearDy = -np.sin(x) - damping * y

            dx = (1 - pendulumEpsilon.get_value()) * linearDx + pendulumEpsilon.get_value() * nonlinearDx
            dy = (1 - pendulumEpsilon.get_value()) * linearDy + pendulumEpsilon.get_value() * nonlinearDy

            return np.array([dx, dy, 0], dtype=float)

        def pendulumColoredField():
            field = ArrowVectorField(
                pendulumTransitionFieldFunction,
                x_range=[-6, 6, 1],
                y_range=[-4, 4, 1],
                length_func=lambda norm: 0.7 * np.tanh(norm)
            )
            field.set_opacity(0.85)

            for arrow in field:
                center = arrow.get_center()
                radius = np.clip(np.linalg.norm(center[:2]) / 5.5, 0, 1)
                arrow.set_color(interpolate_color(YELLOW, RED, radius))

            return field

        pendulumTransitionField = always_redraw(pendulumColoredField)

        self.play(
            FadeOut(rotatedTransitionField),
            FadeIn(pendulumTransitionField),
            run_time=1
        )

        self.play(
            pendulumEpsilon.animate.set_value(1),
            run_time=4,
            rate_func=smooth
        )

        self.wait(1)

        pendulumPlane = NumberPlane( 
            x_range=[-2 * np.pi, 2 * np.pi, np.pi / 2],
            y_range=[-5, 5, 1],
            x_length=14,
            y_length=8,
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 2,
                "stroke_opacity": 0.8,
            },
            axis_config={
                "stroke_color": WHITE,
                "stroke_width": 2,
            },
        )

        self.play( 
            ReplacementTransform(plane, pendulumPlane), 
            run_time=1.5
        )

        def pendulumFieldFunction(point): 
            x, y = point[0], point[1]

            damping = 0.35
            dx = y 
            dy = -np.sin(x) - damping * y

            return np.array([dx, dy, 0], dtype=float)
        
        def finalPendulumColoredField():
            field = ArrowVectorField(
                pendulumFieldFunction,
                x_range=[-2 * np.pi, 2 * np.pi, np.pi / 2],
                y_range=[-5, 5, 1],
                length_func=lambda norm: 0.95 * np.tanh(norm)
            )
            field.set_opacity(0.85)

            for arrow in field: 
                center = arrow.get_center()
                x, y = center[0], center[1]

                energy = 0.5 * y**2 + 1 - np.cos(x)
                separatrixDistance = abs(energy - 2.0)

                t = np.clip(separatrixDistance / 2.5, 0, 1)
                arrow.set_color(interpolate_color(YELLOW, RED, t))

            return field 
        

        finalPendulumField = finalPendulumColoredField()

        self.play(
            FadeOut(pendulumTransitionField),
            FadeIn(finalPendulumField),
            run_time=1
        )

        self.wait(1)

        def generateBoundedPendulumTrajectory(f, start, steps=2500, dt=0.01, xBound=2 * np.pi + 1, yBound=6):
            points = [np.array(start, dtype=float).reshape(3,)]
            current = np.array(start, dtype=float).reshape(3,)

            for _ in range(steps):
                current = np.array(rk4Step(f, current, dt), dtype=float).reshape(3,)

                if abs(current[0]) > xBound or abs(current[1]) > yBound:
                    break

                points.append(current)

            return points
        
        pendulumLoopSeeds = [
            np.array([ 0.4,  0.0, 0], dtype=float),
            np.array([ 1.0,  0.0, 0], dtype=float),
            np.array([-1.0,  0.0, 0], dtype=float),

            np.array([ 2 * np.pi - 0.4,  0.0, 0], dtype=float),
            np.array([ 2 * np.pi - 0.9,  0.0, 0], dtype=float),

            np.array([-2 * np.pi + 0.4,  0.0, 0], dtype=float),
            np.array([-2 * np.pi + 0.9,  0.0, 0], dtype=float),

            np.array([ 2 * np.pi - 0.6,  0.6, 0], dtype=float),
            np.array([-2 * np.pi + 0.6, -0.6, 0], dtype=float),
        ]

        pendulumSeparatrixSeeds = [
            np.array([ np.pi - 0.2,  0.0, 0], dtype=float),
            np.array([-np.pi + 0.2,  0.0, 0], dtype=float),
            np.array([ np.pi - 0.2,  0.6, 0], dtype=float),
            np.array([-np.pi + 0.2, -0.6, 0], dtype=float),
            np.array([ np.pi - 0.35,  0.9, 0], dtype=float),
            np.array([-np.pi + 0.35, -0.9, 0], dtype=float),
        ]

        pendulumRotationSeeds = [
            np.array([ 0.0,  2.6, 0], dtype=float),
            np.array([ 1.5,  2.8, 0], dtype=float),
            np.array([-1.5, -2.8, 0], dtype=float),
            np.array([ 0.0, -2.6, 0], dtype=float),
            
            np.array([ 2.5,  2.6, 0], dtype=float),
            np.array([-2.5,  2.6, 0], dtype=float),
            np.array([ 2.5, -2.6, 0], dtype=float),
            np.array([-2.5, -2.6, 0], dtype=float),

            np.array([ 3.6,  2.8, 0], dtype=float),
            np.array([-3.6,  2.8, 0], dtype=float),
            np.array([ 3.6, -2.8, 0], dtype=float),
            np.array([-3.6, -2.8, 0], dtype=float),

            np.array([ 5.0,  2.4, 0], dtype=float),
            np.array([-5.0,  2.4, 0], dtype=float),
            np.array([ 5.0, -2.4, 0], dtype=float),
            np.array([-5.0, -2.4, 0], dtype=float),

            np.array([ 4.0,  2.2, 0], dtype=float),
            np.array([-4.0,  2.2, 0], dtype=float),
            np.array([ 4.0, -2.2, 0], dtype=float),
            np.array([-4.0, -2.2, 0], dtype=float),
        ]

        highlightSeed = np.array([0.0, 2.6, 0], dtype=float)
        leftHighlightSeed = np.array([-2 * np.pi + 0.6, -0.6, 0], dtype=float)
        rightHighlightSeed = np.array([2 * np.pi - 0.6, 0.6, 0], dtype=float)

        pendulumTrajectories = VGroup()

        allPendulumSeeds = pendulumLoopSeeds + pendulumSeparatrixSeeds + pendulumRotationSeeds

        for p in allPendulumSeeds:
            forwardPoints = generateBoundedPendulumTrajectory(
                pendulumFieldFunction,
                p,
                steps=2500,
                dt=0.01,
                xBound=2 * np.pi + 1,
                yBound=6
            )

            backwardPoints = generateBoundedPendulumTrajectory(
                pendulumFieldFunction,
                p,
                steps=2500,
                dt=-0.01,
                xBound=2 * np.pi + 1,
                yBound=6
            )

            fullTrajectory = backwardPoints[::-1] + forwardPoints[1:]

            if len(fullTrajectory) < 8:
                continue

            cleanTrajectory = []
            for pt in fullTrajectory:
                pt = np.array(pt, dtype=float).flatten()

                if pt.shape[0] == 2:
                    pt = np.array([pt[0], pt[1], 0.0], dtype=float)
                elif pt.shape[0] != 3:
                    continue

                cleanTrajectory.append(pt)

            if len(cleanTrajectory) < 3:
                continue

            curve = VMobject()
            curve.set_points_smoothly(cleanTrajectory)
            curve.set_stroke(color=LIGHT_PINK, width=2.5)

            pendulumTrajectories.add(curve)

        def buildHighlightedPendulumCurve(seed, color, width=4):
            forwardPoints = generateBoundedPendulumTrajectory(
                pendulumFieldFunction,
                seed,
                steps=2500,
                dt=0.01,
                xBound=2 * np.pi + 1,
                yBound=6
            )

            backwardPoints = generateBoundedPendulumTrajectory(
                pendulumFieldFunction,
                seed,
                steps=2500,
                dt=-0.01,
                xBound=2 * np.pi + 1,
                yBound=6
            )

            fullTrajectory = backwardPoints[::-1] + forwardPoints[1:]

            cleanTrajectory = []
            for pt in fullTrajectory:
                pt = np.array(pt, dtype=float).flatten()

                if pt.shape[0] == 2:
                    pt = np.array([pt[0], pt[1], 0.0], dtype=float)
                elif pt.shape[0] != 3:
                    continue

                cleanTrajectory.append(pt)

            curve = VMobject()
            curve.set_points_smoothly(cleanTrajectory)
            curve.set_stroke(color=color, width=width)

            return curve
        
        centerHighlightCurve = buildHighlightedPendulumCurve(highlightSeed, WHITE, width=5)
        leftHighlightCurve = buildHighlightedPendulumCurve(leftHighlightSeed, BLUE_C, width=5)
        rightHighlightCurve = buildHighlightedPendulumCurve(rightHighlightSeed, TEAL_C, width=5)

        if len(pendulumTrajectories) > 0:
            self.play(
                LaggedStart(*[Create(curve) for curve in pendulumTrajectories], lag_ratio=0.08),
                run_time=6
            )

        self.wait(1)

        self.play(Create(centerHighlightCurve), run_time=2)
        self.wait(0.5)

        self.play(
            Create(leftHighlightCurve),
            Create(rightHighlightCurve),
            run_time=2
        )

        self.wait(1)

        pendulumEquationTex = MathTex( 
            r"\ddot{\theta} + c\dot{\theta} + \frac{g}{L}\sin(\theta)=0"
        )
        pendulumEquationTex.scale(0.9)

        pendulumEquationBox = SurroundingRectangle( 
            pendulumEquationTex, 
            buff=0.3, 
            color=WHITE, 
            stroke_width=2
        )
        pendulumEquationBox.set_fill(BLACK, opacity=0.7)

        pendulumEquationGroup = VGroup( 
            pendulumEquationBox, 
            pendulumEquationTex
        )
        pendulumEquationGroup.to_edge(UP)
        pendulumEquationGroup.shift(DOWN * 0.4)

        pendulumParameterTex = MathTex( 
            r"c > 0: \ \text{damping}, \quad \frac{g}{L}: \ \text{gravitational strength}"
        )
        pendulumParameterTex.scale(0.8)

        pendulumParameterBox = SurroundingRectangle( 
            pendulumParameterTex, 
            buff=0.3, 
            color=WHITE, 
            stroke_width=2
        )
        pendulumParameterBox.set_fill(BLACK, opacity=0.7)

        pendulumParameterGroup = VGroup( 
            pendulumParameterBox, 
            pendulumParameterTex
        )
        pendulumParameterGroup.to_edge(DOWN)
        pendulumParameterGroup.shift(UP * 0.45)

        self.play( 
            FadeIn(pendulumEquationGroup), 
            FadeIn(pendulumParameterGroup), 
            run_time=1
        )
        self.wait(4)
        self.play( 
            FadeOut(pendulumEquationGroup), 
            FadeOut(pendulumParameterGroup), 
            run_time=1 
        )
        self.wait(2)