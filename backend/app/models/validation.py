from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import Boolean

from sqlalchemy.dialects.postgresql import UUID

import uuid

from app.core.database import Base


class Validation(Base):

    __tablename__ = "validations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    invoice_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    status = Column(String)

    remarks = Column(String)

    validated_gst = Column(Numeric)

    mismatch_amount = Column(Numeric)

    duplicate_detected = Column(Boolean)

    voucher_match = Column(Boolean)

    vendor_match = Column(Boolean)

    invoice_match = Column(Boolean)

    amount_match = Column(Boolean)

    gst_match = Column(Boolean)