## channels_create_v1 assumptions:
    - eachtime the channel_id that created by the function should  be unique.
## channel_message_v1 assumptions:
    - user id can be invalid so it is important to test the validity of the user id
    - start number can not less than zero
- Assume that name_first and name_last provided in auth-register-v1 will be only alphanumeric characters i.e. [A-Za-z0-9]
