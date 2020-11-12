import datetime as datetime

from globals import db
from models import (Events, TicketTypeEnum, )


def create_event(
    event_name: str,
    date: datetime.date,
    vip_limit: int,
    premium_limit: int,
    regular_limit: int,
):
    event = Events(
        name=event_name,
        date=date,
        vip_limit=vip_limit,
        premium_limit=premium_limit,
        regular_limit=regular_limit,
    )
    db.session.add(event)
    db.session.commit()
    return event.id

def get_event(event_id: int) -> Events:
    event = Events.query.get(event_id)
    if event is None:
        raise EventNotFound
    return event

def limit_for_event(event: Events, ticket_type: TicketTypeEnum):
    if ticket_type == TicketTypeEnum.vip:
        return event.vip_limit
    if ticket_type == TicketTypeEnum.regular:
        return event.regular_limit
    if ticket_type == TicketTypeEnum.premium:
        return event.premium_limit
    raise ValueError('Unknow ticket type')


class EventNotFound(Exception):
    pass


