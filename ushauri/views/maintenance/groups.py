from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from ushauri.processes.color_hash import ColorHash
from ushauri.odk.api import addFormToGroup
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
from ushauri.views.classes import privateView
import json
import zlib
import os
import base64
import uuid
import qrcode
from pyramid.response import FileResponse


class groupList_view(privateView):
    def processView(self):
        groups = getUserGroups(self.request, self.user.id)
        return {"groups": groups}


class GroupQRCode(privateView):
    def processView(self):
        group_id = self.request.matchdict["group"]

        data = getGroupDetails(self.request, group_id)
        url = self.request.route_url("odkformlist", group=data["group_sname"])
        url = url.replace("/formList", "")
        group_color = ColorHash(data["group_sname"]).hex
        odk_settings = {
            "admin": {"change_server": True, "change_form_metadata": False},
            "general": {
                "change_server": True,
                "navigation": "buttons",
                "server_url": url,
            },
            "project": {
                "name": data["group_name"],
                "icon": data["group_sname"][0],
                "color": group_color,
            },
        }
        qr_json = json.dumps(odk_settings).encode()
        zip_json = zlib.compress(qr_json)
        serialization = base64.encodebytes(zip_json)
        serialization = serialization.decode()
        serialization = serialization.replace("\n", "")
        img = qrcode.make(serialization)

        repository_path = self.request.registry.settings["repository"]
        if not os.path.exists(repository_path):
            os.makedirs(repository_path)
        unique_id = str(uuid.uuid4())
        temp_path = os.path.join(repository_path, *["tmp", unique_id])
        os.makedirs(temp_path)

        qr_file = os.path.join(temp_path, *[group_id + ".png"])
        img.save(qr_file)
        response = FileResponse(qr_file, request=self.request, content_type="image/png")
        response.content_disposition = 'attachment; filename="' + group_id + '.png"'
        self.justReturn = True
        return response


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
                                error_summary["district"] = self._(
                                    "You need to select a district"
                                )
                        else:
                            error_summary["group_ward"] = self._(
                                "The ward cannot be empty"
                            )
                    else:
                        error_summary["group_name"] = self._(
                            "The full name cannot be empty"
                        )
                else:
                    error_summary["group_sname"] = self._("The name cannot be empty")
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
