from flask import Blueprint, jsonify
from sqlalchemy import text
from ..db import SessionContext

bp = Blueprint("health", __name__)

@bp.route("/health", methods=["GET"])
def health():
    try:
        # Database connectivity check
        with SessionContext() as session:
            session.execute(text("SELECT 1"))
            db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"

    return jsonify({
        "status": "ok",
        "database": db_status,
        "service": "branch-loan-api",
        "timestamp": "2025-11-14T18:00:00Z"
    })
