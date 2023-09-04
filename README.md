# OTP Based Authentication Microservice
The Authentication Microservice is a standalone application designed to deliver secure user authentication functionality, including OTP-based authentication, password reset, and account updates.

This repository contains a Django custom user model implementation that extends Django's built-in AbstractBaseUser and BaseUserManager classes to create a custom user model called customUser. This custom user model includes fields for user authentication and additional user information.

Technology consists of :
- Python
- Django
- django-rest-framework
- Some libraries of django-rest-framework

## Scope
Core responsibilities of Authentication based microservice are:
- User Registration
- User Login with OTP-based Authentication
- Password Reset
- Account Information Update

### User Registration

The Authentication Microservice features an API endpoint i.e (register/) that allows users to register. During registration, the following information is collected:
- First Name
- Last Name
- Email Address
- Phone Number
- Password
  
### User Login with OTP-based Authentication

This microservice includes an API endpoint that enables users to log in using their phone number and OTP-based authentication. Users enter their phone number, receive an OTP via SMS.

### Password Reset

The Authentication Microservice provides an API endpoint i.e (password-reset/) for users to reset their passwords. To initiate a password reset, users must provide their email address. This action triggers an email to the user's registered email address, containing a link to a password reset page.

### Account Information Update

Users can update their account information through an API endpoint. Information that can be updated includes:

- First Name
- Last Name
- Phone Number
- Password

The API endpoint validates the user's input and updates their account if the provided information is valid.








