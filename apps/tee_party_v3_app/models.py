from __future__ import unicode_literals
from django.db import models
import re

class GolferManager(models.Manager):
    def validate(self, postData):
        errors = {}       
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')  
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = "Invalid email address!"
        if len(postData['first_name'])  < 2:
            errors['first_name'] = "First name must be at least two characters long" 
        if len(postData['last_name'])  < 2:
            errors['last_name'] = "Last name must be at least two characters long" 
        if len(postData['handicap'])  < 1:
            errors['handicap'] = "Handicap must be at least one character long"
        if len(postData['best_scorecard'])  < 2:
            errors['best_scorecard'] = "Best Scorecard must be at least two characters long" 
        if Golfer.objects.filter(email=postData['email']):
            errors['email'] = "Email is already registered" 
        if postData['confirm_pw'] != postData['password']:
            errors['confirm_pw'] = "Passwords must match!"     
        return errors

    def update_validation(self, postData):
        errors = {}        
        if len(postData['handicap'])  < 1:
            errors['handicap'] = "Handicap must be at least one character long"
        if len(postData['best_scorecard'])  < 2:
            errors['best_scorecard'] = "Best Scorecard must be at least two characters long"       
        return errors

class Golfer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    handicap = models.IntegerField()
    best_scorecard = models.IntegerField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
    user_status = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GolferManager()

    def __repr__(self):
        return f"<Golfer {self.id} ({self.user_status}): {self.first_name} {self.last_name}>"


class CourseManager(models.Manager):
    def basic_validate(self, postData):
        errors = {}
        if Course.objects.filter(name=postData['name']):
            errors['name'] = "This course has already been added"         
        if Course.objects.filter(address=postData['address']):
            errors['adress'] = "This course has already been added"         
        if len(postData['name'])  < 3:
            errors['name'] = "Course name must be at least three characters long"
        if len(postData['address'])  < 3:
            errors['address'] = "Address must be at least three characters long"
        if len(postData['par'])  < 2:
            errors['par'] = "Par must be at least two characters long"
        if len(postData['rating'])  < 2:
            errors['rating'] = "Rating must be at least two characters long"
        if len(postData['slope'])  < 2:
            errors['slope'] = "Slope must be at least two characters long"    
        return errors
    
class Course(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    par = models.IntegerField()
    rating = models.FloatField()
    slope = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CourseManager()


    def __repr__(self):
        return f"<Course ({self.id}): {self.name}>"
        

class TeeTime(models.Model):
    tee_time = models.CharField(max_length=255)
    location = models.ForeignKey(Course, related_name="tee_time_at_course")
    player = models.ForeignKey(Golfer, related_name="golfer_playing")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __repr__(self):
        return f"<Tee Time ({self.id}): {self.player.first_name} is playing {self.location.name} at {self.tee_time}"


