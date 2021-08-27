import datetime
import uuid

from ushauri.models import Question, User, Member, Response, Menuitem, Audio


def getItemData(request, itemID):
    data = request.dbsession.query(Menuitem).filter(Menuitem.item_id == itemID).first()
    if data is not None:
        return {
            "item_type": data.item_type,
            "item_desc": data.item_desc,
            "next_item": data.next_item,
        }
    else:
        return None


def getItemResponses(request, itemID):
    result = []
    data = request.dbsession.query(Response).filter(Response.item_id == itemID).all()
    if data is not None:
        for aResp in data:
            result.append(
                {
                    "resp_num": aResp.resp_num,
                    "target_item": aResp.target_item,
                    "resp_default": aResp.resp_default,
                }
            )
    return result


def getAudioFileName(request, audioID):
    res = request.dbsession.query(Audio).filter(Audio.audio_id == audioID).first()
    return res.audio_file


def getAudioFile(request, itemID):
    data = request.dbsession.query(Menuitem).filter(Menuitem.item_id == itemID).first()
    if data is not None:
        return {
            "audio_id": data.audio_id,
            "audio_file": getAudioFileName(request, data.audio_id),
        }
    else:
        return None


def storeQuestion(request, groupID, memberID, audioID):
    uid = str(uuid.uuid4())
    uid = uid[-12:]
    newQuestion = Question(
        group_id=groupID,
        member_id=memberID,
        question_id=uid,
        question_dtime=datetime.datetime.now(),
        question_audiofile=audioID,
        question_status=1,
    )
    try:
        request.dbsession.add(newQuestion)
        return True, ""
    except Exception as e:
        return False, str(e)


def isNumberAnAgent(request, number):
    res = request.dbsession.query(User).filter(User.user_telef == number).first()
    if res is not None:
        return res.user_id
    else:
        return None


def getAgentStartItem(request, agetID):
    sql = (
        "SELECT menuitem.item_id "
        "FROM menuitem,ivrmenu,user "
        "WHERE menuitem.menu_id = ivrmenu.menu_id "
        "AND ivrmenu.menu_id = user.menu_id "
        "AND user.user_id = '" + agetID + "' "
        "AND menuitem.item_start = 1"
    )
    res = request.dbsession.execute(sql).fetchone()
    if res is not None:
        return res.item_id
    else:
        return None


def getMemberStartItem(request, memberID):
    sql = (
        "SELECT menuitem.item_id "
        "FROM menuitem,ivrmenu,advgroup,member "
        "WHERE menuitem.menu_id = ivrmenu.menu_id "
        "AND ivrmenu.menu_id = advgroup.menu_id "
        "AND advgroup.group_id = member.group_id "
        "AND member.member_id = '" + memberID + "' "
        "AND menuitem.item_start = 1"
    )
    res = request.dbsession.execute(sql).fetchone()
    if res is not None:
        return res.item_id
    else:
        return None


def isNumberAMember(request, number):
    res = request.dbsession.query(Member).filter(Member.member_tele == number).first()
    if res is None:
        return None
    else:
        return res.member_id


def getMemberAndGroup(request, number):
    res = request.dbsession.query(Member).filter(Member.member_tele == number).first()
    if res is None:
        return None, None
    else:
        return res.group_id, res.member_id
