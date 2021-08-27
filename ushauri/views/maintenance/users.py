from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from ushauri.processes.db.maintenance import (
    getUsers,
    getSubCounties,
    addUser,
    deleteUser,
    getUserDetails,
    modifyUser,
    listMenus,
    modifyPassword,
)
from ushauri.views.classes import privateView


class userList_view(privateView):
    def processView(self):
        if self.user.admin == False:
            raise HTTPNotFound
        users = getUsers(self.request)
        return {"users": users}


class addUser_view(privateView):
    def processView(self):
        if self.user.admin == False:
            raise HTTPNotFound
        error_summary = {}
        data = {}
        subCounties = getSubCounties(self.request)
        menus = listMenus(self.request)
        if self.request.method == "POST":
            if "add" in self.request.POST:
                data = self.getPostDict()
                if data["user_id"] != "":
                    if data["password1"] != "":
                        if data["password1"] == data["password2"]:
                            parts = data["district"].split("-")
                            if len(parts) == 2:
                                added, message = addUser(
                                    self.request,
                                    data["user_id"],
                                    data["user_name"],
                                    data["user_telef"],
                                    data["user_email"],
                                    parts[0],
                                    parts[1],
                                    data["password1"],
                                    data["menu_id"],
                                )
                                if added:
                                    return HTTPFound(
                                        location=self.request.route_url("users")
                                    )
                                else:
                                    error_summary["error"] = message
                            else:
                                error_summary["district"] = self._(
                                    "You need to select a district"
                                )
                        else:
                            error_summary["password1"] = self._(
                                "The password and its confirmation are not the same"
                            )
                    else:
                        error_summary["password1"] = self._(
                            "The password cannot be blank"
                        )
                else:
                    error_summary["user_id"] = self._("The user ID cannot be blank")

        return {
            "error_summary": error_summary,
            "data": data,
            "subcounties": subCounties,
            "menus": menus,
        }


class deleteUser_view(privateView):
    def processView(self):
        if self.user.admin == False:
            raise HTTPNotFound
        userID = self.request.matchdict["user"]
        if self.request.method == "POST":
            deleteUser(self.request, userID)
            return HTTPFound(location=self.request.route_url("users"))
        else:
            raise HTTPNotFound


class modifyUser_view(privateView):
    def processView(self):
        if self.user.admin == False:
            raise HTTPNotFound
        error_summary = {}
        userID = self.request.matchdict["user"]
        data = getUserDetails(self.request, userID)
        menus = listMenus(self.request)
        if self.request.method == "POST":
            if "edit" in self.request.POST:
                data = self.getPostDict()
                modified, message = modifyUser(
                    self.request,
                    userID,
                    data["user_name"],
                    data["user_telef"],
                    data["user_email"],
                    data["menu_id"],
                )
                if modified:
                    return HTTPFound(location=self.request.route_url("users"))

        return {
            "error_summary": error_summary,
            "data": data,
            "menus": menus,
            "userid": userID,
        }


class modifyUserPass_view(privateView):
    def processView(self):
        if self.user.admin == False:
            raise HTTPNotFound
        error_summary = {}
        userID = self.request.matchdict["user"]
        data = getUserDetails(self.request, userID)
        menus = listMenus(self.request)
        if self.request.method == "POST":
            if "edit" in self.request.POST:
                data = self.getPostDict()
                if data["password1"] != "":
                    if data["password1"] == data["password2"]:
                        modified, message = modifyPassword(
                            self.request, userID, data["password1"]
                        )
                        if modified:
                            return HTTPFound(location=self.request.route_url("users"))
                    else:
                        error_summary["password1"] = self._(
                            "The password and its confirmation are not the same"
                        )
                else:
                    error_summary["password1"] = self._("The password cannot be blank")
        return {
            "error_summary": error_summary,
            "data": data,
            "menus": menus,
            "userid": userID,
        }
