"""
Plot contour of the vorticity field at saved time steps using the
visualization software VisIt.
The PNG files are saved in the sub-folder `figures` of the simulation
directory.

CLI: visit -nowin -cli scripts/visit_plot_vorticity.py
"""

import os
import math


# Check version of VisIt.
script_version = '2.12.1'
tested_versions = [script_version]
current_version = Version()
print('VisIt version: {}\n'.format(Version()))
if current_version not in tested_versions:
    print('[warning] You are using VisIt-{}.'.format(current_version))
    print('[warning] This script was created with VisIt-{}.'
          .format(script_version))
    print('[warning] This script was tested with versions: {}.'
          .format(tested_versions))
    print('[warning] It may not work as expected')

script_dir = os.path.dirname(os.path.realpath(__file__))
simu_dir = os.path.dirname(script_dir)
filepath = os.path.join(simu_dir, 'wz.xmf')
OpenDatabase('{}:{}'.format(GetLocalHostName(), filepath), 0)

AddPlot('Contour', 'wz', 1, 1)

ContourAtts = ContourAttributes()
ContourAtts = ContourAttributes()
ContourAtts.colorType = ContourAtts.ColorByColorTable
ContourAtts.colorTableName = 'viridis'
ContourAtts.legendFlag = 0
ContourAtts.contourNLevels = 40
ContourAtts.minFlag = 1
ContourAtts.maxFlag = 1
ContourAtts.min = -20.0
ContourAtts.max = 20.0
SetPlotOptions(ContourAtts)

filepaths = os.path.join(simu_dir, 'solution', 'ellipse_*.3D')
OpenDatabase('{}:{} database'.format(GetLocalHostName(), filepaths),
             0, 'Point3D_1.0')

AddPlot('Mesh', 'points', 1, 1)

MeshAtts = MeshAttributes()
MeshAtts.legendFlag = 0
MeshAtts.pointSize = 0.05
SetPlotOptions(MeshAtts)

DrawPlots()

view = (-4.0, 3.0, -5.0, 1.0)
width, height = view[1] - view[0], view[3] - view[2]
center = (view[0] + width / 2, view[2] + height / 2, 0.0)
fig_width = 400
ratio = (width) / (height)
fig_height = int(math.floor(ratio * fig_width))

View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = center
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 90.0
zoom = 1.0 + 0.5 * height
View3DAtts.parallelScale = zoom
View3DAtts.nearPlane = -0.5
View3DAtts.farPlane = 0.5
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 0
View3DAtts.windowValid = 1
SetView3D(View3DAtts)

AnnotationAtts = AnnotationAttributes()
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
AnnotationAtts.legendInfoFlag = 0
AnnotationAtts.axesArray.visible = 0
SetAnnotationAttributes(AnnotationAtts)

time_annotation = CreateAnnotationObject('Text2D')
time_annotation.position = (0.05, 0.9)
time_annotation.fontFamily = 1
time_annotation.fontBold = 0
time_annotation.height = 0.035

states = range(1, TimeSliderGetNStates(), 1)
dt = 0.005
nsave = 100
frequency = 0.25
times = [state * nsave * dt * frequency for state in states]
fig_dir = os.path.join(simu_dir, 'figures')
if not os.path.isdir(fig_dir):
    os.makedirs(fig_dir)
prefix = 'wz'

for state, time in zip(states, times):
    SetTimeSliderState(state)
    print('\n[state {}] Create andsave field.'.format(state))
    time_annotation.text = 't/T={0:.3f}'.format(time)
    RenderingAtts = RenderingAttributes()
    SetRenderingAttributes(RenderingAtts)

    SaveWindowAtts = SaveWindowAttributes()
    SaveWindowAtts.outputToCurrentDirectory = 0
    SaveWindowAtts.outputDirectory = fig_dir
    SaveWindowAtts.fileName = '{}{:0>7}'.format(prefix, state)
    SaveWindowAtts.family = 0
    SaveWindowAtts.format = SaveWindowAtts.PNG
    SaveWindowAtts.width = fig_width
    SaveWindowAtts.height = fig_height
    SaveWindowAtts.quality = 100
    SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
    SetSaveWindowAttributes(SaveWindowAtts)

    SaveWindow()

os.remove('visitlog.py')
exit(0)
