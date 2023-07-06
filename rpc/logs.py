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

""" RPC """
import operator
import json
from pylon.core.tools import web, log  # pylint: disable=E0611,E0401
from sqlalchemy import or_, and_, asc, desc
from tools import rpc_tools, db
from ..models.logs import Log, RelatedEntity


class RPC:  # pylint: disable=E1101,R0903
    """ RPC Resource """

    @web.rpc("audit_get_logs", "get_logs")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def _get_logs(self, project_id, flask_args):        
        args = dict(flask_args)
        args.pop('_', None)
        limit = args.pop('limit', 100)
        offset = args.pop('offset', None)
        search = args.pop('search', None)
        sort = args.pop('sort', None)
        order = args.pop('order', None)

        auditable_id = args.pop('auditable_id', None)
        auditable_type = args.pop('auditable_type', None)
        related_entities = json.loads(args.pop('related_entities', None))


        query = db.session.query(Log).filter(Log.project_id==project_id)
        query = query.filter(or_(
            and_(
                Log.auditable_id==auditable_id,
                Log.auditable_type==auditable_type
            ),
            Log.related_entities.any(
                and_(
                    RelatedEntity.auditable_id==related_entities['auditable_id'], 
                    RelatedEntity.auditable_type==related_entities['auditable_type'],
                )
            )
        ))

        
        if search:
            query = query.filter(or_(
                Log.description.like(f'%{search}%'),
                Log.user_email.like(f'%{search}%'),
            ))

        filter_ = list()
        for key, value in args.items():
            filter_.append(operator.eq(getattr(Log, key), value))
        filter_ = and_(*tuple(filter_))

        query = query.filter(filter_)
        total = query.count()

        if sort:
            column = getattr(Log, sort, Log.id)
            sort_order = asc(column) if order == "asc" else desc(column)
            query = query.order_by(sort_order)
        else:
            query = query.order_by(Log.id.asc())

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        return total, query.all()



    