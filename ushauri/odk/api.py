import glob
import io
import json
import logging
import mimetypes
import os
import shutil
import zipfile
from hashlib import md5
from subprocess import Popen, PIPE
from uuid import uuid4

from lxml import etree
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse

from ushauri.odk.processes import userCanRegister, storeRegistration

log = logging.getLogger(__name__)


class FileIterator(object):
    chunk_size = 4096

    def __init__(self, filename):
        self.filename = filename
        self.fileobj = open(self.filename, "rb")

    def __iter__(self):
        return self

    def next(self):
        chunk = self.fileobj.read(self.chunk_size)
        if not chunk:
            raise StopIteration
        return chunk

    __next__ = next  # py3 compat


# An Object containing the file download iterator
class FileIterable(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        return FileIterator(self.filename)


def generateFormList(projectArray):
    root = etree.Element("xforms", xmlns="http://openrosa.org/xforms/xformsList")
    for project in projectArray:
        xformTag = etree.Element("xform")
        for key, value in project.items():
            atag = etree.Element(key)
            atag.text = value
            xformTag.append(atag)
        root.append(xformTag)
    return etree.tostring(root, encoding="utf-8")


def generateManifest(mediaFileArray):
    root = etree.Element("manifest", xmlns="http://openrosa.org/xforms/xformsManifest")
    for file in mediaFileArray:
        xformTag = etree.Element("mediaFile")
        for key, value in file.items():
            atag = etree.Element(key)
            atag.text = value
            xformTag.append(atag)
        root.append(xformTag)
    return etree.tostring(root, encoding="utf-8")


def getFormList(request, groupID, groupName):
    ODKDir = request.registry.settings["odk.repository"]
    prjList = []
    path = os.path.join(ODKDir, *["forms", groupID, "*.json"])
    files = glob.glob(path)
    if files:
        with io.open(files[0], encoding="utf8") as data_file:
            data = json.load(data_file)
            data["downloadUrl"] = request.route_url("odkxmlform", group=groupName)
            data["manifestUrl"] = request.route_url("odkmanifest", group=groupName)
        prjList.append(data)
    return generateFormList(prjList)


def getManifest(groupID, groupName, request):
    ODKDir = request.registry.settings["odk.repository"]
    path = os.path.join(ODKDir, *["forms", groupID, "media", "*.*"])
    files = glob.glob(path)
    if files:
        fileArray = []
        for file in files:
            fileName = os.path.basename(file)
            fileArray.append(
                {
                    "filename": fileName,
                    "hash": "md5:" + md5(open(file, "rb").read()).hexdigest(),
                    "downloadUrl": request.route_url(
                        "odkmediafile", group=groupName, fileid=fileName
                    ),
                }
            )
        return generateManifest(fileArray)
    else:
        return generateManifest([])


def getXMLForm(groupID, request):
    ODKDir = request.registry.settings["odk.repository"]
    path = os.path.join(ODKDir, *["forms", groupID, "*.xml"])
    files = glob.glob(path)
    if files:
        content_type, content_enc = mimetypes.guess_type(files[0])
        fileName = os.path.basename(files[0])
        response = FileResponse(files[0], request=request, content_type=content_type)
        response.content_disposition = 'attachment; filename="' + fileName + '"'
        return response
    else:
        raise HTTPNotFound()


def getMediaFile(groupID, fileid, request):
    ODKDir = request.registry.settings["odk.repository"]
    path = os.path.join(ODKDir, *["forms", groupID, "media", fileid])
    if os.path.isfile(path):
        content_type, content_enc = mimetypes.guess_type(path)
        fileName = os.path.basename(path)
        response = FileResponse(path, request=request, content_type=content_type)
        response.content_disposition = 'attachment; filename="' + fileName + '"'
        return response
    else:
        raise HTTPNotFound()


def getSubmissionFile(groupID, submissionID, request):
    ODKDir = request.registry.settings["odk.repository"]
    path = os.path.join(
        ODKDir, *["forms", groupID, "submissions", submissionID + ".json"]
    )
    if os.path.isfile(path):
        content_type, content_enc = mimetypes.guess_type(path)
        fileName = os.path.basename(path)
        response = FileResponse(path, request=request, content_type=content_type)
        response.content_disposition = 'attachment; filename="' + fileName + '"'
        return response
    else:
        raise HTTPNotFound()


def moveMediaFiles(ODKDir, XFormDirectory, srcSubmission, trgSubmission):
    sourcePath = os.path.join(
        ODKDir, *["forms", XFormDirectory, "submissions", srcSubmission, "*.*"]
    )
    targetPath = os.path.join(
        ODKDir, *["forms", XFormDirectory, "submissions", trgSubmission]
    )
    files = glob.glob(sourcePath)
    for file in files:
        try:
            shutil.move(file, targetPath)
        except Exception as e:
            log.debug(
                "moveMediaFiles. Error moving from "
                + srcSubmission
                + " to "
                + trgSubmission
                + " . Message: "
                + str(e)
            )


def convertXMLToJSON(ODKDir, XMLFile, groupID, request):
    XMLtoJSON = os.path.join(
        request.registry.settings["odktools.path"], *["XMLtoJSON", "xmltojson"]
    )
    TJSONFile = XMLFile.replace(".xml", ".tmp.json")
    JSONFile = XMLFile.replace(".xml", ".json")
    submissionID = os.path.basename(XMLFile)
    submissionID = submissionID.replace(".xml", "")
    XMLFormFile = os.path.join(
        ODKDir,
        *["forms", groupID, request.registry.settings["registryXFormFile"] + ".xml"]
    )
    # First we convert the XML to a temporal JSON
    args = []
    args.append(XMLtoJSON)
    args.append("-i " + XMLFile)
    args.append("-o " + TJSONFile)
    args.append("-x " + XMLFormFile)
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        # We compare the MD5Sum of the testing submissions so the
        # media files are stored in the proper way if ODK Collect
        # send the media files in separate submissions when such
        # file are so big that separation is required
        try:
            shutil.move(TJSONFile, JSONFile)
            submissionsPath = os.path.join(
                ODKDir, *["forms", groupID, "submissions", "*.json"]
            )
            files = glob.glob(submissionsPath)
            md5sum = md5(open(JSONFile, "rb").read()).hexdigest()
            for aFile in files:
                if aFile != JSONFile:
                    othmd5sum = md5(open(aFile, "rb").read()).hexdigest()
                    if md5sum == othmd5sum:
                        targetSubmissionID = os.path.basename(aFile)
                        targetSubmissionID = targetSubmissionID.replace(".json", "")
                        moveMediaFiles(
                            ODKDir, groupID, targetSubmissionID, submissionID
                        )
                        os.remove(aFile)
            stored, message = storeRegistration(request, JSONFile, groupID)
            if not stored:
                log.debug(message)
                return 1, message
            else:
                return 0, ""
        except Exception as e:
            log.debug(
                "XMLToJSON error. Temporary file "
                + TJSONFile
                + " might not exist! Error: "
                + str(e)
            )
            return 1, ""

    else:
        log.debug(
            "XMLToJSON error. Converting "
            + XMLFile
            + "  to "
            + JSONFile
            + ". Error: "
            + stdout.decode()
            + "-"
            + stderr.decode()
            + ". Command line: "
            + " ".join(args)
        )
        return 1, ""


def storeSubmission(groupID, userID, request):
    ODKDir = request.registry.settings["odk.repository"]
    iniqueID = uuid4()
    path = os.path.join(ODKDir, *["submissions", str(iniqueID)])
    os.makedirs(path)
    XMLFile = ""
    for key in request.POST.keys():
        try:
            filename = request.POST[key].filename
            if filename.upper().find(".XML") >= 0:
                filename = str(iniqueID) + ".xml"
            input_file = request.POST[key].file
            file_path = os.path.join(path, filename)
            if file_path.upper().find(".XML") >= 0:
                XMLFile = file_path
            temp_file_path = file_path + "~"
            input_file.seek(0)
            with open(temp_file_path, "wb") as output_file:
                shutil.copyfileobj(input_file, output_file)
            # Now that we know the file has been fully saved to disk move it into place.
            os.rename(temp_file_path, file_path)
        except Exception as e:
            log.debug(
                "Submission "
                + str(iniqueID)
                + " has POST error key: "
                + key
                + " Error: "
                + str(e)
            )
    if XMLFile != "":
        tree = etree.parse(XMLFile)
        root = tree.getroot()
        XFormID = root.get("id")
        if XFormID is not None:
            if XFormID == request.registry.settings["registryXFormID"]:
                if userCanRegister(request, groupID, userID):
                    mediaPath = os.path.join(
                        ODKDir,
                        *["forms", groupID, "submissions", str(iniqueID), "diffs"]
                    )
                    os.makedirs(mediaPath)
                    mediaPath = os.path.join(
                        ODKDir, *["forms", groupID, "submissions", str(iniqueID)]
                    )
                    targetPath = os.path.join(
                        ODKDir, *["forms", groupID, "submissions"]
                    )
                    path = os.path.join(path, *["*.*"])
                    files = glob.glob(path)
                    XMLFile = ""
                    for file in files:
                        basefile = os.path.basename(file)
                        if basefile.upper().find(".XML") >= 0:
                            targetFile = os.path.join(targetPath, basefile)
                            XMLFile = targetFile
                        else:
                            targetFile = os.path.join(mediaPath, basefile)
                        shutil.move(file, targetFile)
                    if XMLFile != "":
                        resCode, message = convertXMLToJSON(
                            ODKDir, XMLFile, groupID, request
                        )
                        if resCode == 0:
                            return True, 201
                        else:
                            if resCode == 1:
                                print(message)
                                return False, 500
                            else:
                                return True, 201
                    else:
                        return False, 404
                else:
                    log.debug("Enumerator %s cannot submit data to %s", userID, XFormID)
                    return False, 404
            else:
                log.debug(
                    "Submission for ID %s does not exist in the database", XFormID
                )
                return False, 404
        else:
            log.debug("Submission does not have and ID")
            return False, 404
    else:
        log.debug("Submission does not have an XML file")
        return False, 500


def addFormToGroup(request, groupID):
    ODKDir = request.registry.settings["odk.repository"]
    formPath = os.path.join(ODKDir, *["forms", groupID])
    os.makedirs(formPath)
    with zipfile.ZipFile(
        request.registry.settings["registryXFormzipFile"], "r"
    ) as zip_ref:
        zip_ref.extractall(formPath)
