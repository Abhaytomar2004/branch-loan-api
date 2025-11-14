from flask import Blueprint, jsonify, request, abort
from sqlalchemy import select
from uuid import UUID
from decimal import Decimal
import logging

from ..db import SessionContext
from ..models import Loan
from ..schemas import CreateLoanRequest, LoanOut

bp = Blueprint("loans", __name__)
logger = logging.getLogger(__name__)

@bp.route("/loans", methods=["GET"])
def list_loans():
    logger.info("Fetching all loans", extra={"request_id": getattr(request, 'id', 'unknown')})
    
    with SessionContext() as session:
        result = session.execute(select(Loan).order_by(Loan.created_at.desc()))
        loans = [
            LoanOut.model_validate(obj, from_attributes=True).model_dump()
            for obj in result.scalars().all()
        ]
        
        logger.info(f"Retrieved {len(loans)} loans", extra={"request_id": getattr(request, 'id', 'unknown')})
        return jsonify(loans)

@bp.route("/loans/<id>", methods=["GET"])
def get_loan(id: str):
    logger.info(f"Fetching loan {id}", extra={"request_id": getattr(request, 'id', 'unknown')})
    
    try:
        loan_id = UUID(id)
    except Exception:
        logger.warning(f"Invalid loan ID format: {id}", extra={"request_id": getattr(request, 'id', 'unknown')})
        abort(400, description="Invalid loan id")

    with SessionContext() as session:
        loan = session.get(Loan, loan_id)
        if not loan:
            logger.warning(f"Loan not found: {id}", extra={"request_id": getattr(request, 'id', 'unknown')})
            abort(404)
        
        logger.info(f"Loan found: {id}", extra={"request_id": getattr(request, 'id', 'unknown')})
        return jsonify(LoanOut.model_validate(loan, from_attributes=True).model_dump())

@bp.route("/loans", methods=["POST"])
def create_loan():
    logger.info("Creating new loan", extra={"request_id": getattr(request, 'id', 'unknown')})
    
    payload = request.get_json(silent=True) or {}
    try:
        data = CreateLoanRequest(**payload)
    except Exception as e:
        logger.error(f"Loan creation failed: {str(e)}", extra={"request_id": getattr(request, 'id', 'unknown')})
        abort(400, description=str(e))

    with SessionContext() as session:
        loan = Loan(
            borrower_id=data.borrower_id,
            amount=Decimal(str(data.amount)),
            currency=data.currency.upper(),
            term_months=data.term_months,
            interest_rate_apr=(Decimal(str(data.interest_rate_apr)) if data.interest_rate_apr is not None else None),
            status="pending",
        )
        session.add(loan)
        session.flush()
        
        logger.info(f"Loan created successfully: {loan.id}", extra={
            "request_id": getattr(request, 'id', 'unknown'),
            "loan_id": str(loan.id),
            "amount": float(loan.amount),
            "currency": loan.currency
        })
        return jsonify(LoanOut.model_validate(loan, from_attributes=True).model_dump()), 201
