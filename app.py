import datetime
# from datetime import
import os

from flask import abort, Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from events import create_event, EventNotFound, get_event
from globals import api, app, db
from models import Events, ticket_type_str_to_enum
from tickets import (get_ticket, get_tickets_stats, pay_for_ticket,
                     reserve_ticket, )
from translation_engine import decode, encode


class EventsDetailsApi(Resource):
    def get(self, event_id):
        try:
            event = get_event(event_id)
        except EventNotFound as e:
            abort(400, 'Event id not Found')
        return jsonify({
            'event_id': event.id,
            'name': event.name,
            'date': str(event.date),
            'premium_limit': event.premium_limit,
            'regular_limit': event.regular_limit,
            'vip_limit': event.vip_limit,
        })


class EventsApi(Resource):
    def post(self):
        event_id = create_event(
            event_name=request.json['event_name'],
            date=datetime.datetime.strptime(
                request.json['date'],
                '%d/%m/%y'
            ).date(),
            vip_limit=request.json['vip_limit'],
            premium_limit=request.json['premium_limit'],
            regular_limit=request.json['regular_limit'],
        )
        return jsonify({'event_id': event_id})


class EventTicketsApi(Resource):
    def get(self, event_id):
        stats = get_tickets_stats(event_id)
        print(stats)
        return jsonify(stats)

    def post(self, event_id):
        if not request.json:
            abort(400)
        if 'ticket_type' not in request.json:
            abort(400)
        if request.json['ticket_type'] not in ['vip', 'premium', 'regular']:
            abort(400)
        ticket_id = reserve_ticket(
            event_id,
            ticket_type=ticket_type_str_to_enum(request.json['ticket_type'])
        )
        return jsonify({"ticket_id": ticket_id})


class TicketApi(Resource):
    def get(self, ticket_id):
        ticket = get_ticket(ticket_id)
        return jsonify(ticket)

    def put(self, ticket_id):
        if (
            not request.json
            or 'amount' not in request.json
            or 'token' not in request.json
        ):
            pay_for_ticket(
                ticket_id,
                amount=request.json['amount'],
                token=request.json['token']
            )
        return


api.add_resource(EventsApi, '/v1/events')
api.add_resource(EventsDetailsApi, '/v1/events/<int:event_id>')
api.add_resource(EventTicketsApi, '/v1/events/<int:event_id>/tickets')
api.add_resource(TicketApi, '/tickets/<int:ticket_id>')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, use_reloader=False)
    # app.run(
    #     # threaded=True,
    #     debug=True,
    # )
