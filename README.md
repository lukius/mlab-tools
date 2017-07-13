# mlab-tools

3D animation tools for [mlab](http://docs.enthought.com/mayavi/mayavi/mlab.html). 

## Overview

This project aims at simplifying the production of geometric animations through [mlab](http://docs.enthought.com/mayavi/mayavi/mlab.html), a Python API for 3D plotting. It defines a collection of classes that wrap and extend `mlab` and [tvtk](http://docs.enthought.com/mayavi/tvtk/README.html) (traited VTK).

### Features

 * Automatic recording of AVI videos.
 * Definition of arbitrary polyhedrons through a (basic) support of [OFF (Object File Format)](https://en.wikipedia.org/wiki/OFF_(file_format)).
 * Animated polylines (i.e., continuous lines made up of linear segments) that can mimic 3D trajectories.
 * Clean interface to manipulate the animation scene in order to dynamically add or remove objects, handle the camera, etc.

## Getting started

### Prerequisites

* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [Mayavi2](http://code.enthought.com/projects/mayavi/) and its `mlab` API
* Python bindings for [OpenCV 2.4](http://opencv.org/) (only for video recording)

### Installation

You can simply clone this repository and use it locally right away.

### Examples

In the [examples](examples) folder you can find the following demos:

 * [Shrinking polyhedron](examples/shrinking_polyhedron.py), a basic animation that shrinks an OFF-based polyhedron by 20% on each frame.
 * [Animated polyhedrons](examples/animated_polyhedrons.py), another basic animation that transforms two OFF-based polyhedrons and dynamically updates some of their properties (such as their color).
 * [Polyhedron and lines](examples/polyhedron_and_random_lines.py), an animation that shows an OFF-based polyhedron rotating and randomly changing colors along with some random polylines appearing and disappearing.
 * [Primitives and points](examples/primitives_and_points.py), where some primitive shapes (namely, sphere, cube, cone and cylinder) are displayed and an animate polyline progressively joins a random set of points.
 * [Helix in detector](examples/detector_helix.py), a more complex animation that shows a small fragment of a particle detector, zooming into it to reveal a particle describing a helicoidal trajectory inside.

## License

This project is licensed under the MIT license. See the [LICENSE](LICENSE) file for further details.
