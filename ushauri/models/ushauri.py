# coding: utf-8
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
    Numeric,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Advgroup(Base):
    __tablename__ = "advgroup"
    __table_args__ = (
        ForeignKeyConstraint(
            ["county_id", "subcounty_id"],
            [u"subcounty.county_id", u"subcounty.subcounty_id"],
        ),
        Index("fk_advgroup_subcounty1_idx", "county_id", "subcounty_id"),
    )

    group_id = Column(String(12), primary_key=True)
    group_sname = Column(String(120))
    group_twoword = Column(String(3))
    group_name = Column(String(120))
    group_ward = Column(String(120))
    group_lat = Column(String(80))
    group_long = Column(String(180))
    group_elev = Column(Numeric(11, 3))
    county_id = Column(String(12), nullable=False)
    subcounty_id = Column(String(12), nullable=False)
    menu_id = Column(ForeignKey(u"ivrmenu.menu_id"), index=True)

    county = relationship(u"Subcounty")
    menu = relationship(u"Ivrmenu")


class Answer(Base):
    __tablename__ = "answer"

    group_id = Column(
        ForeignKey(u"advgroup.group_id", ondelete=u"CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    answer_id = Column(String(12), primary_key=True, nullable=False)
    user_id = Column(ForeignKey(u"user.user_id"), nullable=False, index=True)
    answer_text = Column(Text)
    answer_votes = Column(Integer)

    group = relationship(u"Advgroup")
    user = relationship(u"User")


class Answeraudio(Base):
    __tablename__ = "answeraudio"
    __table_args__ = (
        ForeignKeyConstraint(
            ["group_id", "answer_id"],
            [u"answer.group_id", u"answer.answer_id"],
            ondelete=u"CASCADE",
        ),
    )

    group_id = Column(String(12), primary_key=True, nullable=False)
    answer_id = Column(String(12), primary_key=True, nullable=False)
    audio_id = Column(
        ForeignKey(u"audio.audio_id"), primary_key=True, nullable=False, index=True
    )

    audio = relationship(u"Audio")
    group = relationship(u"Answer")


class Audio(Base):
    __tablename__ = "audio"

    audio_id = Column(String(80), primary_key=True)
    audio_desc = Column(String(120))
    audio_file = Column(Text)
    group_id = Column(
        ForeignKey(u"advgroup.group_id", ondelete=u"SET NULL"), index=True
    )
    audio_dtime = Column(DateTime)
    audio_type = Column(Integer)
    user_id = Column(ForeignKey(u"user.user_id"), index=True)

    group = relationship(u"Advgroup")
    groups = relationship(u"Answer", secondary="answeraudio")
    user = relationship(u"User")


class County(Base):
    __tablename__ = "county"

    county_id = Column(String(12), primary_key=True)
    county_name = Column(String(120))


class Groupuser(Base):
    __tablename__ = "groupuser"

    group_id = Column(
        ForeignKey(u"advgroup.group_id", ondelete=u"CASCADE"),
        primary_key=True,
        nullable=False,
    )
    user_id = Column(
        ForeignKey(u"user.user_id", ondelete=u"CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    access_type = Column(Integer)
    group_active = Column(Integer)

    group = relationship(u"Advgroup")
    user = relationship(u"User")


# class Itemaudio(Base):
#     __tablename__ = 'itemaudio'
#
#     item_id = Column(ForeignKey(u'menuitem.item_id', ondelete=u'CASCADE'), primary_key=True, nullable=False)
#     language_code = Column(ForeignKey(u'language.language_code'), primary_key=True, nullable=False, index=True)
#     audio_id = Column(ForeignKey(u'audio.audio_id'), nullable=False, index=True)
#
#     audio = relationship(u'Audio')
#     item = relationship(u'Menuitem')
#     language = relationship(u'Language')


class Itemaudio(Base):
    __tablename__ = "itemaudio"

    item_id = Column(
        ForeignKey(u"menuitem.item_id", ondelete=u"CASCADE"),
        primary_key=True,
        nullable=False,
    )
    language_code = Column(
        ForeignKey(u"language.language_code"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    audio_id = Column(ForeignKey(u"audio.audio_id"), nullable=False, index=True)

    audio = relationship(u"Audio")
    item = relationship(u"Menuitem")
    language = relationship(u"Language")


# class Ivrlog(Base):
#     __tablename__ = 'ivrlog'
#     __table_args__ = (
#         ForeignKeyConstraint(['group_id', 'member_id'], [u'member.group_id', u'member.member_id']),
#         Index('fk_ivrlog_member1_idx', 'group_id', 'member_id')
#     )
#
#     log_id = Column(String(80), primary_key=True)
#     log_dtime = Column(DateTime)
#     group_id = Column(String(12), nullable=False)
#     member_id = Column(String(45), nullable=False)
#     item_id = Column(ForeignKey(u'menuitem.item_id'), nullable=False, index=True)
#
#     group = relationship(u'Member')
#     item = relationship(u'Menuitem')


class Ivrlog(Base):
    __tablename__ = "ivrlog"
    __table_args__ = (
        ForeignKeyConstraint(
            ["group_id", "member_id"], [u"member.group_id", u"member.member_id"]
        ),
        Index("fk_ivrlog_member1_idx", "group_id", "member_id"),
    )

    log_id = Column(String(80), primary_key=True)
    log_dtime = Column(DateTime)
    group_id = Column(String(12), nullable=False)
    member_id = Column(String(45), nullable=False)
    item_id = Column(ForeignKey(u"menuitem.item_id"), nullable=False, index=True)

    group = relationship(u"Member")
    item = relationship(u"Menuitem")


class Ivrmenu(Base):
    __tablename__ = "ivrmenu"

    menu_id = Column(String(12), primary_key=True)
    menu_name = Column(String(45))


# class Ivrmenu(Base):
#     __tablename__ = 'ivrmenu'
#
#     group_id = Column(ForeignKey(u'advgroup.group_id', ondelete=u'CASCADE'), primary_key=True, nullable=False)
#     menu_id = Column(String(12), primary_key=True, nullable=False)
#     menu_name = Column(String(45))
#     menu_current = Column(Integer)
#     menu_agentcurrent = Column(Integer)
#
#     group = relationship(u'Advgroup')


class Language(Base):
    __tablename__ = "language"

    language_code = Column(String(4), primary_key=True)
    language_name = Column(String(120))
    audio_id = Column(ForeignKey(u"audio.audio_id"), nullable=False, index=True)

    audio = relationship(u"Audio")


class Member(Base):
    __tablename__ = "member"

    group_id = Column(
        ForeignKey(u"advgroup.group_id", ondelete=u"CASCADE"),
        primary_key=True,
        nullable=False,
    )
    member_id = Column(String(45), primary_key=True, nullable=False)
    member_name = Column(String(120))
    member_tele = Column(String(45))
    member_gender = Column(Integer)
    member_village = Column(String(120))
    member_gardentype = Column(String(32))

    group = relationship(u"Advgroup")


# class Menuitem(Base):
#     __tablename__ = 'menuitem'
#     __table_args__ = (
#         ForeignKeyConstraint(['group_id', 'menu_id'], [u'ivrmenu.group_id', u'ivrmenu.menu_id'], ondelete=u'CASCADE'),
#         Index('fk_menuitem_ivrmenu1_idx', 'group_id', 'menu_id')
#     )
#
#     item_id = Column(String(12), primary_key=True)
#     item_type = Column(Integer)
#     item_desc = Column(Text)
#     item_pos = Column(Integer)
#     group_id = Column(String(12), nullable=False)
#     menu_id = Column(String(12), nullable=False)
#     next_item = Column(ForeignKey(u'menuitem.item_id'), index=True)
#
#     group = relationship(u'Ivrmenu')
#     parent = relationship(u'Menuitem', remote_side=[item_id])


class Menuitem(Base):
    __tablename__ = "menuitem"

    item_id = Column(String(12), primary_key=True)
    item_type = Column(Integer)
    item_name = Column(String(120))
    item_desc = Column(Text)
    item_start = Column(Integer)
    next_item = Column(ForeignKey(u"menuitem.item_id"), index=True)
    menu_id = Column(
        ForeignKey(u"ivrmenu.menu_id", ondelete=u"CASCADE"), nullable=False, index=True
    )

    menu = relationship(u"Ivrmenu")
    parent = relationship(u"Menuitem", remote_side=[item_id])


# class Menuwelcome(Base):
#     __tablename__ = 'menuwelcome'
#     __table_args__ = (
#         ForeignKeyConstraint(['group_id', 'menu_id'], [u'ivrmenu.group_id', u'ivrmenu.menu_id'], ondelete=u'CASCADE'),
#     )
#
#     group_id = Column(String(12), primary_key=True, nullable=False)
#     menu_id = Column(String(12), primary_key=True, nullable=False)
#     language_code = Column(ForeignKey(u'language.language_code'), primary_key=True, nullable=False, index=True)
#     audio_id = Column(ForeignKey(u'audio.audio_id'), nullable=False, index=True)
#
#     audio = relationship(u'Audio')
#     group = relationship(u'Ivrmenu')
#     language = relationship(u'Language')


class Menuwelcome(Base):
    __tablename__ = "menuwelcome"

    menu_id = Column(
        ForeignKey(u"ivrmenu.menu_id", ondelete=u"CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    language_code = Column(
        ForeignKey(u"language.language_code"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    audio_id = Column(ForeignKey(u"audio.audio_id"), nullable=False, index=True)

    audio = relationship(u"Audio")
    language = relationship(u"Language")
    menu = relationship(u"Ivrmenu")


class Question(Base):
    __tablename__ = "question"
    __table_args__ = (
        ForeignKeyConstraint(
            ["group_id", "member_id"],
            [u"member.group_id", u"member.member_id"],
            ondelete=u"CASCADE",
        ),
    )

    group_id = Column(String(12), primary_key=True, nullable=False)
    member_id = Column(String(45), primary_key=True, nullable=False)
    question_id = Column(String(12), primary_key=True, nullable=False)
    question_dtime = Column(DateTime)
    question_audiofile = Column(Text)
    question_text = Column(Text)
    question_tags = Column(Text)
    question_status = Column(Integer)
    audioreply_id = Column(ForeignKey(u"audio.audio_id"), index=True)

    audio = relationship(u"Audio")

    group = relationship(u"Member")


class Questionanswer(Base):
    __tablename__ = "questionanswer"
    __table_args__ = (
        ForeignKeyConstraint(
            ["answer_group", "answer_id"],
            [u"answer.group_id", u"answer.answer_id"],
            ondelete=u"CASCADE",
        ),
        ForeignKeyConstraint(
            ["group_id", "member_id", "question_id"],
            [u"question.group_id", u"question.member_id", u"question.question_id"],
            ondelete=u"CASCADE",
        ),
        Index("fk_questionanswer_answer1_idx", "answer_group", "answer_id"),
    )

    group_id = Column(String(12), primary_key=True, nullable=False)
    member_id = Column(String(45), primary_key=True, nullable=False)
    question_id = Column(String(12), primary_key=True, nullable=False)
    answer_group = Column(String(12), primary_key=True, nullable=False)
    answer_id = Column(String(12), primary_key=True, nullable=False)
    answer_sent = Column(Integer)

    answer = relationship(u"Answer")
    group = relationship(u"Question")


class Questiontag(Base):
    __tablename__ = "questiontag"
    __table_args__ = (
        ForeignKeyConstraint(
            ["group_id", "member_id", "question_id"],
            [u"question.group_id", u"question.member_id", u"question.question_id"],
            ondelete=u"CASCADE",
        ),
    )

    group_id = Column(String(12), primary_key=True, nullable=False)
    member_id = Column(String(45), primary_key=True, nullable=False)
    question_id = Column(String(12), primary_key=True, nullable=False)
    tag_name = Column(String(120), primary_key=True, nullable=False)

    group = relationship(u"Question")


# class Response(Base):
#     __tablename__ = 'response'
#
#     item_id = Column(ForeignKey(u'menuitem.item_id', ondelete=u'CASCADE'), primary_key=True, nullable=False)
#     resp_num = Column(Integer, primary_key=True, nullable=False)
#     target_item = Column(ForeignKey(u'menuitem.item_id'), nullable=False, index=True)
#     resp_default = Column(Integer)
#
#     item = relationship(u'Menuitem', primaryjoin='Response.item_id == Menuitem.item_id')
#     menuitem = relationship(u'Menuitem', primaryjoin='Response.target_item == Menuitem.item_id')


class Response(Base):
    __tablename__ = "response"

    item_id = Column(
        ForeignKey(u"menuitem.item_id", ondelete=u"CASCADE"),
        primary_key=True,
        nullable=False,
    )
    resp_num = Column(Integer, primary_key=True, nullable=False)
    target_item = Column(ForeignKey(u"menuitem.item_id"), nullable=False, index=True)
    resp_default = Column(Integer)

    item = relationship(u"Menuitem", primaryjoin="Response.item_id == Menuitem.item_id")
    menuitem = relationship(
        u"Menuitem", primaryjoin="Response.target_item == Menuitem.item_id"
    )


class Subcounty(Base):
    __tablename__ = "subcounty"

    county_id = Column(
        ForeignKey(u"county.county_id", ondelete=u"CASCADE"),
        primary_key=True,
        nullable=False,
    )
    subcounty_id = Column(String(12), primary_key=True, nullable=False)
    subcounty_name = Column(String(120))

    county = relationship(u"County")


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        ForeignKeyConstraint(
            ["county_id", "subcounty_id"],
            [u"subcounty.county_id", u"subcounty.subcounty_id"],
        ),
        Index("fk_user_subcounty1_idx", "county_id", "subcounty_id"),
    )

    user_id = Column(String(120), primary_key=True)
    user_name = Column(String(45))
    user_pass = Column(String(120))
    user_telef = Column(String(120))
    user_active = Column(Integer)
    user_admin = Column(Integer)
    user_email = Column(Text)
    county_id = Column(String(12))
    subcounty_id = Column(String(12))
    menu_id = Column(ForeignKey(u"ivrmenu.menu_id"), index=True)

    county = relationship(u"Subcounty")
    menu = relationship(u"Ivrmenu")
