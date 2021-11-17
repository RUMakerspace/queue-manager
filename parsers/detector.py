from parsers.manufacturer.gcode import (
    extractPrusaGCodeInfo,
    extractPrusaThumbnails,
    detectGCodeType,
)
from parsers.manufacturer.ufp import getGCode, extractThumbnails, getUFPProperties


def detectFile(fileList, formDict):
    print(formDict)
    for f in fileList:
        if fileList[f].filename.endswith(".ufp"):
            fileData = fileList[f]

            getGCode(fileData)
            print("Ultimaker Cura UFP")

            thumbs = extractThumbnails(fileList[f])
            print(getUFPProperties(fileList[f]))

        if fileList[f].mimetype in [
            "text/x.gcode",
            "text/x-gcode",
        ]:  # mimetypes for prusa gcode I think. https://mimetype.io/gcode
            # We extract the file here to avoid issues wrt stream decoding.  May be an issue for very big files.  _okay_ for now.
            fileData = fileList[f].read().decode("utf-8")
            # print(fileData)

            gcodeflavor = detectGCodeType(fileData.split("\n"))

            if gcodeflavor == "PRUSASLICER":
                print(
                    extractPrusaGCodeInfo(
                        filename=fileList[f].filename, fileData=fileData
                    )
                )
                # thumbs = extractPrusaThumbnails(fileData)
                # return render_template("imgs.html", thumbs=thumbs)
