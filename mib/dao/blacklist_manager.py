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
    def retrieve_blacklist_by_user_id(user_id) -> List[int]:
        
        Manager.check_none(user_id=user_id)
        
        blacklist = Blacklist.query.filter(or_(
            Blacklist.blocking_user_id == user_id,
            Blacklist.blocked_user_id == user_id
        )).all()
        
        blacklist_ids = [ob.blocked_user_id if ob.blocking_user_id == user_id else ob.blocking_user_id for ob in blacklist]

        return blacklist_ids

    @staticmethod
    def retrieve_blacklist_element(blocking, blocked) -> Blacklist:
        
        Manager.check_none(blocking=blocking)
        Manager.check_none(blocked=blocked)
        
        blacklist = Blacklist.query.filter(Blacklist.blocking_user_id == blocking)\
            .filter(Blacklist.blocked_user_id==blocked).first()

        return blacklist
        