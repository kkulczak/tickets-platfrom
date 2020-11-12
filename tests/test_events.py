from datetime import date, datetime

import pytest

from events import (create_event, )
from tickets import (get_tickets_stats, pay_for_ticket, reserve_ticket,
                     TicketsLimitExceeded, TiketsLimits, )
from models import TicketTypeEnum


def test_create_event():
    create_event(
        'Event1',
        date=datetime.today(),
        vip_limit=10,
        premium_limit=10,
        regular_limit=10,
    )


def test_reserve_ticket():
    reserve_ticket(
        event_id=1,
        ticket_type=TicketTypeEnum.vip
    )


def test_event_limits():
    event_id = create_event(
        event_name='test1',
        date=date(year=2020, month=12, day=25),
        vip_limit=1,
        premium_limit=2,
        regular_limit=3,
    )
    for ticket_type, amount in {
        TicketTypeEnum.vip: 1,
        TicketTypeEnum.premium: 2,
        TicketTypeEnum.regular: 3,
    }.items():
        for _ in range(amount):
            ticket_id = reserve_ticket(event_id, ticket_type)
            pay_for_ticket(ticket_id, 10, 'token')

    stats = get_tickets_stats(event_id)
    for obj in stats.values():
        assert obj['limit'] == obj['reserved']

    with pytest.raises(TicketsLimitExceeded):
        reserve_ticket(event_id, TicketTypeEnum.vip)
    with pytest.raises(TicketsLimitExceeded):
        reserve_ticket(event_id, TicketTypeEnum.premium)
    with pytest.raises(TicketsLimitExceeded):
        reserve_ticket(event_id, TicketTypeEnum.regular)
