from src.schema import UserModel


class Worker:
    def __init__(self, user: UserModel):
        self.user_id = user['user_id']
        self.name = user['name']
        self.surname = user['surname']
        self.phone = user['phone']
        self.email = user['email']
        self.tag = user['tag']
        self.status = user['status']
        self.kpi = user['kpi']
        self.skill = user['skill']
        self.employment_date = user['employment_date']
        self.hour = user['day']
        self.day = user['night']
        self.note = user['note']


