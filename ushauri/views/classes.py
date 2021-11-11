# -*- coding: utf-8 -*-
"""
    odktools.resources.resources
    ~~~~~~~~~~~~~~~~~~

    Provides the basic view classes for ODKTools and
    the Digest Authorization for ODK

    :copyright: (c) 2017 by QLands Technology Consultants.
    :license: AGPL, see LICENSE for more details.
"""

import hashlib
import uuid

from babel import Locale
from formencode.variabledecode import variable_decode
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.response import Response
from pyramid.security import forget
from pyramid.session import check_csrf_token

# from odktools.odk.processes import getProjectIDFromName,getFormData
from ushauri.config.auth import getUserAccount
from ushauri.processes.db.maintenance import getUserGroups


class odkView(object):
    def __init__(self, request):
        self.request = request
        self._ = self.request.translate
        self.nonce = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()
        self.opaque = request.registry.settings["auth.opaque"]
        self.realm = request.registry.settings["auth.realm"]
        self.authHeader = {}
        self.user = ""

    def getAuthDict(self):
        authheader = self.request.headers["Authorization"].replace(", ", ",")
        authheader = authheader.replace('"', "")
        autharray = authheader.split(",")
        for e in autharray:
            t = e.split("=")
            if len(t) == 2:
                self.authHeader[t[0]] = t[1]
            else:
                self.authHeader[t[0]] = t[1] + "=" + t[2]

    def authorize(self, correctPassword):
        HA1 = ""
        HA2 = ""
        if self.authHeader["qop"] == "auth":
            HA1 = hashlib.md5(
                (self.user + ":" + self.realm + ":" + correctPassword.decode()).encode()
            )
            HA2 = hashlib.md5(
                (self.request.method + ":" + self.authHeader["uri"]).encode()
            )
        if self.authHeader["qop"] == "auth-int":
            HA1 = hashlib.md5(
                (self.user + ":" + self.realm + ":" + correctPassword.decode()).encode()
            )
            MD5Body = hashlib.md5(self.request.body).hexdigest()
            HA2 = hashlib.md5(
                (
                    self.request.method + ":" + self.authHeader["uri"] + ":" + MD5Body
                ).encode()
            )
        if HA1 == "":
            HA1 = hashlib.md5(
                (self.user + ":" + self.realm + ":" + correctPassword).encode()
            )
            HA2 = hashlib.md5(self.request.method + ":" + self.authHeader["uri"])

        authLine = ":".join(
            [
                HA1.hexdigest(),
                self.authHeader["nonce"],
                self.authHeader["nc"],
                self.authHeader["cnonce"],
                self.authHeader["qop"],
                HA2.hexdigest(),
            ]
        )

        resp = hashlib.md5(authLine.encode())
        if resp.hexdigest() == self.authHeader["response"]:
            return True
        else:
            return False

    def askForCredentials(self):
        headers = [
            (
                "WWW-Authenticate",
                'Digest realm="'
                + self.realm
                + '",qop="auth,auth-int",nonce="'
                + self.nonce
                + '",opaque="'
                + self.opaque
                + '"',
            )
        ]
        reponse = Response(status=401, headerlist=headers)
        return reponse

    def createXMLResponse(self, XMLData):
        headers = [
            ("Content-Type", "text/xml; charset=utf-8"),
            ("X-OpenRosa-Accept-Content-Length", "10000000"),
            ("Content-Language", self.request.locale_name),
            ("Vary", "Accept-Language,Cookie,Accept-Encoding"),
            ("X-OpenRosa-Version", "1.0"),
            ("Allow", "GET, HEAD, OPTIONS"),
        ]
        response = Response(headerlist=headers, status=200)

        response.text = str(XMLData, "utf-8")
        return response

    def __call__(self):
        if "Authorization" in self.request.headers:
            if self.request.headers["Authorization"].find("Basic ") == -1:
                self.getAuthDict()
                self.user = self.authHeader["Digest username"]
                return self.processView()
            else:
                headers = [
                    (
                        "WWW-Authenticate",
                        'Digest realm="'
                        + self.realm
                        + '",qop="auth,auth-int",nonce="'
                        + self.nonce
                        + '",opaque="'
                        + self.opaque
                        + '"',
                    )
                ]
                reponse = Response(status=401, headerlist=headers)
                return reponse
        else:
            headers = [
                (
                    "WWW-Authenticate",
                    'Digest realm="'
                    + self.realm
                    + '",qop="auth,auth-int",nonce="'
                    + self.nonce
                    + '",opaque="'
                    + self.opaque
                    + '"',
                )
            ]
            reponse = Response(status=401, headerlist=headers)
            return reponse

    def processView(self):
        # At this point children of odkView have:
        # self.user which us the user requesting ODK data
        # authorize(self,correctPassword) which checks if the password in the authorization is correct
        # askForCredentials(self) which return a response to ask again for the credentials
        # createXMLResponse(self,XMLData) that can be used to return XML data to ODK with the required headers
        return {}


# This is the most basic public view. Used for 404 and 500. But then used for others more advanced classes
class publicView(object):
    def __init__(self, request):
        self.request = request
        self._ = self.request.translate
        self.resultDict = {}
        self.errors = []
        self.justReturn = False
        locale = Locale(request.locale_name)
        if locale.character_order == "left-to-right":
            self.resultDict["rtl"] = False
        else:
            self.resultDict["rtl"] = True

    def __call__(self):
        self.resultDict["errors"] = self.errors
        processDict = self.processView()
        if type(processDict) == dict and not self.justReturn:
            self.resultDict.update(processDict)
            return self.resultDict
        else:
            return processDict

    def processView(self):
        return {}

    def getPostDict(self):
        dct = variable_decode(self.request.POST)
        return dct


class privateView(object):
    def __init__(self, request):
        self.request = request
        self.user = None
        self._ = self.request.translate
        self.errors = []
        self.resultDict = {}
        self.justReturn = False
        locale = Locale(request.locale_name)
        if locale.character_order == "left-to-right":
            self.resultDict["rtl"] = False
        else:
            self.resultDict["rtl"] = True

    def __call__(self):
        currentUser = self.request.authenticated_userid
        if currentUser is not None:
            self.user = getUserAccount(currentUser, self.request)
            if self.user is None:
                headers = forget(self.request)
                return HTTPFound(
                    location=self.request.route_url(
                        "login", _query={"next": self.request.url}
                    ),
                    headers=headers,
                )
        else:
            return HTTPFound(
                location=self.request.route_url(
                    "login", _query={"next": self.request.url}
                )
            )

        if self.request.method == "POST":
            safe = check_csrf_token(self.request, raises=False)
            if not safe:
                raise HTTPNotFound()

        groups = getUserGroups(self.request, self.user.id)
        self.resultDict["groups"] = groups
        self.resultDict["activeUser"] = self.user
        self.resultDict["errors"] = self.errors
        processDict = self.processView()
        if type(processDict) == dict and self.justReturn == False:
            self.resultDict.update(processDict)
            return self.resultDict
        else:
            return processDict

    def processView(self):
        return {"activeuser": self.user}

    def getPostDict(self):
        dct = variable_decode(self.request.POST)
        return dct
