import datetime
import sys
import uuid

from sqlalchemy.exc import IntegrityError

from ushauri.config.encdecdata import AESCipher
from ushauri.models import (
    Advgroup,
    Member,
    County,
    Subcounty,
    Groupuser,
    User,
    Ivrmenu,
    Menuitem,
    Response,
    Audio,
    Question,
)


def getMemberCount(request, groupID):
    res = request.dbsession.query(Member).filter(Member.group_id == groupID).count()
    return res


def getQuestionCount(request, groupID):
    res = (
        request.dbsession.query(Question)
        .filter(Question.group_id == groupID)
        .filter(Question.question_status == 1)
        .count()
    )
    return res


def getUserGroups(request, userID):
    sql = (
        "SELECT advgroup.group_id,advgroup.group_name,advgroup.group_twoword,advgroup.group_ward,advgroup.group_lat,"
        "advgroup.group_long,advgroup.group_elev,advgroup.county_id,advgroup.subcounty_id,"
        "advgroup.group_sname,county.county_name,subcounty.subcounty_name "
        "FROM advgroup,groupuser,subcounty,county "
        "WHERE advgroup.group_id = groupuser.group_id "
        "AND advgroup.county_id = subcounty.county_id "
        "AND advgroup.subcounty_id = subcounty.subcounty_id "
        "AND subcounty.county_id = county.county_id "
        "AND groupuser.user_id = '" + userID + "'"
    )
    result = []
    groups = request.dbsession.execute(sql).fetchall()
    for group in groups:
        result.append(
            {
                "group_id": group.group_id,
                "group_name": group.group_name,
                "group_twoword": group.group_twoword,
                "group_ward": group.group_ward,
                "group_sname": group.group_sname,
                "county_name": group.county_name,
                "subcounty_name": group.subcounty_name,
                "members": getMemberCount(request, group.group_id),
                "questions": getQuestionCount(request, group.group_id),
            }
        )
    return result


def getGroupAgents(request, groupID):
    sql = (
        "SELECT user.user_id,user.user_name,groupuser.access_type "
        "FROM user,groupuser "
        "WHERE groupuser.user_id = user.user_id "
        "AND groupuser.group_id = '" + groupID + "'"
    )

    agents = request.dbsession.execute(sql).fetchall()
    result = []
    for agent in agents:
        result.append(
            {
                "user_id": agent.user_id,
                "user_name": agent.user_name,
                "access_type": agent.access_type,
            }
        )
    return result


def deleteAgent(request, groupID, agentID):
    try:
        request.dbsession.query(Groupuser).filter(Groupuser.group_id == groupID).filter(
            Groupuser.user_id == agentID
        ).delete()
        return True, ""
    except Exception as e:
        return False, str(e)


def addAgentToGroup(request, groupID, agentID, access):
    try:
        newAgent = Groupuser(
            group_id=groupID, user_id=agentID, access_type=access, group_active=0
        )
        request.dbsession.add(newAgent)
        return True, ""
    except Exception as e:
        return False, str(e)


def setActiveGroup(request, groupID, agentID):
    try:
        request.dbsession.query(Groupuser).filter(Groupuser.user_id == agentID).update(
            {"group_active": 0}
        )
        request.dbsession.query(Groupuser).filter(Groupuser.group_id == groupID).filter(
            Groupuser.user_id == agentID
        ).update({"group_active": 1})
        return True, ""
    except Exception as e:
        return False, str(e)


def getActiveGroup(request, agentID):
    res = (
        request.dbsession.query(Groupuser)
        .filter(Groupuser.user_id == agentID)
        .filter(Groupuser.group_active == 1)
        .first()
    )
    if res is None:
        return None
    else:
        return res.group_id


def getAgents(request):
    result = []
    users = request.dbsession.query(User).all()
    for user in users:
        result.append({"user_id": user.user_id, "user_name": user.user_name})
    return result


def getGroupMembers(request, groupID):
    result = []
    members = request.dbsession.query(Member).filter(Member.group_id == groupID).all()
    for member in members:
        result.append(
            {
                "member_id": member.member_id,
                "member_name": member.member_name,
                "member_tele": member.member_tele,
                "member_gender": member.member_gender,
                "member_village": member.member_village,
                "member_gardentype": member.member_gardentype,
            }
        )
    return result


def getGroupName(request, groupID):
    res = request.dbsession.query(Advgroup).filter(Advgroup.group_id == groupID).first()
    return res.group_name


def getMemberDetails(request, groupID, memberID):
    res = (
        request.dbsession.query(Member)
        .filter(Member.group_id == groupID)
        .filter(Member.member_id == memberID)
        .first()
    )
    if res is not None:
        return {
            "member_name": res.member_name,
            "member_tele": res.member_tele,
            "member_gender": res.member_gender,
            "member_village": res.member_village,
        }
    return {}


def deleteMember(request, groupID, memberID):
    try:
        request.dbsession.query(Member).filter(Member.group_id == groupID).filter(
            Member.member_id == memberID
        ).delete()
        return True, ""
    except Exception as e:
        return False, str(e)


def updateMember(request, groupID, memberID, name, telephone, gender, village):
    try:
        request.dbsession.query(Member).filter(Member.group_id == groupID).filter(
            Member.member_id == memberID
        ).update(
            {
                "member_name": name,
                "member_tele": telephone,
                "member_gender": gender,
                "member_village": village,
            }
        )
        return True, ""
    except Exception as e:
        return False, str(e)


def getAudioDesc2(request, audioID):
    if audioID is not None:
        res = request.dbsession.query(Audio).filter(Audio.audio_id == audioID).first()
        if res is not None:
            return res.audio_desc
        else:
            return ""
    else:
        return ""


def getQuestions(request, groupID):
    result = []
    questions = request.dbsession.query(Question).filter(Question.group_id == groupID)
    for question in questions:
        tags = []
        stags = question.question_tags
        if stags is not None:
            tags = stags.split(",")
        result.append(
            {
                "group_id": groupID,
                "question_id": question.question_id,
                "member_id": question.member_id,
                "question_dtime": question.question_dtime,
                "question_audiofile": question.question_audiofile,
                "tags": tags,
                "question_status": question.question_status,
                "member": getMemberDetails(request, groupID, question.member_id),
                "audioreply_id": question.audioreply_id,
                "audioreply_desc": getAudioDesc2(request, question.audioreply_id),
            }
        )
    return result


def getQuestionDetails(request, groupID, questionID):
    question = (
        request.dbsession.query(Question)
        .filter(Question.question_id == questionID)
        .first()
    )
    return {
        "question_id": question.question_id,
        "member_id": question.member_id,
        "question_dtime": question.question_dtime,
        "question_text": question.question_text,
        "question_audiofile": question.question_audiofile,
        "question_tags": question.question_tags,
        "question_status": question.question_status,
        "member": getMemberDetails(request, groupID, question.member_id),
    }


def getMemberNumber(request, memberID):
    res = request.dbsession.query(Member).filter(Member.member_id == memberID).first()
    return res.member_tele


def updateQuestion(request, questionID, tags, content):
    try:
        request.dbsession.query(Question).filter(
            Question.question_id == questionID
        ).update({"question_text": content, "question_tags": tags})
        return True, ""
    except Exception as e:
        return False, str(e)


def setQuestionStatus(request, questionID, status, replyId):
    try:
        request.dbsession.query(Question).filter(
            Question.question_id == questionID
        ).update({"question_status": status, "audioreply_id": replyId})
        return True, ""
    except Exception as e:
        return False, str(e)


def getSubCounties(request):
    result = []
    counties = request.dbsession.query(County).all()
    for county in counties:
        countyInfo = {"name": county.county_name, "subcounties": []}
        subCounties = request.dbsession.query(Subcounty).filter(
            Subcounty.county_id == county.county_id
        )
        for subCounty in subCounties:
            countyInfo["subcounties"].append(
                {
                    "id": county.county_id + "-" + subCounty.subcounty_id,
                    "name": subCounty.subcounty_name,
                }
            )
        result.append(countyInfo)
    return result


def addGroup(
    request,
    groupName,
    groupTwoWord,
    groupWard,
    groupSName,
    groupCounty,
    groupSubCounty,
    userID,
    menu,
):
    _ = request.translate
    res = (
        request.dbsession.query(Advgroup)
        .filter(Advgroup.group_sname == groupSName)
        .first()
    )
    if res is None:
        uid = str(uuid.uuid4())
        uid = uid[-12:]
        try:
            newGroup = Advgroup(
                group_id=uid,
                group_name=groupName,
                group_ward=groupWard,
                group_twoword=groupTwoWord,
                group_sname=groupSName,
                county_id=groupCounty,
                subcounty_id=groupSubCounty,
                menu_id=menu,
            )
            request.dbsession.add(newGroup)
            newUser = Groupuser(
                group_id=uid, user_id=userID, access_type=2, group_active=0
            )
            request.dbsession.add(newUser)
            return True, uid
        except Exception as e:
            return False, str(e)
    else:
        return False, _("Such group name already exists")


def editGroup(request, groupID, groupName, threeLetters, groupWard, menu):
    request.dbsession.query(Advgroup).filter(Advgroup.group_id == groupID).update(
        {
            "group_name": groupName,
            "group_ward": groupWard,
            "menu_id": menu,
            "group_twoword": threeLetters,
        }
    )


def getGroupDetails(request, groupID):
    res = request.dbsession.query(Advgroup).filter(Advgroup.group_id == groupID).first()
    if res is not None:
        return {
            "group_name": res.group_name,
            "group_sname": res.group_sname,
            "group_ward": res.group_ward,
            "menu_id": res.menu_id,
            "group_twoword": res.group_twoword,
        }
    return {}


def getOneGroup(request, userID):
    res = request.dbsession.query(Groupuser).filter(Groupuser.user_id == userID).first()
    if res is None:
        return None
    else:
        return res.group_id


def deleteGroup(request, groupID):
    try:
        request.dbsession.query(Advgroup).filter(Advgroup.group_id == groupID).delete()
        return True, ""
    except Exception as e:
        return False, str(e)


# -----------------------------------------Users--------------------


def getUsers(request):
    result = []
    sql = (
        "SELECT user.user_id,user.user_name,user.user_telef,user.user_email,user.user_active,"
        "subcounty.subcounty_name,county.county_name "
        "FROM user,subcounty,county "
        "WHERE user.county_id = subcounty.county_id "
        "AND user.subcounty_id = subcounty.subcounty_id "
        "AND subcounty.county_id = county.county_id "
        "AND user.user_admin = false"
    )
    users = request.dbsession.execute(sql).fetchall()
    for user in users:
        result.append(
            {
                "user_id": user.user_id,
                "user_name": user.user_name,
                "user_telef": user.user_telef,
                "user_email": user.user_email,
                "user_active": user.user_active,
                "subcounty_name": user.subcounty_name,
                "county_name": user.county_name,
            }
        )
    return result


def addUser(request, userID, name, telef, email, county, subcounty, password, menu):
    _ = request.translate
    cipher = AESCipher()
    encoded_password = cipher.encrypt(request, password)
    newUser = User(
        user_id=userID,
        user_name=name,
        user_pass=encoded_password,
        user_telef=telef,
        user_active=1,
        user_admin=0,
        user_email=email,
        county_id=county,
        subcounty_id=subcounty,
        menu_id=menu,
    )
    try:
        request.dbsession.add(newUser)
        return True, ""
    except IntegrityError as e:
        return False, request.translate(_("Duplicated user"))
    except:
        return False, sys.exc_info()[0]


def deleteUser(request, userID):
    try:
        request.dbsession.query(User).filter(User.user_id == userID).delete()
        return True, ""
    except Exception as e:
        return False, str(e)


def modifyUser(request, userID, name, telef, email, menu):
    try:
        request.dbsession.query(User).filter(User.user_id == userID).update(
            {
                "user_name": name,
                "user_telef": telef,
                "user_email": email,
                "menu_id": menu,
            }
        )
        return True, ""
    except Exception as e:
        return False, str(e)


def modifyPassword(request, userID, newPassword):
    try:
        cipher = AESCipher()
        encoded_password = cipher.encrypt(request, newPassword)
        request.dbsession.query(User).filter(User.user_id == userID).update(
            {"user_pass": encoded_password}
        )
        return True, ""
    except Exception as e:
        return False, str(e)


def getUserDetails(request, userID):
    user = request.dbsession.query(User).filter(User.user_id == userID).first()
    if user is not None:
        return {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "user_telef": user.user_telef,
            "user_email": user.user_email,
            "menu_id": user.menu_id,
        }
    else:
        return {}


# --------------------------------------Menus-----------------------


def listMenus(request):
    result = []
    menus = request.dbsession.query(Ivrmenu).all()
    for menu in menus:
        result.append({"menu_id": menu.menu_id, "menu_name": menu.menu_name})
    return result


def modifyMenu(request, menuID, name):
    request.dbsession.query(Ivrmenu).filter(Ivrmenu.menu_id == menuID).update(
        {"menu_name": name}
    )
    return True, ""


def getMenuInfo(request, menuID):
    res = request.dbsession.query(Ivrmenu).filter(Ivrmenu.menu_id == menuID).first()
    return {"menu_name": res.menu_name}


def getMenuName(request, menuID):
    res = request.dbsession.query(Ivrmenu).filter(Ivrmenu.menu_id == menuID).first()
    return res.menu_name


def addMenu(request, name):
    uid = str(uuid.uuid4())
    uid = uid[-12:]
    try:
        newMenu = Ivrmenu(menu_id=uid, menu_name=name)
        request.dbsession.add(newMenu)
        return True, ""
    except Exception as e:
        return False, str(e)


def deleteMenu(request, menuID):
    try:
        request.dbsession.query(Ivrmenu).filter(Ivrmenu.menu_id == menuID).delete()
        return True, ""
    except Exception as e:
        return False, str(e)


# -------------------------------------Menu items-------------------------------------


def getAllItems(request, currItem=None):
    result = []
    menus = request.dbsession.query(Ivrmenu).all()
    for menu in menus:
        menuInfo = {"name": menu.menu_name, "mitems": []}
        items = (
            request.dbsession.query(Menuitem)
            .filter(Menuitem.menu_id == menu.menu_id)
            .all()
        )
        for item in items:
            if item.item_id != currItem:
                menuInfo["mitems"].append({"id": item.item_id, "name": item.item_name})
        result.append(menuInfo)
    return result


def getNext(request, itemID):
    item = request.dbsession.query(Menuitem).filter(Menuitem.item_id == itemID).first()
    if item is not None:
        return item.item_name
    else:
        return "None"


def getItemData(request, itemID):
    item = request.dbsession.query(Menuitem).filter(Menuitem.item_id == itemID).first()
    return {
        "item_type": item.item_type,
        "item_name": item.item_name,
        "item_desc": item.item_desc,
        "next_item": item.next_item,
        "audio_id": getItemAudio(request, itemID),
    }


def getItemName(request, itemID):
    item = request.dbsession.query(Menuitem).filter(Menuitem.item_id == itemID).first()
    return item.item_name


# TODO: We need to change this to support multi languages
def getItemAudio(request, itemID):
    res = request.dbsession.query(Menuitem).filter(Menuitem.item_id == itemID).first()
    if res is not None:
        return res.audio_id
    else:
        return None


def listItems(request, menuID):
    result = []
    items = request.dbsession.query(Menuitem).filter(Menuitem.menu_id == menuID).all()
    for item in items:
        result.append(
            {
                "item_id": item.item_id,
                "item_type": item.item_type,
                "item_name": item.item_name,
                "item_desc": item.item_desc,
                "item_start": item.item_start,
                "next_item": getNext(request, item.next_item),
            }
        )
    return result


def addItem(request, menuID, type, name, desc, nextItem, audio):
    uid = str(uuid.uuid4())
    uid = uid[-12:]
    newItem = Menuitem(
        item_id=uid,
        item_type=type,
        item_name=name,
        item_desc=desc,
        next_item=nextItem,
        menu_id=menuID,
        audio_id=audio,
    )
    try:
        request.dbsession.add(newItem)
        return True, ""
    except Exception as e:
        return False, str(e)


# TODO: We need to change this to support multi languages
def modifyItemAudio(request, itemID, audio):
    try:
        request.dbsession.query(Menuitem).filter(Menuitem.item_id == itemID).update(
            {"audio_id": audio}
        )
        return True, ""
    except Exception as e:
        return False, str(e)


def modifyItem(request, itemID, type, name, desc, nextItem, audio):
    try:
        request.dbsession.query(Menuitem).filter(Menuitem.item_id == itemID).update(
            {
                "item_type": type,
                "item_name": name,
                "item_desc": desc,
                "next_item": nextItem,
            }
        )
        modifyItemAudio(request, itemID, audio)
        return True, ""
    except Exception as e:
        return False, str(e)


def setItemAsStart(request, menuID, itemID):
    request.dbsession.query(Menuitem).filter(Menuitem.menu_id == menuID).update(
        {"item_start": 0}
    )
    request.dbsession.query(Menuitem).filter(Menuitem.item_id == itemID).update(
        {"item_start": 1}
    )
    return True, ""


def deleteItem(request, itemID):
    try:
        request.dbsession.query(Menuitem).filter(Menuitem.item_id == itemID).delete()
        return True, ""
    except Exception as e:
        return False, str(e)


# -----------------------------------------------Responses------------------------


def listResponses(request, itemID):
    result = []
    responses = request.dbsession.query(Response).filter(Response.item_id == itemID)
    for resp in responses:
        result.append(
            {
                "resp_num": resp.resp_num,
                "target_item": getNext(request, resp.target_item),
            }
        )
    return result


def addRenponse(request, itemID, number, targetItem):
    try:
        newResponse = Response(item_id=itemID, resp_num=number, target_item=targetItem)
        request.dbsession.add(newResponse)
        return True, ""
    except Exception as e:
        return False, str(e)


def deleteResponse(request, itemID, number):
    try:
        request.dbsession.query(Response).filter(Response.item_id == itemID).filter(
            Response.resp_num == number
        ).delete()
        return True, ""
    except Exception as e:
        return False, str(e)


# -------------------------------------------Audios-----------------------------------


def listAudios(request, group, admin=False):
    if not admin:
        sql = (
            "SELECT user_id FROM groupuser WHERE group_id = '"
            + group
            + "' and user_id <> 'admin'"
        )
        userArray = []
        res = request.dbsession.execute(sql).fetchall()
        for aUser in res:
            userArray.append(aUser.user_id)
        userList = "'" + "','".join(userArray) + "'"
        sql = (
            "SELECT audio_id,audio_desc,audio_dtime,audio_type,user_id FROM audio WHERE user_id IN ("
            + userList
            + ") and audio_type <> 0"
        )
        audios = request.dbsession.execute(sql).fetchall()
    else:
        audios = (
            request.dbsession.query(Audio)
            .filter(Audio.audio_type != 0)
            .order_by(Audio.audio_dtime.desc())
            .all()
        )
    result = []

    for audio in audios:
        userDetails = getUserDetails(request, audio.user_id)
        result.append(
            {
                "audio_id": audio.audio_id,
                "audio_desc": audio.audio_desc,
                "audio_dtime": audio.audio_dtime,
                "audio_type": audio.audio_type,
                "user_id": audio.user_id,
                "user_name": userDetails["user_name"],
            }
        )
    return result


def listPodcasts(request):
    result = []
    audios = (
        request.dbsession.query(Audio)
        .filter(Audio.audio_type == 1)
        .order_by(Audio.audio_dtime.desc())
        .all()
    )
    for audio in audios:
        result.append(
            {
                "audio_id": audio.audio_id,
                "audio_desc": audio.audio_desc,
                "audio_dtime": audio.audio_dtime,
                "audio_type": audio.audio_type,
            }
        )
    return result


def listAnswers(request, userID):
    # Get related groups of the user
    sql = "SELECT group_id FROM groupuser WHERE user_id = '" + userID + "'"
    groupArray = []
    res = request.dbsession.execute(sql).fetchall()
    for aGroup in res:
        groupArray.append(aGroup.group_id)
    groupList = "'" + "','".join(groupArray) + "'"

    # Get releted users of the user (users share same group as user)
    sql = (
        "SELECT distinct user_id FROM groupuser WHERE group_id in ("
        + groupList
        + ") AND user_id <> 'admin'"
    )
    res = request.dbsession.execute(sql).fetchall()
    userArray = []
    for aUser in res:
        userArray.append(aUser.user_id)
    userList = "'" + "','".join(userArray) + "'"

    # get related audios of the user
    sql = (
        "SELECT audio_id,audio_desc,audio_dtime,audio_type FROM audio WHERE user_id IN ("
        + userList
        + ") and audio_type <> 1"
    )
    audios = request.dbsession.execute(sql).fetchall()
    result = []
    for audio in audios:
        result.append(
            {
                "audio_id": audio.audio_id,
                "audio_desc": audio.audio_desc,
                "audio_dtime": audio.audio_dtime,
                "audio_type": audio.audio_type,
            }
        )
    return result


def getAudioDesc(request, audioID):
    res = request.dbsession.query(Audio).filter(Audio.audio_id == audioID).first()
    return res.audio_desc


def getAudioFile(request, audioID):
    res = request.dbsession.query(Audio).filter(Audio.audio_id == audioID).first()
    if res is not None:
        return res.audio_file
    else:
        return None


def addAudio(request, uid, desc, fileName, type, user):
    try:
        newAudio = Audio(
            audio_id=uid,
            audio_desc=desc,
            audio_dtime=datetime.datetime.now(),
            audio_file=fileName,
            audio_type=type,
            user_id=user,
        )
        request.dbsession.add(newAudio)
        return True, ""
    except Exception as e:
        return False, str(e)


def modifyAudio(request, audioID, desc):
    try:
        request.dbsession.query(Audio).filter(Audio.audio_id == audioID).update(
            {"audio_desc": desc}
        )
        return True, ""
    except Exception as e:
        return False, str(e)


def deleteAudio(request, audioID):
    try:
        request.dbsession.query(Audio).filter(Audio.audio_id == audioID).delete()
        return True, ""
    except Exception as e:
        return False, str(e)


# --------------------------------Counties


def getRegions(request):
    result = []
    regions = request.dbsession.query(County).all()
    for region in regions:
        result.append(
            {"county_id": region.county_id, "county_name": region.county_name}
        )
    return result


def addCounty(request, name):
    uid = str(uuid.uuid4())
    uid = uid[-12:]
    try:
        newCounty = County(county_id=uid, county_name=name)
        request.dbsession.add(newCounty)
        return True, ""
    except Exception as e:
        return False, str(e)


def deleteCounty(request, countyID):
    try:
        request.dbsession.query(County).filter(County.county_id == countyID).delete()
    except Exception as e:
        return False, str(e)


def getCountyData(request, countyID):
    res = request.dbsession.query(County).filter(County.county_id == countyID).first()
    return {"county_name": res.county_name}


def updateCounty(request, countyID, name):
    try:
        request.dbsession.query(County).filter(County.county_id == countyID).update(
            {"county_name": name}
        )
        return True, ""
    except Exception as e:
        return False, str(e)


# ---------------------------------Sub county ---------------------------------


def getSubCounties2(request, countyID):
    result = []
    subcs = (
        request.dbsession.query(Subcounty).filter(Subcounty.county_id == countyID).all()
    )
    for subc in subcs:
        result.append(
            {"subcounty_id": subc.subcounty_id, "subcounty_name": subc.subcounty_name}
        )
    return result


def addSubCounty(request, countyID, name):
    uid = str(uuid.uuid4())
    uid = uid[-12:]
    try:
        newSubCounty = Subcounty(
            county_id=countyID, subcounty_id=uid, subcounty_name=name
        )
        request.dbsession.add(newSubCounty)
        return True, ""
    except Exception as e:
        return False, str(e)


def deleteSubCounty(request, countyID, subCountyID):
    try:
        request.dbsession.query(Subcounty).filter(
            Subcounty.county_id == countyID
        ).filter(Subcounty.subcounty_id == subCountyID).delete()
    except Exception as e:
        return False, str(e)


def getSubCountyData(request, countyID, subCountyID):
    res = (
        request.dbsession.query(Subcounty)
        .filter(Subcounty.county_id == countyID)
        .filter(Subcounty.subcounty_id == subCountyID)
        .first()
    )
    return {"subcounty_name": res.subcounty_name}


def getCountyName(request, countyID):
    res = request.dbsession.query(County).filter(County.county_id == countyID).first()
    return res.county_name


def updateSubCounty(request, countyID, subCountyID, name):
    try:
        request.dbsession.query(Subcounty).filter(
            Subcounty.county_id == countyID
        ).filter(Subcounty.subcounty_id == subCountyID).update({"subcounty_name": name})
        return True, ""
    except Exception as e:
        return False, str(e)
