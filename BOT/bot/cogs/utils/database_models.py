from tortoise import Model, fields


class RegistrationRecord(Model):
    guild_id = fields.IntField()
    member_id = fields.IntField()
