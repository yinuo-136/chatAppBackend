## auth_login_v1:
    - assume that every registered user is already logged in

## auth_register_v1:
    - assume that name_first and name_last can contain non-alphanumeric characters.
    - assume that emails are case-senstive i.e. email@gmail.com != Email@gmail.com
    - assume that empty string handles are valid, if fully non-alphanumeric first name and last name are provided

## channel_create_v1:
    - assume that owners of channels are counted as members of that channel

## data_store.py:
    - assume that logged_in_users is required to be stored, for later use and testing.

## general:
    - assume auth user id can be invalid so it is important to test the validity of it
    - assume unspecified error cases will raise an AccessError.


