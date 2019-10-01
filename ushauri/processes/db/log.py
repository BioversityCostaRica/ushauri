from ushauri.models import Ivrlog, Member
import uuid, datetime


def recordLog(request, number, item):
    res = request.dbsession.query(Member).filter(Member.member_tele == number).first()
    if res is not None:
        uid = str(uuid.uuid4())
        newLog = Ivrlog(
            log_id=uid,
            log_dtime=datetime.datetime.now(),
            group_id=res.group_id,
            member_id=res.member_id,
            item_id=item,
        )
        try:
            request.dbsession.add(newLog)
            return True, ""
        except Exception as e:
            return False, str(e)
