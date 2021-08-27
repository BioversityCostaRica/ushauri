# -*- coding: utf-8 -*-
"""
    formshare.config.mainresources
    ~~~~~~~~~~~~~~~~~~

    Provides the main JS and CSS resources to FormShare.

    :copyright: (c) 2017 by QLands Technology Consultants.
    :license: AGPL, see LICENSE for more details.
"""

import os

import ushauri.resources as r


def createResources(apppath, config):

    # ----------------Landing page--------------------
    # Add core resource library
    r.addLibrary("landing", os.path.join(apppath, "jsandcss/landing"), config)
    # Add core CSS and JS
    r.addCSSResource("landing", "bootstrap", "css/bootstrap.min.css")
    r.addCSSResource("landing", "animate", "css/animate.min.css")
    r.addCSSResource("landing", "font-awesome", "font-awesome/css/font-awesome.min.css")
    r.addCSSResource("landing", "style", "css/style.css")

    r.addJSResource("landing", "jquery", "js/jquery-2.1.1.js")
    r.addJSResource("landing", "pace", "js/pace.min.js")
    r.addJSResource("landing", "bootstrap", "js/bootstrap.min.js")
    r.addJSResource("landing", "classie", "js/classie.js")
    r.addJSResource("landing", "animate-header", "js/cbpAnimatedHeader.js")
    r.addJSResource("landing", "wow", "js/wow.min.js")
    r.addJSResource("landing", "inspinia", "js/inspinia.js")

    r.addLibrary("dashboard", os.path.join(apppath, "jsandcss/dashboard"), config)

    r.addCSSResource("dashboard", "bootstrap", "css/bootstrap.min.css")
    r.addCSSResource("dashboard", "font-awesome", "font-awesome/css/font-awesome.css")
    r.addCSSResource("dashboard", "animate", "css/animate.css")
    r.addCSSResource("dashboard", "style", "css/style.css")
    r.addCSSResource("dashboard", "toastr", "css/plugins/toastr/toastr.min.css", None)
    r.addCSSResource(
        "dashboard",
        "rtl",
        "css/plugins/bootstrap-rtl/bootstrap-rtl.min.css",
        "bootstrap",
    )
    r.addCSSResource(
        "dashboard", "select2", "css/plugins/select2/select2.min.css", "style"
    )

    r.addJSResource("dashboard", "jquery", "js/jquery-3.1.1.min.js")
    r.addJSResource("dashboard", "bootstrap", "js/bootstrap.min.js")
    r.addJSResource(
        "dashboard", "metismenu", "js/plugins/metisMenu/jquery.metisMenu.js"
    )
    r.addJSResource(
        "dashboard", "slimscroll", "js/plugins/slimscroll/jquery.slimscroll.min.js"
    )
    r.addJSResource("dashboard", "inspinia", "js/inspinia.js")
    r.addJSResource("dashboard", "pace", "js/plugins/pace/pace.min.js")
    r.addJSResource("dashboard", "toastr", "js/plugins/toastr/toastr.min.js")
    r.addJSResource("dashboard", "modal", "modal.js", "pace")
    r.addJSResource(
        "dashboard", "select2", "js/plugins/select2/select2.full.min.js", "pace"
    )
    r.addJSResource("dashboard", "confirm", "confirm.js", "pace")
    r.addJSResource("dashboard", "howler", "js/plugins/howler/howler.min.js", "pace")

    r.addJSResource(
        "dashboard", "jrecord_display", "js/plugins/jrecord/audiodisplay.js", None
    )
    r.addJSResource(
        "dashboard",
        "jrecord_recorder",
        "js/plugins/jrecord/recorder.js",
        "jrecord_display",
    )
    r.addJSResource(
        "dashboard", "jrecord_main", "js/plugins/jrecord/main.js", "jrecord_recorder"
    )
    r.addJSResource(
        "dashboard", "jrecord_worker", "js/plugins/jrecord/recorderWorker.js", None
    )
