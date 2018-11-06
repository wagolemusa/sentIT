from flask import Flask,jsonify,request, make_response
from flask_restful import Resource

import datetime
import jwt
from functools import wraps
from __init__ import *


class Home(Resource):
	def get(self):
		return {"message": "SendIT is one of popular courier services"}


class Parcels(Resource):
	def post(self):
		parcel = {
		len(Orders)+ 1:{
		'pickup':request.get_json()['pickup'],
		'destination':request.get_json()['destination'],
		'weight':request.get_json()['weight']
		}}
		Orders.update(parcel)
		return jsonify(Orders)

	"""get all delivery parcels"""
	def get(self):
		return make_response(jsonify(
			{
			'Status': "Ok",
      'Message': "Success",
      'parcel': Orders
      }), 200)

class ParcelID(Resource):
	""" delete parcel order """
	def delete(self, parcel_id):
		del Orders[parcel_id]
		return jsonify({"message": "Succesfuly Deleted"})

	""" get a specific parcel"""
	def get(self, parcel_id):
		return make_response(jsonify(
			{
			'Status': "Ok",
      'Message': "Success",
      'parcel': (Orders[parcel_id])
      }), 200)