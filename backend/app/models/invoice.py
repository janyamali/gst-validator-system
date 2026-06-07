from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import Date

from sqlalchemy.dialects.postgresql import UUID

import uuid

from app.core.database import Base


class Invoice(Base):

    __tablename__ = "invoices"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # PDF DATA

    claim_voucher_number = Column(String)

    vendor_name = Column(String)

    gstin = Column(String)

    invoice_number = Column(String)

    invoice_date = Column(Date)

    taxable_amount = Column(Numeric)

    cgst = Column(Numeric)

    sgst = Column(Numeric)

    igst = Column(Numeric)

    total_amount = Column(Numeric)

    # CLAIM DATA

    claimed_amount = Column(Numeric)

    claimed_gst = Column(Numeric)

    # FINAL RESULT

    validation_status = Column(String)