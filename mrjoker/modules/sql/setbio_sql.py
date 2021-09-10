import threading
from mrjoker.modules.sql import BASE, SESSION
from sqlalchemy import Boolean, Column, Integer, UnicodeText, String


class BIO(BASE):
    __tablename__ = "user_bio"

    user_id = Column(Integer, primary_key=True)
    is_sudo = Column(Boolean)
    fname = Column(UnicodeText)

    def __init__(self, user_id, fname="", is_sudo=True):
        self.user_id = user_id
        self.fname = fname
        self.is_sudo = is_sudo

    def __repr__(self):
        return "{}".format(self.user_id)


BIO.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

SUDO_USERS = {}
SUDO_USERSS = {}


def is_bio(user_id):
    return user_id in SUDO_USERS
    return user_id in SUDO_USERSS


def check_bio_status(user_id):
    try:
        return SESSION.query(BIO).get(user_id)
    finally:
        SESSION.close()


def set_bio(user_id, fname):
    with INSERTION_LOCK:
        curr = SESSION.query(BIO).get(user_id)
        if not curr:
            curr = BIO(user_id, fname, True)
        else:
            curr.is_sudo = True
            curr.fname = fname
        SUDO_USERS[user_id] = fname
        SUDO_USERSS[user_id] = fname
        SESSION.add(curr)
        SESSION.commit()


def rm_bio(user_id):
    with INSERTION_LOCK:
        curr = SESSION.query(BIO).get(user_id)
        if curr:
            if user_id in SUDO_USERS:  # sanity check
                del SUDO_USERS[user_id]
                del SUDO_USERSS[user_id]
            SESSION.delete(curr)
            SESSION.commit()
            return True

        SESSION.close()
        return False
def get_all_bio_id():
    stark = SESSION.query(BIO).all()
    SESSION.close()
    return stark

def __load_sudo_users():
    global SUDO_USERS
    global SUDO_USERSS
    try:
        all_bio = SESSION.query(BIO).all()
        SUDO_USERS = {user.user_id: user.fname for user in all_bio if user.is_sudo}
        SUDO_USERSS = {user.user_id: user.fname for user in all_bio if user.is_sudo}
    finally:
        SESSION.close()


__load_sudo_users()
