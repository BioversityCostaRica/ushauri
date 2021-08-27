import json
import uuid

from ushauri.config.encdecdata import AESCipher
from ushauri.models import User, Groupuser, Advgroup, Member


def isUserActive(request, userID):
    user = request.dbsession.query(User).filter(User.user_id == userID).first()
    if user is not None:
        if user.user_active == 1:
            return True
        else:
            return False
    else:
        return False


def getUserPassword(request, userID):
    user = request.dbsession.query(User).filter(User.user_id == userID).first()
    encodedPass = user.user_pass.encode()
    cipher = AESCipher()
    decrypted = cipher.decrypt(request, encodedPass)
    return decrypted


def userCanRegister(request, groupID, userID):
    permisions = (
        request.dbsession.query(Groupuser)
        .filter(Groupuser.group_id == groupID)
        .filter(Groupuser.user_id == userID)
        .all()
    )
    for permision in permisions:
        if permision.access_type == 2:
            return True
    return False


def getGroupIDFromName(request, groupName):
    group = (
        request.dbsession.query(Advgroup)
        .filter(Advgroup.group_sname == groupName)
        .first()
    )
    if group is not None:
        return group.group_id
    else:
        return None


def storeRegistration(request, JSONFile, groupID):
    try:
        uid = str(uuid.uuid4())
        uid = uid[-12:]
        data = json.load(open(JSONFile))
        tele = data["grpaitechinfo/mobile"]
        country_code = request.registry.settings["country.code"]
        if tele[: len(country_code)] != country_code:
            if tele[:1] == "0":
                tele = country_code + tele[1:]

        newMember = Member(
            group_id=groupID,
            member_id=uid,
            member_name=data["grpaitechinfo/name"],
            member_tele=tele,
            member_gender=data["grpaitechinfo/gender"],
            member_village=data["grpaitechinfo/village"],
            member_gardentype=data["grpaitechinfo/gardentype"],
        )

        request.dbsession.add(newMember)
        return True, ""
    except Exception as e:
        return False, str(e)
