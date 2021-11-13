# from pprint import pprint
import re


# This function takes in gcode as a stri
# ng and extracts the thumbnails from
# them to use for web rendering in the
# *future*. Woohoo!
def extractPrusaThumbnails(data: list):
    # Basic capturing groups.
    matches = re.findall(
        r"(thumbnail begin.*?\n)(.*?)(; thumbnail end)", data, flags=re.S
    )

    thumbs = []

    for (
        m
    ) in (
        matches
    ):  # Remove the line endings, and remove the newlines.  Should work then.
        thumbs.append(m[1].replace("; ", "").replace("\n", "").strip())

    return thumbs


def detectGCodeType(lines: list):
    for l in lines:
        if l.startswith(";") and "Generated with Cura_" in l:
            return "CURA"

        if l.startswith(";") and "generated by PrusaSlicer" in l:
            return "PRUSASLICER"

    return "UNKNOWN"


def extractPrusaGCodeInfo(filename: str, fileData: str):

    # data = file.read().decode('utf-8')
    # print(type(data))

    data = fileData

    importantKeys = [
        "estimated printing time (normal mode)",
        "total filament used [g]",
        "filament_type",
        "default_filament_profile",
        "thumbnails",
    ]

    lines = [x for x in data.split("\n") if ((x.startswith(";")) and ("=" in x))]
    # this filters our gcode to parse to only the comments at the end from the slicer.

    outputKeys = {"filename": filename}

    # Because we filter by commented lines, and then iterate by keys, we need to check that we didn't already mess with a given line and we do that by checking whether it's split already or not.
    for line in lines:
        for k in importantKeys:
            if type(line) != type([]):
                if k in line.split("=")[0]:
                    line = [x.strip() for x in line.split("=")]

                    # this gets rid of anything we can't deal with.
                    extraneous_chars = ["[", "]", "; ", "(", ")"]
                    for c in extraneous_chars:
                        line[0] = line[0].replace(c, "")

                    line[0] = line[0].replace(" ", "_")

                    # print(line[0])

                    outputKeys[line[0]] = line[1]
                    # print(line)

    # Test keys pulled from PrusaSlicer 2.3 on Linux at home.

    # ; estimated printing time (normal mode) = 1h 54m 11s
    # ; filament used [g] = 9.53
    # ; filament_type = PLA
    # ; default_filament_profile = "Generic PLA @CREALITY"
    # pprint(outputKeys)

    timeString = outputKeys["estimated_printing_time_normal_mode"].strip()

    print(timeString)
    timeTotalSeconds = 0

    for componentTime in timeString.split(" "):
        if componentTime[-1] == "d":
            timeTotalSeconds += int(componentTime.replace("d", "")) * 24 * 3600
        if componentTime[-1] == "h":
            timeTotalSeconds += int(componentTime.replace("h", "")) * 3600
        if componentTime[-1] == "m":
            timeTotalSeconds += int(componentTime.replace("m", "")) * 60
        if componentTime[-1] == "s":
            timeTotalSeconds += int(componentTime.replace("s", ""))

    outputKeys["printTimeSeconds"] = timeTotalSeconds

    return outputKeys
