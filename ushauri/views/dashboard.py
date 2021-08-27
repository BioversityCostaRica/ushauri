from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from ushauri.processes.db.maintenance import (
    getQuestions,
    getGroupDetails,
    getOneGroup,
    getActiveGroup,
    setActiveGroup,
)
from ushauri.views.classes import privateView


class dashboard_view(privateView):
    def processView(self):
        if "group" in self.request.params.keys():
            activeGroup = self.request.params["group"]
            groupDetails = getGroupDetails(self.request, activeGroup)
            if groupDetails:
                setActiveGroup(self.request, activeGroup, self.user.id)
                questions = getQuestions(self.request, activeGroup)
                return {
                    "questions": questions,
                    "groupdetails": groupDetails,
                    "groupid": activeGroup,
                }
            else:
                raise HTTPNotFound
        else:
            activeGroup = getActiveGroup(self.request, self.user.id)
            if activeGroup is not None:
                return HTTPFound(
                    location=self.request.route_url(
                        "dashboard", _query={"group": activeGroup}
                    )
                )
            else:
                newGroup = getOneGroup(self.request, self.user.id)
                if newGroup is not None:
                    setActiveGroup(self.request, newGroup, self.user.id)
                    return HTTPFound(
                        location=self.request.route_url(
                            "dashboard", _query={"group": newGroup}
                        )
                    )
                else:
                    return {"questions": [], "groupdetails": {}, "groupid": None}
