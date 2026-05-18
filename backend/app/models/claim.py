from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Numeric

from sqlalchemy.dialects.postgresql import UUID

import uuid

from app.core.database import Base


class Claim(Base):

    __tablename__ = "claims"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    employee_name = Column(String)

    claim_number = Column(String)

    claimed_amount = Column(Numeric)

    claimed_gst = Column(Numeric)

    vendor_name = Column(String)

    invoice_number = Column(String)