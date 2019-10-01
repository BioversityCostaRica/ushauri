from ushauri.views.classes import privateView
from ushauri.processes.db.maintenance import (
    getUserGroups,
    getSubCounties,
    addGroup,
    getGroupMembers,
    getGroupName,
    deleteMember,
    getMemberDetails,
    updateMember,
    deleteGroup,
    getGroupDetails,
    editGroup,
    listMenus,
    getGroupAgents,
    deleteAgent,
    getAgents,
    addAgentToGroup,
)
from ushauri.odk.api import addFormToGroup
from pyramid.httpexceptions import HTTPFound, HTTPNotFound


class groupList_view(privateView):
    def processView(self):
        groups = getUserGroups(self.request, self.user.id)
        return {"groups": groups}


class addGroup_view(privateView):
    def processView(self):
        error_summary = {}
        data = {}
        subCounties = getSubCounties(self.request)
        menus = listMenus(self.request)
        if self.request.method == "POST":
            if "add" in self.request.POST:
                data = self.getPostDict()
                if data["group_sname"] != "":
                    if data["group_name"] != "":
                        if data["group_ward"] != "":
                            parts = data["district"].split("-")
                            if len(parts) == 2:
                                added, message = addGroup(
                                    self.request,
                                    data["group_name"],
                                    data["group_twoword"],
                                    data["group_ward"],
                                    data["group_sname"],
                                    parts[0],
                                    parts[1],
                                    self.user.id,
                                    data["menu_id"],
                                )
                                if added:
                                    addFormToGroup(self.request, message)
                                    return HTTPFound(
                                        location=self.request.route_url("groups")
                                    )
                                else:
                                    error_summary["error"] = message
                            else:
                                error_summary[
                                    "district"
                                ] = "You need to select a district"
                        else:
                            error_summary["group_ward"] = "The ward cannot be empty"
                    else:
                        error_summary["group_name"] = "The full name cannot be empty"
                else:
                    error_summary["group_sname"] = "The name cannot be empty"
        return {
            "error_summary": error_summary,
            "data": data,
            "subcounties": subCounties,
            "menus": menus,
        }


class modifyGroup_view(privateView):
    def processView(self):
        groupID = self.request.matchdict["group"]
        data = getGroupDetails(self.request, groupID)
        error_summary = {}
        menus = listMenus(self.request)
        if self.request.method == "POST":
            data = self.getPostDict()
            editGroup(
                self.request,
                groupID,
                data["group_name"],
                data["group_twoword"],
                data["group_ward"],
                data["menu_id"],
            )
            return HTTPFound(location=self.request.route_url("groups"))
        return {
            "error_summary": error_summary,
            "data": data,
            "groupid": groupID,
            "menus": menus,
        }


class deleteGroup_view(privateView):
    def processView(self):
        groupID = self.request.matchdict["group"]
        if self.request.method == "POST":
            deleteGroup(self.request, groupID)
            return HTTPFound(location=self.request.route_url("groups"))
        else:
            raise HTTPNotFound


class membersList_view(privateView):
    def processView(self):
        groupID = self.request.matchdict["group"]
        members = getGroupMembers(self.request, groupID)
        groupName = getGroupName(self.request, groupID)
        return {"members": members, "groupid": groupID, "groupname": groupName}


class deleteMember_view(privateView):
    def processView(self):
        groupID = self.request.matchdict["group"]
        memberID = self.request.matchdict["member"]
        if self.request.method == "POST":
            deleteMember(self.request, groupID, memberID)
            return HTTPFound(location=self.request.route_url("members", group=groupID))
        else:
            raise HTTPNotFound


class modifyMember_view(privateView):
    def processView(self):
        groupID = self.request.matchdict["group"]
        memberID = self.request.matchdict["member"]
        data = getMemberDetails(self.request, groupID, memberID)
        data["member_gender"] = str(data["member_gender"])
        error_summary = {}
        groupName = getGroupName(self.request, groupID)
        if self.request.method == "POST":
            data = self.getPostDict()
            updateMember(
                self.request,
                groupID,
                memberID,
                data["member_name"],
                data["member_tele"],
                data["member_gender"],
                data["member_village"],
            )
            return HTTPFound(location=self.request.route_url("members", group=groupID))

        return {
            "error_summary": error_summary,
            "data": data,
            "groupid": groupID,
            "groupname": groupName,
            "memberid": memberID,
        }


class agentsList_view(privateView):
    def processView(self):
        groupID = self.request.matchdict["group"]
        agents = getGroupAgents(self.request, groupID)
        groupName = getGroupName(self.request, groupID)
        return {"agents": agents, "groupid": groupID, "groupname": groupName}


class deleteAgent_view(privateView):
    def processView(self):
        groupID = self.request.matchdict["group"]
        agentID = self.request.matchdict["agent"]
        if self.request.method == "POST":
            deleteAgent(self.request, groupID, agentID)
            return HTTPFound(location=self.request.route_url("agents", group=groupID))
        else:
            raise HTTPNotFound


class addAgent_view(privateView):
    def processView(self):
        groupID = self.request.matchdict["group"]
        error_summary = {}
        data = {}
        agents = getAgents(self.request)
        if self.request.method == "POST":
            if "add" in self.request.POST:
                data = self.getPostDict()
                added, message = addAgentToGroup(
                    self.request, groupID, data["user_id"], data["access_type"]
                )
                if added:
                    return HTTPFound(
                        location=self.request.route_url("agents", group=groupID)
                    )
                else:
                    error_summary["error"] = message
        groupName = getGroupName(self.request, groupID)
        return {
            "error_summary": error_summary,
            "data": data,
            "agents": agents,
            "groupid": groupID,
            "groupname": groupName,
        }
