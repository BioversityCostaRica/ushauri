# -*- coding: utf-8 -*-
"""
    formshare.config.routes
    ~~~~~~~~~~~~~~~~~~

    Provides the basic routes of FormShare.

    :copyright: (c) 2017 by QLands Technology Consultants.
    :license: AGPL, see LICENSE for more details.
"""

import ushauri.plugins as p
from ushauri.plugins.utilities import addRoute
from ushauri.views.basic_views import (
    notfound_view,
    home_view,
    logout_view,
    login_view,
    register_view,
)
from ushauri.views.dashboard import dashboard_view
from ushauri.views.maintenance.audios import (
    audiosList_view,
    addAudio_view,
    modifyAudio_view,
    deleteAudio_view,
    getAudio_view,
    recordAudio_view,
)
from ushauri.views.maintenance.counties import (
    countiesList_view,
    addCounty_view,
    deleteCounty_view,
    modifyCounty_view,
    subCountiesList_view,
    addSubCounty_view,
    deleteSubCounty_view,
    editSubCounty_view,
)
from ushauri.views.maintenance.groups import (
    groupList_view,
    GroupQRCode,
    addGroup_view,
    membersList_view,
    deleteMember_view,
    modifyMember_view,
    deleteGroup_view,
    modifyGroup_view,
    agentsList_view,
    deleteAgent_view,
    addAgent_view,
)
from ushauri.views.maintenance.menus import (
    menusList_view,
    addMenu_view,
    modifyMenu_view,
    deleteMenu_view,
    menusItemsList_view,
    addMenuItem_view,
    editMenuItem_view,
    deleteMenuItem_view,
    setMenuItemAsStart_view,
    menusItemsResponsesList_view,
    addItemResponse_view,
    deleteItemResponse_view,
)
from ushauri.views.maintenance.questions import (
    modifyQuestion_view,
    replyToMember_view,
    recordAndReplyToMember_view,
)
from ushauri.views.maintenance.users import (
    userList_view,
    addUser_view,
    deleteUser_view,
    modifyUser_view,
    modifyUserPass_view,
)
from ushauri.views.odk import (
    formList_view,
    submission_view,
    push_view,
    XMLForm_view,
    manifest_view,
    mediaFile_view,
)

route_list = []

# This function append or overrides the routes to the main list
def appendToRoutes(routeList):
    for new_route in routeList:
        found = False
        pos = 0
        for curr_route in route_list:
            if curr_route["path"] == new_route["path"]:
                found = True
        pos += 1
        if not found:
            route_list.append(new_route)
        else:
            route_list[pos]["name"] = new_route["name"]
            route_list[pos]["view"] = new_route["view"]
            route_list[pos]["renderer"] = new_route["renderer"]


def loadRoutes(config):
    # Call connected to plugins to add any routes before FormShare
    for plugin in p.PluginImplementations(p.IRoutes):
        routes = plugin.before_mapping(config)
        appendToRoutes(routes)

    # FormShare routes
    routes = []
    routes.append(addRoute("home", "/", home_view, "landing/index.jinja2"))
    routes.append(addRoute("login", "/login", login_view, "dashboard/login.jinja2"))
    routes.append(
        addRoute("register", "/register", register_view, "dashboard/register.jinja2")
    )
    routes.append(addRoute("logout", "/logout", logout_view, None))
    routes.append(
        addRoute("dashboard", "/dashboard", dashboard_view, "dashboard/index.jinja2")
    )
    # Maintenace
    routes.append(
        addRoute(
            "counties",
            "/counties",
            countiesList_view,
            "/dashboard/maintenance/counties/counties.jinja2",
        )
    )
    routes.append(
        addRoute(
            "addcounty",
            "/counties/add",
            addCounty_view,
            "dashboard/maintenance/counties/add_county.jinja2",
        )
    )
    routes.append(
        addRoute("deletecounty", "/county/{county}/delete", deleteCounty_view, None)
    )
    routes.append(
        addRoute(
            "modifycounty",
            "/county/{county}/edit",
            modifyCounty_view,
            "dashboard/maintenance/counties/modify_county.jinja2",
        )
    )

    routes.append(
        addRoute(
            "subcounties",
            "/county/{county}/subcounties",
            subCountiesList_view,
            "dashboard/maintenance/counties/subcounties.jinja2",
        )
    )
    routes.append(
        addRoute(
            "addsubcounty",
            "/county/{county}/subcounties/add",
            addSubCounty_view,
            "dashboard/maintenance/counties/add_subcounty.jinja2",
        )
    )
    routes.append(
        addRoute(
            "deletesubcounty",
            "/county/{county}/subcounty/{subcounty}/delete",
            deleteSubCounty_view,
            None,
        )
    )
    routes.append(
        addRoute(
            "modifysubcounty",
            "/county/{county}/subcounty/{subcounty}/edit",
            editSubCounty_view,
            "dashboard/maintenance/counties/modify_subcounty.jinja2",
        )
    )

    routes.append(
        addRoute(
            "groups",
            "/groups",
            groupList_view,
            "dashboard/maintenance/groups/groups.jinja2",
        )
    )
    routes.append(
        addRoute(
            "addgroup",
            "/groups/add",
            addGroup_view,
            "dashboard/maintenance/groups/add_group.jinja2",
        )
    )
    routes.append(
        addRoute("deletegroup", "/group/{group}/delete", deleteGroup_view, None)
    )
    routes.append(
        addRoute(
            "modifygroup",
            "/group/{group}/modify",
            modifyGroup_view,
            "dashboard/maintenance/groups/edit_group.jinja2",
        )
    )
    routes.append(
        addRoute(
            "groupQR",
            "/group/{group}/qr",
            GroupQRCode,
            None,
        )
    )

    routes.append(
        addRoute(
            "members",
            "/group/{group}/members",
            membersList_view,
            "dashboard/maintenance/groups/members.jinja2",
        )
    )
    routes.append(
        addRoute(
            "deletemember",
            "/group/{group}/member/{member}/delete",
            deleteMember_view,
            None,
        )
    )
    routes.append(
        addRoute(
            "modifymember",
            "/group/{group}/member/{member}/modify",
            modifyMember_view,
            "dashboard/maintenance/groups/edit_member.jinja2",
        )
    )

    routes.append(
        addRoute(
            "agents",
            "/group/{group}/agents",
            agentsList_view,
            "dashboard/maintenance/groups/agents.jinja2",
        )
    )
    routes.append(
        addRoute(
            "deleteagent", "/group/{group}/agent/{agent}/delete", deleteAgent_view, None
        )
    )
    routes.append(
        addRoute(
            "addagent",
            "/group/{group}/agents/add",
            addAgent_view,
            "dashboard/maintenance/groups/add_agent.jinja2",
        )
    )

    routes.append(
        addRoute(
            "users", "/users", userList_view, "dashboard/maintenance/users/users.jinja2"
        )
    )
    routes.append(
        addRoute(
            "adduser",
            "/users/add",
            addUser_view,
            "dashboard/maintenance/users/add_user.jinja2",
        )
    )
    routes.append(
        addRoute(
            "deleteuser",
            "/user/{user}/delete",
            deleteUser_view,
            "dashboard/maintenance/users/add_user.jinja2",
        )
    )
    routes.append(
        addRoute(
            "modifyuser",
            "/user/{user}/modify",
            modifyUser_view,
            "dashboard/maintenance/users/edit_user.jinja2",
        )
    )
    routes.append(
        addRoute(
            "modifyuserpass",
            "/user/{user}/modifypass",
            modifyUserPass_view,
            "dashboard/maintenance/users/edit_pass.jinja2",
        )
    )

    routes.append(
        addRoute(
            "menus",
            "/menus",
            menusList_view,
            "dashboard/maintenance/menus/menus.jinja2",
        )
    )
    routes.append(
        addRoute(
            "addmenu",
            "/menus/add",
            addMenu_view,
            "dashboard/maintenance/menus/add_menu.jinja2",
        )
    )
    routes.append(
        addRoute(
            "modifymenu",
            "/menu/{menu}/modify",
            modifyMenu_view,
            "dashboard/maintenance/menus/edit_menu.jinja2",
        )
    )
    routes.append(addRoute("deletemenu", "/menu/{menu}/delete", deleteMenu_view, None))

    routes.append(
        addRoute(
            "items",
            "/menu/{menu}/items",
            menusItemsList_view,
            "dashboard/maintenance/menus/items.jinja2",
        )
    )
    routes.append(
        addRoute(
            "additem",
            "/menu/{menu}/add",
            addMenuItem_view,
            "dashboard/maintenance/menus/add_item.jinja2",
        )
    )
    routes.append(
        addRoute(
            "edititem",
            "/menu/{menu}/item/{item}/edit",
            editMenuItem_view,
            "dashboard/maintenance/menus/edit_item.jinja2",
        )
    )
    routes.append(
        addRoute(
            "deleteitem", "/menu/{menu}/item/{item}/delete", deleteMenuItem_view, None
        )
    )
    routes.append(
        addRoute(
            "itemstart", "/menu/{menu}/item/{item}/start", setMenuItemAsStart_view, None
        )
    )
    routes.append(
        addRoute(
            "responses",
            "/menu/{menu}/item/{item}/responses",
            menusItemsResponsesList_view,
            "dashboard/maintenance/menus/responses.jinja2",
        )
    )
    routes.append(
        addRoute(
            "addresponse",
            "/menu/{menu}/item/{item}/responses/add",
            addItemResponse_view,
            "dashboard/maintenance/menus/add_response.jinja2",
        )
    )
    routes.append(
        addRoute(
            "deleteresponse",
            "/menu/{menu}/item/{item}/response/{resp}/delete",
            deleteItemResponse_view,
            None,
        )
    )

    routes.append(
        addRoute(
            "audios",
            "/audios",
            audiosList_view,
            "dashboard/maintenance/audios/audios.jinja2",
        )
    )
    routes.append(
        addRoute(
            "addaudio",
            "/audios/add",
            addAudio_view,
            "dashboard/maintenance/audios/add_audio.jinja2",
        )
    )
    routes.append(
        addRoute(
            "editaudio",
            "/audios/{audio}/edit",
            modifyAudio_view,
            "dashboard/maintenance/audios/edit_audio.jinja2",
        )
    )
    routes.append(
        addRoute("deleteaudio", "/audios/{audio}/delete", deleteAudio_view, None)
    )
    routes.append(addRoute("playaudio", "/audios/{audio}/play", getAudio_view, None))
    routes.append(
        addRoute(
            "recordaudio",
            "/audios/record",
            recordAudio_view,
            "dashboard/maintenance/audios/record.jinja2",
        )
    )

    routes.append(
        addRoute(
            "modifyquestion",
            "/group/{group}/question/{question}/modify",
            modifyQuestion_view,
            "dashboard/maintenance/questions/edit_question.jinja2",
        )
    )
    routes.append(
        addRoute(
            "replytomember",
            "/group/{group}/question/{question}/reply",
            replyToMember_view,
            "dashboard/maintenance/questions/reply_to_member.jinja2",
        )
    )
    routes.append(
        addRoute(
            "recordandreplytomember",
            "/group/{group}/question/{question}/record",
            recordAndReplyToMember_view,
            "dashboard/maintenance/questions/record_a_reply.jinja2",
        )
    )

    # ODK Forms
    routes.append(
        addRoute("odkformlist", "/register/{group}/formList", formList_view, None)
    )
    routes.append(
        addRoute("odksubmission", "/register/{group}/submission", submission_view, None)
    )
    routes.append(addRoute("odkpush", "/register/{group}/push", push_view, None))
    routes.append(
        addRoute("odkxmlform", "/register/{group}/xmlform", XMLForm_view, None)
    )
    routes.append(
        addRoute("odkmanifest", "/register/{group}/manifest", manifest_view, None)
    )
    routes.append(
        addRoute(
            "odkmediafile",
            "/register/{group}/manifest/mediafile/{fileid}",
            mediaFile_view,
            None,
        )
    )

    appendToRoutes(routes)

    # Add the not found route
    config.add_notfound_view(notfound_view, renderer="404.jinja2")

    # Call connected plugins to add any routes after FormShare
    for plugin in p.PluginImplementations(p.IRoutes):
        routes = plugin.after_mapping(config)
        appendToRoutes(routes)

    # Now add the routes and views to the Pyramid config
    for curr_route in route_list:
        config.add_route(curr_route["name"], curr_route["path"])
        config.add_view(
            curr_route["view"],
            route_name=curr_route["name"],
            renderer=curr_route["renderer"],
        )
