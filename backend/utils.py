from datetime import datetime, timedelta
from typing import Optional

"""
Utility helpers for CareSRE HMS backend.
Provides functions for token generation, time calculations, and OPD load normalization.
"""



def generate_token_number(prefix: str = "TKN") -> str:
    """
    Generate a unique token number using timestamp.
    
    Args:
        prefix: Token prefix (default: "TKN")
    
    Returns:
        Unique token string
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    return f"{prefix}{timestamp}"


def calculate_time_window(start_hour: int, duration_minutes: int) -> tuple[datetime, datetime]:
    """
    Calculate start and end times for a time window.
    
    Args:
        start_hour: Starting hour (0-23)
        duration_minutes: Window duration in minutes
    
    Returns:
        Tuple of (start_time, end_time)
    """
    now = datetime.now()
    start = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    end = start + timedelta(minutes=duration_minutes)
    return start, end


def normalize_opd_load(current_load: int, max_capacity: int) -> float:
    """
    Normalize OPD load to a 0-1 scale.
    
    Args:
        current_load: Current patient count
        max_capacity: Maximum OPD capacity
    
    Returns:
        Normalized load value (0.0 to 1.0)
    """
    if max_capacity <= 0:
        return 0.0
    return min(current_load / max_capacity, 1.0)


def is_within_time_window(check_time: Optional[datetime] = None, 
                         start: datetime = None, 
                         end: datetime = None) -> bool:
    """
    Check if a time falls within a window.
    
    Args:
        check_time: Time to check (default: current time)
        start: Window start time
        end: Window end time
    
    Returns:
        True if time is within window
    """
    check_time = check_time or datetime.now()
    return start <= check_time <= end if (start and end) else False