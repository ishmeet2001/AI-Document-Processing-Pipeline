from pydantic import BaseModel, Field
import datetime
from typing import List

class ClinicalNoteDetails(BaseModel):
    Symptom: str = Field(description="Individual symptom reported by the patient")
    Duration: str = Field(description="Duration or onset timing of the symptom")

class PatientReferral(BaseModel):
    Patient_Name: str = Field(description="Full name of the patient being referred")
    DOB: datetime.date = Field(description="Date of birth of the patient")
    Referring_Physician: str = Field(description="Full name and title of the referring physician")
    Urgency: str = Field(description="Referral priority/urgency: Urgent, Semi-Urgent, or Routine")
    Clinical_Notes: List[ClinicalNoteDetails] = Field(description="Detailed clinical symptoms and notes")
