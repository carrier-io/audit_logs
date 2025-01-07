#!/usr/bin/python3
# coding=utf-8

#   Copyright 2022 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" Slot """
# from tools import auth  # pylint: disable=E0401
from pylon.core.tools import web, log  # pylint: disable=E0611,E0401
from tools import db
from ..models import Log, RelatedEntity
from ..serializers.log import log_schama
from datetime import datetime


class Event:  # pylint: disable=E1101,R0903
    """
        Event Resource
    """

    @web.event("audit_add_log")
    def _add_log(self, context, event, payload):
        related_entities = payload.pop('related_entities')
        related_entities = tuple() if related_entities is None else related_entities
        log.info(related_entities)
        entities = []
        for data in related_entities:
            entities.append(RelatedEntity(**data))
        audit_log = Log(**payload)
        audit_log.related_entities = entities
        if not audit_log.created_at:
            audit_log.created_at = datetime.utcnow()
        audit_log.updated_at = datetime.utcnow()

        db.session.add(audit_log)
        db.session.commit()

        context.sio.emit("new_log_added", log_schama.dump(audit_log))
