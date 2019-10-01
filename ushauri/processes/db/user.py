from ushauri.config.encdecdata import AESCipher
from ushauri.models import User
from ushauri.models.schema import mapToSchema
from sqlalchemy.exc import IntegrityError
import logging, sys

log = logging.getLogger(__name__)


def getUserPassword(request, userID):
    user = request.dbsession.query(User).filter(User.user_id == userID).first()
    if user is not None:
        encodedPass = user.user_pass.encode()
        cipher = AESCipher(key=request.registry.settings["aes.key"])
        decrypted = cipher.decrypt(encodedPass)
        return decrypted
    else:
        return None


def isUserActive(request, userID):
    user = request.dbsession.query(User).filter(User.user_id == userID).first()
    if user is not None:
        if user.user_active == 1:
            return True
        else:
            return False
    else:
        return False


def getUserData(request, userID):
    user = request.dbsession.query(User).filter(User.user_id == userID).first()
    if user is not None:
        return {
            "name": user.user_name,
            "admin": user.user_admin,
            "email": user.user_email,
        }
    else:
        return None


def register_user(request, userData):
    userData.pop("user_pass2", None)
    userData["user_active"] = 1
    userData["user_admin"] = 0
    mappedData = mapToSchema(User, userData)
    cipher = AESCipher(key=request.registry.settings["aes.key"])
    encPass = cipher.encrypt(mappedData["user_pass"])
    mappedData["user_pass"] = encPass
    newUser = User(**mappedData)
    try:
        request.dbsession.add(newUser)
        return True, ""
    except IntegrityError as e:
        log.error("Duplicated user {}".format(mappedData["user_id"]))
        return False, request.translate("Duplicated user")
    except:
        log.error(
            "Error {} when inserting user user {}".format(
                sys.exc_info()[0], mappedData["user_id"]
            )
        )
        return False, sys.exc_info()[0]


def getUserGroups(request, userID):
    sql = (
        "SELECT advgroup.group_id,advgroup.group_name "
        "FROM advgroup,groupuser "
        "WHERE groupuser.group_id = advgroup.group_id "
        "AND groupuser.user_id = '" + userID + "'"
    )
    result = []
    groups = request.dbsession.execute(sql).fetchall()
    for group in groups:
        result.append({"group": group.group_id, "name": group.group_name})
    return result
