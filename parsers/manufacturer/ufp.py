# Ultimaker Cura uses ufp file format for their printers.
# Very similar to 3mf, except it packs the actual gcode inside the archive.
# They also use 3mf, fucking hell.
# See /3D/model.gcode in reference files.
# Also has easier to parse gcode data _for some reason_.  idk.

# See ZipFile

from zipfile import ZipFile
import base64
import pprint


def getGCode(file):
    # Here we take in the files[f] object because it's BytesIO in memory like the other stuff.
    q = ZipFile(file)
    gco = q.read("/3D/model.gcode").decode("utf-8")

    gco = gco.split("\n")

    return gco


def getUFPProperties(file):
    GCodeData = getGCodeMetadata(file)
    materialsData = getMaterials(file)

    output = {}

    for k in GCodeData.keys():
        output[k] = GCodeData[k]

    for k in materialsData.keys():
        output[k] = materialsData[k]

    # This only works IIF the subsidiary functions work.  Normalize output between UFP and Prusa GCode?
    output["materialUsedGrams"] = (output["volumeUsed"] / 10 ** 3) * output["density"]

    return output


def getGCodeMetadata(file):
    lines = getGCode(file)

    lines = [x for x in lines if x.startswith(";")]

    outputMeta = {}

    for l in lines:
        if "EXTRUDER_TRAIN.0.MATERIAL.VOLUME_USED" in l:
            outputMeta["volumeUsed"] = int(
                l.split(":")[-1]
            )  # this is measured in g/cm^3 as opposed to mm^3.  Conversion factor is 10E3.

        if "PRINT.TIME" in l:
            outputMeta["printTimeSeconds"] = int(l.split(":")[-1])

    return outputMeta


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

    materialProp = {}
    # We have to do this cursed shit because they use an XML variant that's BROKEN SOMEHOW!?
    for f in filelist:
        currentXML = ET.fromstring(f)
        # print("/here")
        for topLevel in currentXML.getchildren():
            if "metadata" in topLevel.tag:
                for midLevel in topLevel.getchildren():
                    if "name" in midLevel.tag:
                        for finalLevel in midLevel.getchildren():
                            if "material" in finalLevel.tag.split("}")[-1]:
                                materialProp["material"] = finalLevel.text

            if "properties" in topLevel.tag:
                for midLevel in topLevel.getchildren():
                    if "density" in midLevel.tag.split("}")[-1]:
                        materialProp["density"] = float(midLevel.text)
                    if "diameter" in midLevel.tag.split("}")[-1]:
                        materialProp["diameter"] = float(midLevel.text)

    return materialProp


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
