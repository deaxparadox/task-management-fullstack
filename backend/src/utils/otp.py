
import pyotp
from sqlalchemy.orm import Session

from src.models.otp import Otp

class OTP:
    __current_otp_counter = None
    __current_otp = None
    
    
    def __init__(self, db: Session = None):
        self.otp_model = Otp
        self.__db = db
        self.hotp = pyotp.HOTP('base32secret3232')
    
    def set_db(self, db: Session):
        self.__db = db
    
    def generate(self):
        """
        This function returns the current otp counter, 
        generate the associated OTP from counter,
        and increment and save the new counter value in database. 
        """
        if not self.__db:
            raise RuntimeError("Database session not set for otp")
        
        row: Otp = self.__db.query(self.otp_model).with_for_update().first()
        
        # get otp and counter
        self.__current_otp_counter = row.counter
        self.__current_otp = self.hotp.at(self.__current_otp_counter)
        
        # update counter
        row.counter = row.counter+1
        self.save(row)
        
    @property
    def otp(self):
        return self.__current_otp
    
    @property
    def otp_counter(self):
        return self.__current_otp_counter
    
    def save(self, row):
        self.__db.add(row)
        self.__db.commit()
        
    def verify(self, otp: str, otp_counter: int):
        return self.hotp.verify(otp, otp_counter)