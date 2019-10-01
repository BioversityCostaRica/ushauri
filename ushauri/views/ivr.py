from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client
from pyramid.response import Response, FileResponse
from ushauri.processes import (
    getItemData,
    getItemResponses,
    getAudioFile,
    storeQuestion,
    isNumberAnAgent,
    isNumberAMember,
    getAgentStartItem,
    getMemberStartItem,
    getMemberAndGroup,
    getAudioFileName,
    recordLog,
)
import uuid, os, arrow
from datetime import datetime, timedelta
from urllib.request import urlretrieve
from ushauri.processes.db.maintenance import getUserDetails, addAudio, setQuestionStatus


import logging

log = logging.getLogger(__name__)


def twiml(resp):
    headers = [("Content-Type", "text/xml; charset=utf-8")]
    resp = Response(body=str(resp), headerlist=headers)
    return resp


def sendReply(request, number, audioID, questionID):
    account_sid = request.registry.settings["account_sid"]
    auth_token = request.registry.settings["auth_token"]
    client = Client(account_sid, auth_token)
    # print("*************************R33")
    # print(number)
    # print("-----------------------")
    # print(audioID)
    # print("*************************R33")
    call = client.calls.create(
        to=number,
        from_=request.registry.settings["call_from"],
        url=request.route_url("sendreply", audioid=audioID),
        method="GET",
        status_callback=request.route_url(
            "replystatus", questionid=questionID, audioid=audioID
        ),
    )


def ivrSend_view(request):
    audioID = request.matchdict["audioid"]
    response = VoiceResponse()
    response.play(
        request.url_for_static("static/audio/" + getAudioFileName(request, audioID)),
        loop=0,
    )
    response.hangup()
    return twiml(response)


def ivrReplyStatus_view(request):
    if request.method == "POST":
        questionID = request.matchdict["questionid"]
        audioID = request.matchdict["audioid"]
        print("************************A99")
        print(request.POST)
        classStatus = request.POST.get("CallStatus", "failed")
        if classStatus == "completed":
            setQuestionStatus(request, questionID, 3, audioID)
        else:
            setQuestionStatus(request, questionID, -1, audioID)
        print("************************A99")
    resp = Response()
    return resp


def ivrVoiceStart_view(request):
    number = request.params["From"]
    # If the number is malformed like +792490972 then remove the + and add +255
    if number[:4] != "+255":
        print("*****************90")
        print("Fixing" + number)
        print("--------------------------")
        print(request.params)
        print("-------------------------")
        number = "+255" + number[2:]
        print(number)
        print("*****************90")

    agent = isNumberAnAgent(request, number)
    # agent = None #Only for Skype test. Remove soon

    if agent is not None:
        menuItem = getAgentStartItem(request, agent)
        if menuItem is not None:
            response = VoiceResponse()
            response.redirect(
                request.route_url("ivrget", itemid=menuItem), method="GET"
            )
            return twiml(response)
        else:
            resp = VoiceResponse()
            resp.say("Sorry your account does not have a active menu")
            resp.hangup()
            return twiml(resp)
    else:
        member = isNumberAMember(request, number)

        # member = "ce8576be358a" #Only for Skype test. Remove soon

        if member is not None:
            menuItem = getMemberStartItem(request, member)
            if menuItem is not None:
                response = VoiceResponse()
                response.redirect(
                    request.route_url("ivrget", itemid=menuItem), method="GET"
                )
                # print("*****************13")
                # print(str(response))
                # print("*****************13")
                return twiml(response)
            else:
                resp = VoiceResponse()
                resp.say("Sorry your account does not have a active menu")
                resp.hangup()
                return twiml(resp)
        else:
            resp = VoiceResponse()
            resp.say(
                "Contact your extension agent so he/she register you for this service"
            )
            resp.hangup()
            return twiml(resp)


def ivrMessage_view(request):
    number = request.params["From"]
    # If the number is malformed like +792490972 then remove the + and add +255
    if number[:4] != "+255":
        print("*****************91")
        print("Fixing" + number)
        print("------------------------")
        print(request.params)
        print("*****************91")
        number = "+255" + number[2:]
    agent = isNumberAnAgent(request, number)
    if agent is not None:
        menuItem = getAgentStartItem(request, agent)
        if menuItem is not None:
            response = MessagingResponse()
            message = Message()
            message.body("Hello Extension Agent! We will call you soon")
            response.append(message)

            account_sid = request.registry.settings["account_sid"]
            auth_token = request.registry.settings["auth_token"]
            client = Client(account_sid, auth_token)

            call = client.calls.create(
                to=number,
                from_=request.registry.settings["call_from"],
                url=request.route_url("ivrget", itemid=menuItem),
                method="GET",
            )
            return twiml(response)
        else:
            response = MessagingResponse()
            message = Message()
            message.body("Sorry your account does not have a active menu")
            response.append(message)
            return twiml(response)
    else:
        member = isNumberAMember(request, number)
        if member is not None:
            menuItem = getMemberStartItem(request, member)
            if menuItem is not None:
                response = MessagingResponse()
                message = Message()
                message.body("Hello Member! We will call you soon")
                response.append(message)

                account_sid = request.registry.settings["account_sid"]
                auth_token = request.registry.settings["auth_token"]
                client = Client(account_sid, auth_token)

                call = client.calls.create(
                    to=number,
                    from_=request.registry.settings["call_from"],
                    url=request.route_url("ivrget", itemid=menuItem),
                    method="GET",
                )

                return twiml(response)
            else:
                response = MessagingResponse()
                message = Message()
                message.body("Sorry your account does not have a active menu")
                response.append(message)
                return twiml(response)
        else:
            response = MessagingResponse()
            message = Message()
            message.body(
                "Contact your extension agent so he/she register you for this service"
            )
            response.append(message)
            return twiml(response)


def ivrGet_view(request):
    itemID = request.matchdict["itemid"]
    itemData = getItemData(request, itemID)
    number = request.params["From"]
    # If the number is malformed like +792490972 then remove the + and add +255
    if number[:4] != "+255":
        print("*****************92")
        print("Fixing" + number)
        print("----------------------------")
        print(request.params)
        print("-------------------")
        number = "+255" + number[2:]
        print(number)
        print("*****************92")

    # number = "+50662365878" # Only for Skype

    recordLog(request, number, itemID)
    if itemData is not None:
        if request.method == "GET":
            if itemData["item_type"] == 1:
                response = VoiceResponse()
                audioData = getAudioFile(request, itemID, "en")
                if audioData is None:
                    with response.gather(
                        numDigits=1,
                        action=request.route_url("ivrpost", itemid=itemID),
                        method="POST",
                    ) as g:
                        g.say(
                            itemData["item_desc"],
                            voice="alice",
                            language="en-GB",
                            loop=3,
                        )
                else:
                    with response.gather(
                        numDigits=1,
                        action=request.route_url("ivrpost", itemid=itemID),
                        method="POST",
                    ) as g:
                        g.play(
                            request.url_for_static(
                                "static/audio/" + audioData["audio_file"]
                            ),
                            loop=3,
                        )
                # print("*****************14")
                # print(str(response))
                # print("*****************14")
                return twiml(response)

            if itemData["item_type"] == 2:
                resp = VoiceResponse()
                audioData = getAudioFile(request, itemID, "en")
                if audioData is None:
                    resp.say("Record your message after the tone.")
                else:
                    resp.play(
                        request.url_for_static(
                            "static/audio/" + audioData["audio_file"]
                        ),
                        loop=1,
                    )
                resp.record(
                    maxLength=60,
                    action=request.route_url("ivrstore", itemid=itemID),
                    method="POST",
                    finish_on_key="*",
                )
                resp.hangup()
                # print("*****************15")
                # print(str(resp))
                # print("*****************15")
                return twiml(resp)
            if itemData["item_type"] == 3:
                audioData = getAudioFile(request, itemID, "en")
                response = VoiceResponse()
                response.play(
                    request.url_for_static("static/audio/" + audioData["audio_file"]),
                    loop=1,
                )
                if itemData["next_item"] is not None:
                    response.redirect(
                        request.route_url("ivrget", itemid=itemData["next_item"]),
                        method="GET",
                    )
                    # print("*****************16")
                    # print(str(response))
                    # print("*****************16")
                    return twiml(response)
                else:
                    response.hangup()
                    # print("*****************17")
                    # print(str(response))
                    # print("*****************17")
                    return twiml(response)
        else:
            resp = VoiceResponse()
            resp.say("Error, you are in the get url but in a post call")
            resp.hangup()
            return twiml(resp)
    else:
        resp = VoiceResponse()
        resp.say("Invalid item")
        resp.hangup()
        return twiml(resp)


def ivrPost_view(request):
    itemID = request.matchdict["itemid"]
    itemData = getItemData(request, itemID)
    if itemData is not None:
        itemResponses = getItemResponses(request, itemID)
        if request.method == "POST":
            soption = request.POST.get("Digits", "0")
            noption = 0
            try:
                noption = int(soption)
            except:
                resp = VoiceResponse()
                resp.say(
                    "Sorry, you did not typed a number. Redirecting you to the main menu"
                )
                resp.redirect("https://ushauri.info/kenya/start", method="GET")
                return twiml(resp)
            for resp in itemResponses:
                if resp["resp_num"] == noption:
                    response = VoiceResponse()
                    response.redirect(
                        request.route_url("ivrget", itemid=resp["target_item"]),
                        method="GET",
                    )
                    return twiml(response)
            resp = VoiceResponse()
            resp.say("Error, was not able to find a response")
            resp.hangup()
            return twiml(resp)
        else:
            resp = VoiceResponse()
            resp.say("Error, you are in the post url but in a get call")
            resp.hangup()
            return twiml(resp)
    else:
        resp = VoiceResponse()
        resp.say("Invalid item")
        resp.hangup()
        return twiml(resp)


def ivrStore_view(request):
    if request.method == "POST":
        recording_url = request.POST.get("RecordingUrl", None)
        if recording_url is not None:
            uid = str(uuid.uuid4())
            number = request.POST.get(
                "From", ""
            )  # We assume here that the platform made the call. Change to From
            # If the number is malformed like +792490972 then remove the + and add +255
            if number[:4] != "+255":
                print("*****************93")
                print("Fixing" + number)
                print("---------------------")
                number = "+255" + number[2:]
                print(number)
                print("*****************93")
            agent = isNumberAnAgent(request, number)

            # agent = None #Only for Skype test. Remove soon

            if agent is not None:
                data = getUserDetails(request, agent)
                path = os.path.join(
                    request.registry.settings["audioPath"], *[uid + ".wav"]
                )
                urlretrieve(recording_url, path)
                ar = arrow.get(datetime.now() + timedelta(hours=3))  # Nairobi time
                addAudio(
                    request,
                    uid,
                    "Audio recorded by agent "
                    + data["user_name"]
                    + " the "
                    + ar.format("Do of MMMM, YYYY - HH:mm:ss"),
                    uid + ".wav",
                    2,
                    data["user_id"],
                )
            else:
                group, member = getMemberAndGroup(request, number)

                # group = "35f59a27debc" # Only for Skype test. Remove soon
                # member = "ce8576be358a" # Only for Skype test. Remove soon

                path = os.path.join(
                    request.registry.settings["repository"], *[uid + ".wav"]
                )
                urlretrieve(recording_url, path)
                storeQuestion(request, group, member, uid)
            resp = VoiceResponse()
            resp.hangup()
            return twiml(resp)
        else:
            resp = VoiceResponse()
            resp.hangup()
            return twiml(resp)
    else:
        resp = VoiceResponse()
        resp.hangup()
        return twiml(resp)


def ivrGetAudio_view(request):
    itemID = request.matchdict["audioid"]
    response = FileResponse(
        os.path.join(request.registry.settings["repository"], *[itemID + ".wav"]),
        request=request,
        content_type="audio/wav",
    )
    return response
