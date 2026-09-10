
class Student: 
    def __init__(
        self,
        dni: str = "",
        name: str = "",
        lastname: str = "",
        corp: str = "",
        movil: str = "",
        phone: Optional[str] = None,
        mail: str = "",
        job: str = "",
        student_type: str = "",
        state: str = "",
        ev1: Optional[float] = None,
        ev2: Optional[float] = None,
        ev3: Optional[float] = None,
        ev4: Optional[float] = None,
        evf: Optional[float] = None,
        time: Optional[float] = None,
        firstconection: Optional[str] = None
    ):
        self.dni = dni
        self.name = name
        self.lastname = lastname
        self.corp = corp
        self.movil = movil
        self.phone = phone
        self.mail = mail
        self.job = job
        self.student_type = student_type
        self.state = state
        self.ev1 = ev1
        self.ev2 = ev2
        self.ev3 = ev3
        self.ev4 = ev4
        self.evf = evf
        self.time = time
        self.firstconection = firstconection
        
    def full_name_v1(self):
        return self.name + " " + self.lastname
    
    def full_name_v2(self):
        return self.lastname + ", " + self.name
    