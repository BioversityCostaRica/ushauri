from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from ushauri.processes.db.maintenance import (
    listMenus,
    addMenu,
    modifyMenu,
    getMenuInfo,
    deleteMenu,
    listItems,
    getMenuName,
    getAllItems,
    addItem,
    getItemData,
    modifyItem,
    deleteItem,
    setItemAsStart,
    listResponses,
    getItemName,
    addRenponse,
    deleteResponse,
    listPodcasts,
)
from ushauri.views.classes import privateView


class menusList_view(privateView):
    def processView(self):
        menus = listMenus(self.request)
        return {"menus": menus}


class addMenu_view(privateView):
    def processView(self):
        error_summary = {}
        data = {}
        if self.request.method == "POST":
            if "add" in self.request.POST:
                data = self.getPostDict()
                if data["menu_name"] != "":
                    added, message = addMenu(self.request, data["menu_name"])
                    if added:
                        return HTTPFound(location=self.request.route_url("menus"))
                    else:
                        error_summary["error"] = message
                else:
                    error_summary["menu_name"] = self._("The name cannot be empty")
        return {"error_summary": error_summary, "data": data}


class modifyMenu_view(privateView):
    def processView(self):
        menuID = self.request.matchdict["menu"]
        error_summary = {}
        data = getMenuInfo(self.request, menuID)
        if self.request.method == "POST":
            if "modify" in self.request.POST:
                data = self.getPostDict()
                if data["menu_name"] != "":
                    modified, message = modifyMenu(
                        self.request, menuID, data["menu_name"]
                    )
                    if modified:
                        return HTTPFound(location=self.request.route_url("menus"))
                    else:
                        error_summary["error"] = message
                else:
                    error_summary["menu_name"] = self._("The name cannot be empty")
        return {"error_summary": error_summary, "data": data, "menuid": menuID}


class deleteMenu_view(privateView):
    def processView(self):
        menuID = self.request.matchdict["menu"]
        if self.request.method == "POST":
            deleteMenu(self.request, menuID)
            return HTTPFound(location=self.request.route_url("menus"))
        else:
            raise HTTPNotFound


class menusItemsList_view(privateView):
    def processView(self):
        menuID = self.request.matchdict["menu"]
        items = listItems(self.request, menuID)
        menuName = getMenuName(self.request, menuID)
        return {"items": items, "menuid": menuID, "menuname": menuName}


class addMenuItem_view(privateView):
    def processView(self):
        menuID = self.request.matchdict["menu"]
        menus = getAllItems(self.request)
        menuName = getMenuName(self.request, menuID)
        audios = listPodcasts(self.request)
        error_summary = {}
        data = {}
        if self.request.method == "POST":
            if "add" in self.request.POST:
                data = self.getPostDict()
                if data["item_name"] != "":
                    if data["item_type"] != "3" and data["item_desc"] == "":
                        error_summary["item_desc"] = self._("The item needs content")
                    else:
                        if data["next_item"] == "None":
                            data["next_item"] = None
                        if data["audio_id"] == "None":
                            data["audio_id"] = None
                        added, message = addItem(
                            self.request,
                            menuID,
                            data["item_type"],
                            data["item_name"],
                            data["item_desc"],
                            data["next_item"],
                            data["audio_id"],
                        )
                        if added:
                            return HTTPFound(
                                location=self.request.route_url("items", menu=menuID)
                            )
                        else:
                            error_summary["error"] = message
                else:
                    error_summary["item_name"] = self._("The name cannot be empty")

        return {
            "menus": menus,
            "menuid": menuID,
            "menuname": menuName,
            "error_summary": error_summary,
            "data": data,
            "audios": audios,
        }


class editMenuItem_view(privateView):
    def processView(self):
        menuID = self.request.matchdict["menu"]
        itemID = self.request.matchdict["item"]
        menus = getAllItems(self.request, itemID)
        menuName = getMenuName(self.request, menuID)
        error_summary = {}
        data = getItemData(self.request, itemID)
        if data["next_item"] is None:
            data["next_item"] = "None"
        if data["audio_id"] is None:
            data["audio_id"] = "None"
        audios = listPodcasts(self.request)
        data["item_type"] = str(data["item_type"])
        if self.request.method == "POST":
            if "edit" in self.request.POST:
                data = self.getPostDict()
                if data["item_name"] != "":
                    if data["item_type"] != "3" and data["item_desc"] == "":
                        error_summary["item_desc"] = self._("The item needs content")
                    else:
                        if data["next_item"] == "None":
                            data["next_item"] = None
                        if data["audio_id"] == "None":
                            data["audio_id"] = None
                        modified, message = modifyItem(
                            self.request,
                            itemID,
                            data["item_type"],
                            data["item_name"],
                            data["item_desc"],
                            data["next_item"],
                            data["audio_id"],
                        )
                        if modified:
                            return HTTPFound(
                                location=self.request.route_url("items", menu=menuID)
                            )
                        else:
                            error_summary["error"] = message
                else:
                    error_summary["item_name"] = self._("The name cannot be empty")

        return {
            "menus": menus,
            "menuid": menuID,
            "menuname": menuName,
            "error_summary": error_summary,
            "data": data,
            "itemid": itemID,
            "audios": audios,
        }


class deleteMenuItem_view(privateView):
    def processView(self):
        menuID = self.request.matchdict["menu"]
        itemID = self.request.matchdict["item"]
        if self.request.method == "POST":
            deleteItem(self.request, itemID)
            return HTTPFound(location=self.request.route_url("items", menu=menuID))
        else:
            raise HTTPNotFound


class setMenuItemAsStart_view(privateView):
    def processView(self):
        menuID = self.request.matchdict["menu"]
        itemID = self.request.matchdict["item"]
        if self.request.method == "POST":
            setItemAsStart(self.request, menuID, itemID)
            return HTTPFound(location=self.request.route_url("items", menu=menuID))
        else:
            raise HTTPNotFound


class menusItemsResponsesList_view(privateView):
    def processView(self):
        menuID = self.request.matchdict["menu"]
        itemID = self.request.matchdict["item"]
        responses = listResponses(self.request, itemID)
        menuName = getMenuName(self.request, menuID)
        itemName = getItemName(self.request, itemID)
        return {
            "responses": responses,
            "menuid": menuID,
            "menuname": menuName,
            "itemid": itemID,
            "itemname": itemName,
        }


class addItemResponse_view(privateView):
    def processView(self):
        menuID = self.request.matchdict["menu"]
        itemID = self.request.matchdict["item"]
        responses = listResponses(self.request, menuID)
        menuName = getMenuName(self.request, menuID)
        itemName = getItemName(self.request, itemID)
        menus = getAllItems(self.request, itemID)
        error_summary = {}
        data = {}
        if self.request.method == "POST":
            if "add" in self.request.POST:
                data = self.getPostDict()
                if data["target_item"] != "":
                    if data["resp_num"] != "":
                        added, message = addRenponse(
                            self.request, itemID, data["resp_num"], data["target_item"]
                        )
                        if added:
                            return HTTPFound(
                                location=self.request.route_url(
                                    "responses", menu=menuID, item=itemID
                                )
                            )
                        else:
                            error_summary["error"] = message
                    else:
                        error_summary["resp_num"] = self._(
                            "You need to indicate a response number"
                        )
                else:
                    error_summary["target_item"] = self._(
                        "You need to indicate a target item"
                    )

        return {
            "responses": responses,
            "menuid": menuID,
            "menuname": menuName,
            "itemid": itemID,
            "itemname": itemName,
            "error_summary": error_summary,
            "data": data,
            "menus": menus,
        }


class deleteItemResponse_view(privateView):
    def processView(self):
        menuID = self.request.matchdict["menu"]
        itemID = self.request.matchdict["item"]
        responseID = self.request.matchdict["resp"]
        if self.request.method == "POST":
            deleteResponse(self.request, itemID, responseID)
            return HTTPFound(
                location=self.request.route_url("responses", menu=menuID, item=itemID)
            )
        else:
            raise HTTPNotFound
