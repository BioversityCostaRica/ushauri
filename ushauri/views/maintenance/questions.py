import os
import shutil
import uuid

from pyramid.httpexceptions import HTTPFound

from ushauri.processes.db.maintenance import (
    getQuestionDetails,
    updateQuestion,
    setQuestionStatus,
    getMemberNumber,
    addAudio,
    listAnswers,
)
from ushauri.views.classes import privateView
from ushauri.views.ivr import sendReply


class modifyQuestion_view(privateView):
    def processView(self):
        groupID = self.request.matchdict["group"]
        questionID = self.request.matchdict["question"]
        data = getQuestionDetails(self.request, groupID, questionID)
        error_summary = {}
        if self.request.method == "POST":
            data = self.getPostDict()
            updateQuestion(
                self.request, questionID, data["question_tags"], data["question_text"]
            )
            return HTTPFound(location=self.request.route_url("dashboard"))

        return {
            "error_summary": error_summary,
            "data": data,
            "groupid": groupID,
            "questionid": questionID,
        }


class replyToMember_view(privateView):
    def processView(self):
        groupID = self.request.matchdict["group"]
        questionID = self.request.matchdict["question"]
        data = getQuestionDetails(self.request, groupID, questionID)
        number = getMemberNumber(self.request, data["member_id"])
        audios = listAnswers(self.request, self.user.id)
        error_summary = {}
        if data["question_status"] == 1 or data["question_status"] == -1:
            replied = False
        else:
            replied = True
        if self.request.method == "POST":
            data = self.getPostDict()
            setQuestionStatus(self.request, questionID, 2, data["audio_id"])
            sendReply(self.request, number, data["audio_id"], questionID)
            replied = True

        return {
            "error_summary": error_summary,
            "data": data,
            "groupid": groupID,
            "questionid": questionID,
            "audios": audios,
            "replied": replied,
        }


class recordAndReplyToMember_view(privateView):
    def processView(self):
        groupID = self.request.matchdict["group"]
        questionID = self.request.matchdict["question"]
        data = getQuestionDetails(self.request, groupID, questionID)
        number = getMemberNumber(self.request, data["member_id"])
        error_summary = {}
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
            addAudio(
                self.request,
                uid,
                self.request.POST["audio_desc"],
                uid + ".wav",
                2,
                self.user.id,
            )
            print("***************************88")
            setQuestionStatus(self.request, questionID, 2, uid)
            sendReply(self.request, number, uid, questionID)

        return {
            "error_summary": error_summary,
            "data": data,
            "groupid": groupID,
            "questionid": questionID,
        }
