from mib.dao.manager import Manager
from mib.models.blacklist import Blacklist

class BlacklistManager(Manager):

    @staticmethod
    def block(blacklist: Blacklist):
        Manager.create(blacklist=blacklist)
        
    @staticmethod
    def retrieving_blacklist(user_id):
        Manager.check_none(user_id=user_id)
        blacklist = Blacklist.query.filter(Blacklist.blocking_user_id == user_id).all()

        return [ob for ob in blacklist]
        
    @staticmethod
    def unblock(blacklist: Blacklist):
        Manager.check_none(blacklist=blacklist)
        Manager.delete(blacklist=blacklist)

    @staticmethod
    def retrieving_blacklist_element(blocking, blocked):
        Manager.check_none(blocking=blocking)
        Manager.check_none(blocked=blocked)
        blacklist = Blacklist.query.filter(Blacklist.blocking_user_id == blocking).where(Blacklist.blocked_user_id==blocked).first()

        return blacklist
        