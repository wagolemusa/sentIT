import datetime
import psycopg2
import random 
from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
from functools import wraps
from flask_jwt_extended import (
  	jwt_required, create_access_token, get_current_user, 
    get_jwt_identity 
)
from models.user_model import Usermodel

connection = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
curr = connection.cursor()

class Home(Resource):
	def get(self):
		return {"message": "SendIT is one of the popular courier services"}

class CreateParcel(Resource):
	""" Class for create parcel methods """
	@jwt_required
	def post(self):		
		title = request.json['title']
		pickup = request.json['pickup']
		rec_id = request.json['rec_id']
		rec_phone = request.json['rec_phone']
		rec_name  = request.json['rec_name']
		destination = request.json['destination']
		weight = request.json['weight']

		if title.strip() == '' or pickup.strip() =='' or destination.strip() =='':
			return jsonify({"message":"Feilds  cannot be blank"})
		# elif type(rec_id) != int or type(rec_phone) != int or type(weight) != int:
			# return jsonify({"meassge":"ID, Phone and weight master be numbers"})

		current_user = get_jwt_identity()
		username = current_user
		try:

			curr.execute(""" INSERT INTO orders(title, username, pickup,rec_id, rec_phone, rec_name, destination, weight)
																				VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",\
																				(title, username, pickup, rec_id, rec_phone,rec_name, destination, weight))
			connection.commit()
			return jsonify({"message": 'Successfuly Created an Order'})
		except:
			connection.rollback()
			return {"message": "already exists"}


	@jwt_required
	def get(self):
		""" Method for get all Parcel Orders """
		username = get_jwt_identity()
		curr.execute(" SELECT * FROM orders WHERE username =%s", [username])
		data = curr.fetchall()
		if not data:
			return jsonify({"message":"There is no orders yet"})
		data_list = []
		for row in data:
			parcel_id = row[0]
			title = row[2]
			pickup = row[4]
			rec_id = row[5]
			rec_phone = row[6]
			rec_name = row[7]
			destination = row[8]
			weight = row[9]
			status = row[10]
			created_on = row[11]
			data_list.append({"parcel_id":parcel_id, "title":title, "pickup":pickup, "rec_id":rec_id, "rec_phone":rec_phone, "rec_name":rec_name, "destination":destination, "weight":weight, "status":status, "created_on":created_on})
		return jsonify({"data": data_list})	

class ModifyOrder(Resource):
	""" Class for put an order """
	@jwt_required
	def put(self, parcel_id):
		""" Method to update an order """		
		
		parcel_order = Usermodel().found_by_Id(parcel_id)

		if not parcel_order:
			return {"message":"There is no order ID {} found".format(parcel_id)}, 403	

		title = request.json['title']
		pickup = request.json['pickup']
		rec_id = request.json['rec_id']
		rec_phone = request.json['rec_phone']
		rec_name  = request.json['rec_name']
		destination = request.json['destination']
		weight = request.json['weight']

		curr.execute("""UPDATE orders SET title= %s, pickup=%s, rec_id=%s, rec_phone=%s, rec_name=%s, destination=%s, weight=%s
																														WHERE parcel_id=%s """,(title, pickup, rec_id, rec_phone, rec_name, destination, weight, parcel_id))
		connection.commit()
		return jsonify({"message": "Successfuly Updated"})

	@jwt_required
	def delete(self, parcel_id):
		username = get_jwt_identity()
		""" Method for deleting a specific order """
		parcel_order = Usermodel().found_by_Id(parcel_id)

		if not parcel_order:
			return {"message":"There is no order ID {} found".format(parcel_id)}, 403	
		curr.execute("""DELETE FROM orders WHERE parcel_id = %s AND username = %s""",(parcel_id, username))
		connection.commit()
		return jsonify({"message":"Post Deleted"})

class AnOrder(Resource):
	@jwt_required
	def put(self, parcel_id):
		data = request.get_json(force=True)
		
		destination = data['destination']

		curr.execute("""UPDATE orders SET destination=%s WHERE parcel_id=%s """,(destination,	parcel_id))
		connection.commit()

		curr.execute(" SELECT * FROM orders WHERE parcel_id =%s", [parcel_id])
		data = curr.fetchall()
		data_list = []
		for row in data:
			parcel_id = row[0]
			destination = row[8]
			data_list.append({"parcel_id":parcel_id, "destination":destination})
			return jsonify({"data": data_list})	
		return jsonify({"message": "Successfuly Updated"})
		

class Booking(Resource):
	@jwt_required
	def post(self):
		"""This methods helps a user to book the transport service"""
		data = request.get_json(force=True)
		bookingref = random.randint(1, 1000)
		bookingref = str(bookingref)
		car_number = data['car_number']
		from_location = data['from_location']
		to_location = data['to_location']
		price = data['price']
		quality = data['quality']
		dates  = data['dates']
		total = data['total']
		# if car_number.strip() == '' or from_location.strip() == '' or price.strip() == '' or quality.strip() == '' or data.strip() == '':
			# return{"message": "All Fields Cannot be empty!"}

		current_user = get_jwt_identity()
		username = current_user
		curr.execute(""" INSERT INTO booking(bookingref, username, car_number,from_location, to_location, price, quality, dates, total)
																				VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",\
																				(bookingref, username, car_number, from_location, to_location,price, quality, dates, total))
		connection.commit()
		return jsonify({"message": 'Thanks for booking make sure that you came with number'})
	

	@jwt_required
	def get(self):
		""" Method for get all bookings """
		username = get_jwt_identity()
		curr.execute(" SELECT * FROM booking WHERE username =%s", [username])
		book = curr.fetchall()
		if not book:
			return jsonify({"message":"There is no bookings yet"})
		book_list = []
		for row in book:
			book_id = row[0]
			bookingref = row[2]
			car_number = row[4]
			from_location = row[5]
			to_location = row[6]
			price = row[7]
			quality = row[8]
			dates = row[9]
			total = row[10]
			status = row[11]
			created_on = row[12]
			book_list.append({"book_id":book_id, "bookingref":bookingref, "car_number":car_number, "from_location":from_location, "to_location":to_location, "price":price, "quality":quality, "dates":dates, "total":total, "status":status, "created_on":created_on})
		return jsonify({"book": book_list})	



class BookPostpond(Resource):
	@jwt_required
	def put(self, book_id):
		data = request.get_json(force=True)
		dates = data['dates']
		status = data['status']
		curr.execute("""UPDATE booking SET dates=%s, status=%s WHERE book_id=%s """,(dates, status,	book_id))
		connection.commit()
		return jsonify({"message": "Successfuly Updated"})
		connection.rollback()
		return {"message": "already exists"}


class SearchBooking(Resource):
	""" Methods for searching towns """
	@jwt_required
	def post(self):
		from_location = request.json['from_location']
		to_location = request.json['to_location']

		curr.execute("SELECT * FROM prices WHERE from_location = %s AND to_location =%s",[from_location,to_location])
		data = curr.fetchall()
		if not data:
			return jsonify({"message":"There is no root yet"})
		books = []
		for row in data:
			price_id = row[0]
			car_number = row[1]
			from_location = row[2]
			to_location = row[3]
			price = row[4]
			day_time = row[5]

			books.append({"price_id":price_id, "car_number":car_number, "from_location": from_location, "to_location":to_location, "price":price, "day_time":day_time})
		return jsonify({"data": books})
		return jsonify({"message":"You can book now"})


class Users(Resource):
	""" Get a user account """
	def get(self):
		""" Method for get all Parcel Orders """
		username = get_jwt_identity()
		curr.execute(" SELECT * FROM users WHERE username =%s", [username])
		data = curr.fetchall()
		if not data:
			return jsonify({"message":"There is no user yet"})
		user = []
		for row in data:
			user_id = row[0]
			first_name = row[1]
			last_name = row[2]
			username = row[3]
			phone = row[4]
			email = row[5]
			user.append({"user_id":user_id, "first_name":first_name, "last_name":last_name, "username":username, "phone":phone, "email":email})
			return jsonify({"data":user})