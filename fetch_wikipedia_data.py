# This Python file uses the following encoding: utf-8
__author__ = 'Emanuel'

import wikipedia
import pprint

from pymongo import MongoClient
from bson.json_util import dumps

import  flask
from flask.views import  MethodView
from flask import request

from collections import  OrderedDict

app = flask.Flask(__name__)




class RenderJSONWikipediaData(flask.views.MethodView):
    def get(self):
        year = request.args.get('year')
        day = request.args.get('day').replace('_', ' ')
        category = request.args.get('category')

        user_request = WikipediaAPI(day)
        user_request.store_in_local_json(day)



        user_request.create_connection()
        # user_request.insert_to_mongo(OrderedDict(sorted(user_request.json_obj.items())))

        # database_day = flask.jsonify(OrderedDict(sorted(user_request.json_obj.items())))
        return user_request.get_from_mongo_by_day_year_category(year, day, category)

        # return database_day


app.add_url_rule('/', view_func=RenderJSONWikipediaData.as_view('main'))


class WikipediaAPI(object):
    def __init__(self, day):
        self.json_obj = {}
        self.page = wikipedia.page(title=day, preload=False)
        self.content_of_page = self.page.content.encode('ascii', 'ignore')
        self.events = self.content_of_page[self.content_of_page.find('== Events ==') + len('== Events ==\n'):self.content_of_page.find('== Births ==')]
        self.births = self.content_of_page[self.content_of_page.find('== Births ==') + len('== Births ==\n'):self.content_of_page.find('== Deaths ==')]
        self.deaths = self.content_of_page[self.content_of_page.find('== Deaths ==') + len('== Deaths ==\n'):self.content_of_page.find('== Holidays and observances ==')]
        self.holidays_and_observances = self.content_of_page[self.content_of_page.find('== Holidays and observances ==') + len('== Holidays and observances ==\n')  : self.content_of_page.find('== External links ==')]
        self.json_obj["day"] = day;
        #self.json_obj[day] = {"events" : [], "births" : [], "deaths" : [], "holidays_and_observances" : []}
        self.json_obj["events"] = []
        self.json_obj["births"] = []
        self.json_obj["deaths"] = []
        self.json_obj["holidays_and_observances"] = []



    def store_events_of_requested_day(self, day):
        for event in iter(self.events.splitlines()):
            an_event = event.split(" ", 1)
            if len(an_event) == 2:
                self.json_obj["events"].append({"year": an_event[0], "title": an_event[1]})

    def store_births_of_requested_day(self, day):
        for birth in iter(self.births.splitlines()):
            a_birth = birth.split(" ", 1)
            if len(a_birth) == 2:
                self.json_obj["births"].append({"year": a_birth[0], "title": a_birth[1]})

    def store_deaths_of_requested_day(self, day):
        for death in iter(self.deaths.splitlines()):
            a_death = death.split(" ", 1)
            if len(a_death) == 2:
                self.json_obj["deaths"].append({"year": a_death[0], "title": a_death[1]})

    def store_holidays_and_observances_of_requested_day(self, day):
        for holiday_and_observance in iter(self.holidays_and_observances.splitlines()):
            if holiday_and_observance is not '':
                self.json_obj["holidays_and_observances" ].append({"title" : holiday_and_observance})

    def store_in_local_json(self, day):
        self.store_events_of_requested_day(day)
        self.store_births_of_requested_day(day)
        self.store_deaths_of_requested_day(day)
        self.store_holidays_and_observances_of_requested_day(day)

    def create_connection(self):
        self.client = MongoClient()
        self.db = self.client.hootsuite

    def insert_to_mongo(self, json):
        self.db.pages.insert_one(json)

    def get_from_mongo_by_day_year_category(self, year, day, category):

        cursor = self.db.pages.find({day : {'$exists' : True}})
        return dumps(cursor)




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

if __name__ == "__main__":
    app.debug = True
    app.run()
    # a = {}
    # a["key"]={"beans" : []}
    # a["key"]["beans"] = 123
    # pprint.pprint(a)




