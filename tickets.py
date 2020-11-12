from dataclasses import dataclass
from typing import Optional

from sqlalchemy import and_, false, true

from events import (EventNotFound, limit_for_event, )
from globals import db
from models import (Events, ticket_type_enum_to_str, Tickets, TicketStatusEnum,
                    TicketTypeEnum, )
from payments import PaymentGateway


def get_ticket(ticket_id: int) -> Tickets:
    ticket = Tickets.query.get(ticket_id)
    if ticket is None:
        raise TicketNotFound
    return ticket

def reserve_ticket(
    event_id: int,
    ticket_type: TicketTypeEnum
) -> int:
    event: Optional[Events] = Events.query.get(event_id)
    if event is None:
        raise EventNotFound

    reserved_tickets_count = Tickets.query.filter(and_(
        Tickets.event_id == event_id,
        Tickets.ticket_type == ticket_type,
        Tickets.has_expired == false(),
    )).count()
    tickets_limit = [
        event.vip_limit,
        event.premium_limit,
        event.regular_limit
    ][ticket_type.value]

    if reserved_tickets_count >= tickets_limit:
        raise TicketsLimitExceeded
    new_ticket = Tickets(
        event_id=event_id,
        ticket_type=ticket_type
    )
    db.session.add(new_ticket)
    db.session.commit()
    return new_ticket.id


def pay_for_ticket(ticket_id, amount, token):
    pg = PaymentGateway()
    ticket: Optional[Tickets] = Tickets.query.get(ticket_id)
    if ticket is None:
        raise TicketNotFound
    if ticket.status == TicketStatusEnum.paid:
        raise TicketAlreadyPaid
    payment_result = pg.charge(amount, token)
    if payment_result is not None:
        ticket.status = TicketStatusEnum.paid
    db.session.commit()


def get_tickets_stats(event_id):
    event = Events.query.get(event_id)
    if event is None:
        raise EventNotFound

    av_tickets = (Tickets.query
                  .filter_by(event_id=event_id)
                  .filter_by(has_expired=False)
                  )
    stats = {
        ticket_type_enum_to_str(t_type): {
            'limit': limit_for_event(event, t_type),
            'reserved': av_tickets.filter_by(ticket_type=t_type).count(),
        }
        for t_type in TicketTypeEnum
    }

    return stats


class TicketNotFound(Exception):
    pass


@dataclass
class TiketsLimits:
    regular: int = 0
    premium: int = 0
    vip: int = 0


class TicketsLimitExceeded(Exception):
    pass


class TicketAlreadyPaid(Exception):
    pass
