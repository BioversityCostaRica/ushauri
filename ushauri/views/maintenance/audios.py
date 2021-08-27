import os
import shutil
import uuid

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.response import FileResponse

from ushauri.processes.db.maintenance import (
    listAudios,
    addAudio,
    modifyAudio,
    getAudioDesc,
    deleteAudio,
    getActiveGroup,
    getAudioFile,
)
from ushauri.views.classes import privateView


class audiosList_view(privateView):
    def processView(self):
        if not self.user.admin:
            activeGroup = getActiveGroup(self.request, self.user.id)
            if activeGroup is not None:
                audios = listAudios(self.request, activeGroup, False)
            else:
                audios = listAudios(self.request, "NA", False)
        else:
            audios = listAudios(self.request, None, True)
        return {"audios": audios}


def getAudio_view(request):
    audioID = request.matchdict["audio"]
    audioFile = getAudioFile(request, audioID)
    if audioFile is not None:
        response = FileResponse(
            os.path.join(request.registry.settings["audioPath"], *[audioFile]),
            request=request,
            content_type="audio/wav",
        )
        return response
    else:
        raise HTTPNotFound


class addAudio_view(privateView):
    def processView(self):
        error_summary = {}
        data = {}
        if self.request.method == "POST":
            if "add" in self.request.POST:
                data = self.getPostDict()
                if data["audio_desc"] != "":
                    filename = self.request.POST["audio"].filename
                    input_file = self.request.POST["audio"].file
                    filename, file_extension = os.path.splitext(filename)

                    uid = str(uuid.uuid4())
                    audioPath = self.request.registry.settings["audioPath"]
                    file_path = os.path.join(audioPath, uid + file_extension)
                    temp_file_path = file_path + "~"
                    input_file.seek(0)
                    with open(temp_file_path, "wb") as output_file:
                        shutil.copyfileobj(input_file, output_file)
                    os.rename(temp_file_path, file_path)
                    if not self.user.admin:
                        added, message = addAudio(
                            self.request,
                            uid,
                            data["audio_desc"],
                            uid + file_extension,
                            2,
                            self.user.id,
                        )
                    else:
                        added, message = addAudio(
                            self.request,
                            uid,
                            data["audio_desc"],
                            uid + file_extension,
                            1,
                            self.user.id,
                        )
                    if added:
                        return HTTPFound(location=self.request.route_url("audios"))
                    else:
                        error_summary["error"] = message
                else:
                    error_summary["audio_desc"] = self._(
                        "The description cannot be empty"
                    )
        return {"error_summary": error_summary, "data": data}


class recordAudio_view(privateView):
    def processView(self):
        error_summary = {}
        data = {}
        if self.request.method == "POST":
            print("***************************88")
            print(self.request.POST)
            input_file = self.request.POST["data"].file
            uid = str(uuid.uuid4())
            audioPath = self.request.registry.settings["audioPath"]
            file_path = os.path.join(audioPath, uid + ".wav")
            temp_file_path = file_path + "~"
            input_file.seek(0)
            with open(temp_file_path, "wb") as output_file:
                shutil.copyfileobj(input_file, output_file)
            # Now that we know the file has been fully saved to disk move it into place.
            os.rename(temp_file_path, file_path)
            added, message = addAudio(
                self.request,
                uid,
                self.request.POST["audio_desc"],
                uid + ".wav",
                2,
                self.user.id,
            )
            print("***************************88")
        return {"error_summary": error_summary, "data": data}


class modifyAudio_view(privateView):
    def processView(self):
        audioID = self.request.matchdict["audio"]
        error_summary = {}
        data = {"audio_desc": getAudioDesc(self.request, audioID)}
        if self.request.method == "POST":
            if "edit" in self.request.POST:
                data = self.getPostDict()
                if data["audio_desc"] != "":
                    modified, message = modifyAudio(
                        self.request, audioID, data["audio_desc"]
                    )
                    if modified:
                        return HTTPFound(location=self.request.route_url("audios"))
                    else:
                        error_summary["error"] = message
                else:
                    error_summary["audio_desc"] = self._(
                        "The description cannot be empty"
                    )
        return {"error_summary": error_summary, "data": data, "audioid": audioID}


class deleteAudio_view(privateView):
    def processView(self):
        audioID = self.request.matchdict["audio"]
        if self.request.method == "POST":
            deleteAudio(self.request, audioID)
            return HTTPFound(location=self.request.route_url("audios"))
        else:
            raise HTTPNotFound
