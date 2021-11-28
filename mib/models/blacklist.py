from mib import db

# TODO look at mib-users/mib/models/user.py


class Blacklist(db.Model):
    """Representation of Blacklist model."""
    # The name of the table that we explicitly set

    __tablename__ = 'blacklist'
    SERIALIZE_LIST = ['blocking_user_id', 'blocked_user_id']
    blocking_user_id = db.Column(db.Integer, nullable=False)
    blocked_user_id = db.Column(db.Integer, nullable=False)

   


    __table_args__ = (
        db.PrimaryKeyConstraint(
            blocking_user_id, blocked_user_id,
        ),
    )

    def __init__(self, *args, **kw):
        super(Blacklist, self).__init__(*args, **kw)

    def set_blocking_user_id(self, blocking_user):
        self.blocking_user_id = blocking_user

    def set_blocked_user_id(self, blocked_user):
        self.blocked_user_id = blocked_user
    
    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])