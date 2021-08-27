from pyramid.response import Response

from ushauri.odk.api import (
    getManifest,
    getMediaFile,
    getFormList,
    getXMLForm,
    storeSubmission,
)
from ushauri.odk.processes import (
    getGroupIDFromName,
    userCanRegister,
    getUserPassword,
    isUserActive,
)
from ushauri.views.classes import odkView


class formList_view(odkView):
    def processView(self):
        groupName = self.request.matchdict["group"]
        groupID = getGroupIDFromName(self.request, groupName)
        if groupID is not None:
            if isUserActive(self.request, self.user):
                if userCanRegister(self.request, groupID, self.user):
                    if self.authorize(getUserPassword(self.request, self.user)):
                        return self.createXMLResponse(
                            getFormList(self.request, groupID, groupName)
                        )
                    else:
                        return self.askForCredentials()
                else:
                    return self.askForCredentials()
            else:
                return self.askForCredentials()
        else:
            response = Response(status=404)
            return response


class push_view(odkView):
    def processView(self):
        groupName = self.request.matchdict["group"]
        groupID = getGroupIDFromName(self.request, groupName)
        if groupID is not None:
            if self.request.method == "POST":
                if isUserActive(self.request, self.user):
                    if userCanRegister(self.request, groupID, self.user):
                        if self.authorize(getUserPassword(self.request, self.user)):
                            stored, error = storeSubmission(
                                groupID, self.user, self.request
                            )
                            if stored:
                                response = Response(status=201)
                                return response
                            else:
                                response = Response(status=error)
                                return response
                        else:
                            return self.askForCredentials()
                    else:
                        response = Response(status=401)
                        return response
                else:
                    response = Response(status=401)
                    return response
            else:
                response = Response(status=404)
                return response
        else:
            response = Response(status=404)
            return response


class submission_view(odkView):
    def processView(self):
        groupName = self.request.matchdict["group"]
        groupID = getGroupIDFromName(self.request, groupName)
        if groupID is not None:
            if self.request.method == "HEAD":
                if isUserActive(self.request, self.user):
                    if userCanRegister(self.request, groupID, self.user):
                        headers = [
                            (
                                "Location",
                                self.request.route_url("odkpush", group=groupName),
                            )
                        ]
                        response = Response(headerlist=headers, status=204)
                        return response
                    else:
                        return self.askForCredentials()
                else:
                    return self.askForCredentials()
            else:
                response = Response(status=404)
                return response
        else:
            response = Response(status=404)
            return response


class XMLForm_view(odkView):
    def processView(self):
        groupName = self.request.matchdict["group"]
        groupID = getGroupIDFromName(self.request, groupName)
        if groupID is not None:
            if isUserActive(self.request, self.user):
                if userCanRegister(self.request, groupID, self.user):
                    if self.authorize(getUserPassword(self.request, self.user)):
                        return getXMLForm(groupID, self.request)
                    else:
                        return self.askForCredentials()

                else:
                    return self.askForCredentials()
            else:
                return self.askForCredentials()
        else:
            response = Response(status=404)
            return response


class manifest_view(odkView):
    def processView(self):
        groupName = self.request.matchdict["group"]
        groupID = getGroupIDFromName(self.request, groupName)
        if groupID is not None:
            if isUserActive(self.request, self.user):
                if userCanRegister(self.request, groupID, self.user):
                    if self.authorize(getUserPassword(self.request, self.user)):
                        return self.createXMLResponse(
                            getManifest(groupID, groupName, self.request)
                        )
                    else:
                        return self.askForCredentials()
                else:
                    return self.askForCredentials()
            else:
                return self.askForCredentials()
        else:
            response = Response(status=404)
            return response


class mediaFile_view(odkView):
    def processView(self):
        fileID = self.request.matchdict["fileid"]
        groupName = self.request.matchdict["group"]
        groupID = getGroupIDFromName(self.request, groupName)
        if groupID is not None:
            if isUserActive(self.request, self.user):
                if userCanRegister(self.request, groupID, self.user):
                    if self.authorize(getUserPassword(self.request, self.user)):
                        return getMediaFile(groupID, fileID, self.request)
                    else:
                        return self.askForCredentials()
                else:
                    return self.askForCredentials()
            else:
                return self.askForCredentials()
        else:
            response = Response(status=404)
            return response
