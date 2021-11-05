#Ultimaker Cura uses ufp file format for their printers.
#Very similar to 3mf, except it packs the actual gcode inside the archive.
#They also use 3mf, fucking hell.
# See /3D/model.gcode in reference files.
#Also has easier to parse gcode data _for some reason_.  idk.

#See ZipFile

from zipfile import ZipFile
import base64

def confirmType(file):
	pass

def getGCode(file): 
	# Here we take in the files[f] object because it's BytesIO in memory like the other stuff.
	q = ZipFile(file)
	gco = (q.read("/3D/model.gcode"))
	
	
	
	
def extractThumbnails(file):
	q = ZipFile(file)
	thumb = q.read("/Metadata/thumbnail.png")
	b64 = [base64.b64encode(thumb).decode('utf-8')]
	return b64

# /3D/model.gcode
# ;PRINT.TIME:3795
# ;EXTRUDER_TRAIN.0.MATERIAL.VOLUME_USED:3999 (volume in cubic mm: https://github.com/Ultimaker/CuraEngine/issues/482)

# /Materials/*.fdm_material (xml)
# <fdmmaterial> -> <metadata> -> <name> -> <material>
#fucking hell.

