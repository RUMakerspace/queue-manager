#Ultimaker Cura uses ufp file format for their printers.
#Very similar to 3mf, except it packs the actual gcode inside the archive.
#They also use 3mf, fucking hell.
# See /3D/model.gcode in reference files.
#Also has easier to parse gcode data _for some reason_.  idk.

#See ZipFile

def confirmType(file)
	pass


# /3D/model.gcode
# ;PRINT.TIME:3795
# ;EXTRUDER_TRAIN.0.MATERIAL.VOLUME_USED:3999 (volume in cubic mm: https://github.com/Ultimaker/CuraEngine/issues/482)

# /Materials/*.fdm_material (xml)
# <fdmmaterial> -> <metadata> -> <name> -> <material>
#fucking hell.

