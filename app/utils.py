from pytz import timezone
from datetime import datetime

from sqlalchemy.orm import Session
from typing import List, Optional
def get_kst_now() -> datetime:
    """Get now datetime at KST."""
    return datetime.now(timezone("Asia/Seoul"))

