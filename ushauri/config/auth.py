import hashlib
import urllib

from ushauri.config.encdecdata import AESCipher
from ushauri.models import User
from ushauri.processes import getUserPassword, isUserActive, getUserData


class AUser(object):
    def __init__(self, userID, userName, userAdmin, email):
        self.id = userID
        self.name = userName
        if userAdmin == 1:
            self.admin = True
        else:
            self.admin = False
        self.email = email

        default = "identicon"
        size = 45
        gravatar_url = (
            "http://www.gravatar.com/avatar/"
            + hashlib.md5(self.email.lower().encode("utf8")).hexdigest()
            + "?"
        )
        gravatar_url += urllib.parse.urlencode({"d": default, "s": str(size)})

        self.gravatarURL = gravatar_url

    def check_password(self, password, request):
        return checkLogin(self.id, password, request)

    def getGravatarUrl(self, size):
        default = "identicon"
        gravatar_url = (
            "http://www.gravatar.com/avatar/"
            + hashlib.md5(self.email.lower()).hexdigest()
            + "?"
        )
        gravatar_url += urllib.parse.urlencode({"d": default, "s": str(size)})
        return gravatar_url

    def updateGravatarURL(self):
        default = "identicon"
        size = 45
        gravatar_url = (
            "http://www.gravatar.com/avatar/"
            + hashlib.md5(self.email.lower()).hexdigest()
            + "?"
        )
        gravatar_url += urllib.parse.urlencode({"d": default, "s": str(size)})
        self.gravatarURL = gravatar_url


def getUserAccount(userID, request):
    if isUserActive(request, userID):
        userData = getUserData(request, userID)
        return AUser(userID, userData["name"], userData["admin"], userData["email"])
    return None


def checkLogin(userID, password, request):
    currentPass = getUserPassword(request, userID)
    if currentPass is not None:
        if currentPass.decode() == password:
            return True
        else:
            return False
    else:
        return False


def changePassword(userID, password, request):
    cipher = AESCipher()
    encoded_password = cipher.encrypt(request, password)
    request.dbsession.query(User).filter(User.user_id == userID).update(
        {"user_pass": encoded_password}
    )
