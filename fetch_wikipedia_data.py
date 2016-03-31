# This Python file uses the following encoding: utf-8
__author__ = 'Emanuel'

import wikipedia
import pprint
import json
from pymongo import MongoClient


import flask, flask.views
from flask.views import  MethodView
from flask import request

app = flask.Flask(__name__)

@app.route('/')
class GenericRequest(MethodView):
    def get(self):
        year = request.args.get('year')
        day = request.args.get('day')
        category = request.args.get('category')
        return 'year:%s, day:%s, category:%s' % (year,day,category)

# class View(flask.views.MethodView):
#      def get(self):
#          year =
#          return 'year:%s, day:%s, category:%s' % (year,day,category)

# app.add_url_rule('/', view_func=View.as_view('main'))

app.debug = True
app.run()
#

# print wikipedia.page(title="New york")

# client = MongoClient()
# db = client.test
# cursor = db.restaurants.find()

# for document in cursor:
#     print document

# page = wikipedia.page(title='November 3', preload=False)
# content_of_page = page.content.encode('ascii','ignore')
#
#
# events = content_of_page[content_of_page.find('== Events ==') + len('== Events ==\n'):content_of_page.find('== Births ==')]
# births = content_of_page[content_of_page.find('== Births ==') + len('== Births ==\n'):content_of_page.find('== Deaths ==')]
# deaths = content_of_page[content_of_page.find('== Deaths ==') + len('== Deaths ==\n'):content_of_page.find('== Holidays and observances ==')]
# holidays_and_observances = content_of_page[content_of_page.find('== Holidays and observances ==') + len('== Holidays and observances ==\n')  : content_of_page.find('== External links ==')]
#
# json_obj = {
#     "November_3" : {
#         "events" : [],
#         "births" : [],
#         "deaths" : [],
#         "holidays_and_observances" : []
#
#     }
# }
#
# def store_events_of_requested_day(events):
#     for event in iter(events.splitlines()):
#         an_event = event.split(" ", 1)
#         if len(an_event) == 2:
#             json_obj["November_3"]["events"].append({"year": an_event[0], "description": an_event[1]})
#
# def store_births_of_requested_day(births):
#     for birth in iter(births.splitlines()):
#         a_birth = birth.split(" ", 1)
#         if len(a_birth) == 2:
#             json_obj["November_3"]["births"].append({"year": a_birth[0], "description": a_birth[1]})
#
# def store_deaths_of_requested_day(deaths):
#     for death in iter(deaths.splitlines()):
#         a_death = death.split(" ", 1)
#         if len(a_death) == 2:
#             json_obj["November_3"]["deaths"].append({"year": a_death[0], "description": a_death[1]})
#
# store_events_of_requested_day(events)
# store_births_of_requested_day(births)
# store_deaths_of_requested_day(deaths)
#
# pprint.pprint(json_obj["November_3"])


# # print births
# print deaths
# print holidays_and_observances
