# Ultimaker Cura uses ufp file format for their printers.
# Very similar to 3mf, except it packs the actual gcode inside the archive.
# They also use 3mf, fucking hell.
# See /3D/model.gcode in reference files.
# Also has easier to parse gcode data _for some reason_.  idk.

# See ZipFile

from zipfile import ZipFile
import base64
import pprint


def confirmType(file):
    pass


def getGCode(file):
    # Here we take in the files[f] object because it's BytesIO in memory like the other stuff.
    q = ZipFile(file)
    gco = q.read("/3D/model.gcode")
    return gco


def getMaterials(file):

    q = ZipFile(file)
    filelist = q.namelist()

    # This filters us down to just files in the Materials directory luckily.
    # Should only be a few.
    filelist = [x for x in filelist if x.startswith("/Materials/")]

    # loads each material.
    filelist = [q.read(x).decode("utf-8") for x in filelist]

    # print(filelist)
    import xml.etree.ElementTree as ET

    # print(filelist)

    # We have to do this cursed shit because they use an XML variant that's BROKEN SOMEHOW!?
    for f in filelist:
        currentXML = ET.fromstring(f)
        print("/here")
        for topLevel in currentXML.getchildren():
            if "metadata" in topLevel.tag:
                for midLevel in topLevel.getchildren():
                    if "name" in midLevel.tag:
                        for finalLevel in midLevel.getchildren():
                            if "material" in finalLevel.tag.split("}")[-1]:
                                return finalLevel.text


def extractThumbnails(file):
    q = ZipFile(file)
    thumb = q.read("/Metadata/thumbnail.png")
    b64 = [base64.b64encode(thumb).decode("utf-8")]
    return b64


# /3D/model.gcode
# ;PRINT.TIME:3795
# ;EXTRUDER_TRAIN.0.MATERIAL.VOLUME_USED:3999 (volume in cubic mm: https://github.com/Ultimaker/CuraEngine/issues/482)

# /Materials/*.fdm_material (xml)
# <fdmmaterial> -> <metadata> -> <name> -> <material>
# fucking hell.
