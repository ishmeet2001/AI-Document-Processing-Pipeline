from pydantic import BaseModel,Field
import datetime
from typing import List
class ItemDetails(BaseModel):
    Description:str=Field("Details about the Item")
    Quantity:str=Field("How much the item is required by the user")
    Unit_price:int=Field("Price of one item")

class Invoice(BaseModel):
    Sender_Name:str=Field(description="Invoice Sender Name Information")
    Date:datetime.date=Field(description="Date of the Invoice")
    Item_Details:List[ItemDetails]
    Total_Amount:float=Field(description="Total Amount of the Sender")
    Currency:str=Field(description="Currency Name")