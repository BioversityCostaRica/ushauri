from formencode.variabledecode import variable_decode
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import forget
from pyramid.security import remember
from pyramid.session import check_csrf_token

import ushauri.plugins as p
from ushauri.config.auth import checkLogin
from ushauri.processes import getUserData, register_user
from ushauri.views.classes import publicView


class home_view(publicView):
    def processView(self):
        return {}


class notfound_view(publicView):
    def processView(self):
        self.request.response.status = 404
        return {}


class login_view(publicView):
    def processView(self):
        # If we logged in then go to dashboard
        next = self.request.params.get("next") or self.request.route_url("dashboard")
        if self.request.method == "GET":
            userID = self.request.authenticated_userid
            if userID is not None:
                currentUser = getUserData(self.request, userID)
                if currentUser is not None:
                    return HTTPFound(location=next)
        else:
            safe = check_csrf_token(self.request, raises=False)
            if not safe:
                raise HTTPNotFound()
            data = variable_decode(self.request.POST)
            login = data["login"]
            passwd = data["passwd"]
            user = getUserData(self.request, login)
            if user is not None:
                if checkLogin(login, passwd, self.request):
                    continue_login = True
                    error_message = ""
                    # Load connected plugins and check if they modify the login authorization
                    for plugin in p.PluginImplementations(p.IAuthorize):
                        continue_with_login, error_message = plugin.after_login(
                            self.request, user
                        )
                        if not continue_with_login:
                            self.errors.append(error_message)
                            continue_login = False
                    if continue_login:
                        headers = remember(self.request, login)
                        return HTTPFound(location=next, headers=headers)
                else:
                    self.errors.append(self._("Invalid credentials"))
            else:
                self.errors.append(self._("The user account does not exists"))
        return {"next": next}


def logout_view(request):
    headers = forget(request)
    loc = request.route_url("home")
    return HTTPFound(location=loc, headers=headers)


class register_view(publicView):
    def processView(self):
        # If we logged in then go to dashboard
        if self.request.method == "GET":
            data = {}
        else:
            safe = check_csrf_token(self.request, raises=False)
            if not safe:
                return HTTPNotFound()
            data = variable_decode(self.request.POST)
            if data["user_pass"] != "":
                if data["user_pass"] == data["user_pass2"]:
                    # Load connected plugins and check if they modify the registration of an user
                    continue_registration = True
                    for plugin in p.PluginImplementations(p.IAuthorize):
                        (
                            continue_with_registration,
                            error_message,
                        ) = plugin.before_register(self.request, data)
                        if not continue_with_registration:
                            self.errors.append(error_message)
                            continue_registration = False
                    if continue_registration:
                        added, error_message = register_user(self.request, data)
                        if not added:
                            self.errors.append(error_message)
                        else:
                            # Load connected plugins so they perform actions after the login is performed
                            for plugin in p.PluginImplementations(p.IAuthorize):
                                plugin.after_register(self.request, data)
                            loginData = data["user_id"]
                            headers = remember(self.request, loginData)
                            return HTTPFound(
                                location=self.request.route_url("dashboard"),
                                headers=headers,
                            )
                else:
                    self.errors.append(
                        self._("The password and its retype are not the same")
                    )
            else:
                self.errors.append(self._("The password cannot be empty"))
        return {"next": next, "data": data}
