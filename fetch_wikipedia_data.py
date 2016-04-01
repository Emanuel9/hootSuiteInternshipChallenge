# This Python file uses the following encoding: utf-8
__author__ = 'Emanuel'

from collections import  OrderedDict
import sys

import wikipedia

from pymongo import MongoClient

import bson.json_util
import  json

import  flask
from flask.views import  MethodView
from flask import request
app = flask.Flask(__name__)




class RenderJSONWikipediaData(flask.views.MethodView):
    def get(self):
        year = request.args.get('year')
        day = request.args.get('day').replace('_', ' ')
        category = request.args.get('category')


        user_request = WikipediaAPI(day)
        user_request.create_connection()

        print(user_request.check_if_data_already_exist_in_mongo_db(day), sys.stderr)

        if user_request.check_if_data_already_exist_in_mongo_db(day):
            print(11, sys.stderr)
            user_request.store_in_local_json(day)

            user_request.insert_to_mongo(OrderedDict(sorted(user_request.json_obj.items())))

        user_request.close_connection()
        return user_request.get_from_mongo_by_day_year_category(year, day, category)

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
        self.json_obj["day"] = day
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

    def close_connection(self):
        self.client.close()

    def insert_to_mongo(self, json):
        self.db.pages.insert_one(json)


    def check_if_data_already_exist_in_mongo_db(self, day):
        records = self.db.pages.find({"day" : day}).count()
        if records > 0:
            return False
        return True


    def get_from_mongo_by_day_year_category(self, year, day, category):
        if year is None:
            cursor = self.db.pages.find({"day" : day}, {"_id" : 0, category : []})
        else:
            cursor = self.db.pages.find({"day" : day}, {"_id" : 0, category : { '$elemMatch' : {'year' : year}}})


        output =  json.dumps({'results' :  list(cursor), 'day' : day}, default= bson.json_util.default, indent=4, separators=(',', ': '))
        return output


if __name__ == "__main__":
    app.debug = True
    app.run()





