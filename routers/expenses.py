#crud operations for expenses:
#create an expense
#update an expense
#read 1 expense
#read all expenses
#read muultiple expenses
#delete an expense
#get expenses/summary total and breakdown by category

from auth import get_current_user
from database import get_db
from fastapi import APIRouter,Depends,HTTPException
from models import Expense as Expensemodel
from schemas import ExpenseOut,ExpenseIn,ExpenseUpdate
from typing import List


router=APIRouter(prefix="/expenses",tags=["expenses"])

@router.post("/new_expense", response_model=ExpenseOut)
def create_expense(new_expense:ExpenseIn,user=Depends(get_current_user), db=Depends(get_db)):
    db_expense=Expensemodel(
        user_id=user.id,
        title=new_expense.title,
        amount=new_expense.amount,
        category=new_expense.category,
        date=new_expense.date

    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.put("/update_expense/{id}",response_model=ExpenseOut) #upate logic new...review
def update_expense(id:int,expense:ExpenseUpdate,user=Depends(get_current_user),db=Depends(get_db)):

    saved_expense=db.query(Expensemodel).filter(Expensemodel.id==id,Expensemodel.user_id==user.id).first()
    if not saved_expense:
      raise HTTPException(status_code=404, detail="Expense not found")

    
    for field, value in expense.model_dump(exclude_unset=True).items():
      setattr(saved_expense, field, value)



    db.commit()
    db.refresh(saved_expense)
    return saved_expense


@router.get("/read_expense/{id}",response_model=ExpenseOut)
def read_expense(id:int,db=Depends(get_db),user= Depends(get_current_user)):
    expense=db.query(Expensemodel).filter(Expensemodel.id==id,Expensemodel.user_id==user.id).first()
    if not expense:
      raise HTTPException(status_code=404, detail="Expense not found")

    return expense


@router.get("/read_all",response_model=List[ExpenseOut])
def read_all(db=Depends(get_db),user=Depends(get_current_user)):
    expenses=db.query(Expensemodel).filter(Expensemodel.user_id==user.id).all()
    
    return expenses

@router.delete("/delete/{id}")
def delete_expense(id:int,db=Depends(get_db),user=Depends(get_current_user)):
    expense=db.query(Expensemodel).filter(Expensemodel.id==id,Expensemodel.user_id==user.id).first()
    if not expense:
      raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return{"Message":"expense deleted"}


