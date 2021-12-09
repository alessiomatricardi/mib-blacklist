from mib.dao.manager import Manager
from mib.models.blacklist import Blacklist

from typing import List
from sqlalchemy import or_

class BlacklistManager(Manager):

    @staticmethod
    def block(blacklist: Blacklist):

        Manager.check_none(blacklist=blacklist)
        
        Manager.create(blacklist=blacklist)
    
    @staticmethod
    def unblock(blacklist: Blacklist):
        
        Manager.check_none(blacklist=blacklist)
        
        Manager.delete(blacklist=blacklist)
        
    @staticmethod
    def retrieve_blacklist_by_user_id(user_id):
        
        Manager.check_none(user_id=user_id)
        
        blocking = Blacklist.query.filter(Blacklist.blocked_user_id == user_id).all()
        blocked = Blacklist.query.filter(Blacklist.blocking_user_id == user_id).all()
        
        blocking_ids = [ob.blocking_user_id for ob in blocking]
        blocked_ids = [ob.blocked_user_id for ob in blocked]
        
        return blocking_ids, blocked_ids

    @staticmethod
    def retrieve_blacklist_element(blocking, blocked) -> Blacklist:
        
        Manager.check_none(blocking=blocking)
        Manager.check_none(blocked=blocked)
        
        blacklist = Blacklist.query.filter(Blacklist.blocking_user_id == blocking)\
            .filter(Blacklist.blocked_user_id==blocked).first()

        return blacklist
        