from datetime import datetime, timedelta
import enum

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property

from globals import db


class TicketTypeEnum(enum.Enum):
    vip = 0
    premium = 1
    regular = 2


def ticket_type_str_to_enum(ticket_type: str) -> TicketTypeEnum:
    if ticket_type == 'vip':
        return TicketTypeEnum.vip
    if ticket_type == 'premium':
        return TicketTypeEnum.premium
    if ticket_type == 'regular':
        return TicketTypeEnum.regular
    raise ValueError('Invalid ticket type')


def ticket_type_enum_to_str(ticket_type: TicketTypeEnum) -> str:
    if ticket_type == TicketTypeEnum.vip:
        return 'vip'
    if ticket_type == TicketTypeEnum.premium:
        return 'premium'
    if ticket_type == TicketTypeEnum.regular:
        return 'regular'
    raise ValueError('Invalid ticket type')


class TicketStatusEnum(enum.Enum):
    pending = 0
    paid = 1


class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, ForeignKey('events.id'))
    status = db.Column(db.Enum(TicketStatusEnum),
                       default=TicketStatusEnum.pending)
    ticket_type = db.Column(db.Enum(TicketTypeEnum))
    reserved_at = db.Column(db.DateTime, default=datetime.utcnow())

    @hybrid_property
    def has_expired(self):
        return (
            self.status == TicketStatusEnum.pending
            and datetime.utcnow() - self.reserved_at > timedelta(minutes=15)
        )

    def __repr__(self):
        return f'<Tickets id={self.id} ticket_type={self.ticket_type} ' \
               f'status={self.status} has_expired={self.has_expired}>'


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    name = db.Column(db.String)
    vip_limit = db.Column(db.Integer)
    premium_limit = db.Column(db.Integer)
    regular_limit = db.Column(db.Integer)

    def __repr__(self):
        return f'<Event id={self.id} name={self.name} date={self.date} ' \
               f'vip_limit={self.vip_limit} ' \
               f'premium_limit={self.premium_limit} ' \
               f'regular_limit={self.regular_limit}>'
