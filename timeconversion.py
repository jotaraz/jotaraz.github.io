# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 10:06:56 2025

@author: J_Taraz
"""

# do timeshit!


from datetime import datetime, timezone, timedelta
import re

def parse_timestamp(ts: str) -> datetime:
    """
    Parse a timestamp string into a timezone-aware UTC datetime.

    Supported formats:
      - ISO 8601 UTC with 'Z', e.g. "2025-10-01T09:12:34Z"
      - ISO 8601 with timezone offset, e.g. "2025-10-01T11:12:34+02:00"
      - Compact ISO format: "YYYYMMDDTHHMMSSZ" (e.g. "20251001T091234Z")
      - Unix epoch seconds (int or float string), e.g. "1696150354" or "1696150354.5"
    
    Returns:
        datetime: A timezone-aware UTC datetime.

    Raises:
        ValueError: If the timestamp cannot be parsed.
    """
    ts = ts.strip()
    
    # Case 1: Unix epoch seconds (integer or float)
    # example: 1696150354.5
    if re.fullmatch(r"\d{10}(\.\d+)?", ts):  # 10-digit seconds, optionally with fraction
        try:
            return datetime.fromtimestamp(float(ts), tz=timezone.utc)
        except (ValueError, OSError) as e:
            raise ValueError(f"Invalid epoch timestamp {ts!r}: {e}") from e

    # Case 2: ISO 8601 with UTC 'Z' suffix
    # example: 2025-10-01T09:12:34Z
    if ts.endswith("Z"):
        # Try full ISO form e.g. 2025-10-01T09:12:34Z
        iso_candidate = ts[:-1]  # remove Z
        try:
            dt = datetime.fromisoformat(iso_candidate)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            # Maybe compact form: 20251001T091234Z
            m = re.fullmatch(r"(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z", ts)
            if m:
                y, mo, d, h, mi, s = map(int, m.groups())
                return datetime(y, mo, d, h, mi, s, tzinfo=timezone.utc)
            raise ValueError(f"Unrecognized ISO-Z timestamp format: {ts!r}")

    # Case 3: ISO 8601 with timezone offset (e.g. +02:00)
    # datetime.fromisoformat handles this directly
    # example 2025-10-01T11:12:34+02:00
    try:
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            raise ValueError("Timestamp lacks timezone info")
        return dt.astimezone(timezone.utc)
    except ValueError:
        pass

    # Nothing matched
    raise ValueError(f"Unsupported timestamp format: {ts!r}")

def parse_timestamp2(ts: str) -> datetime:
    ts = ts.strip()

    # Case 1: Unix epoch seconds (integer or float)
    if re.fullmatch(r"\d{10}(\.\d+)?", ts):
        try:
            dt = datetime.fromtimestamp(float(ts), tz=timezone.utc)
            return dt.replace(tzinfo=None)  # strip timezone
        except (ValueError, OSError) as e:
            raise ValueError(f"Invalid epoch timestamp {ts!r}: {e}") from e
    
    # Case 2: ISO 8601 UTC with 'Z'
    if ts.endswith("Z"):
        iso_candidate = ts[:-1]
        try:
            dt = datetime.fromisoformat(iso_candidate)
            return dt.replace(tzinfo=None)  # treat as UTC, naive
        except ValueError:
            # Compact format like 20251001T091234Z
            m = re.fullmatch(r"(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z", ts)
            if m:
                y, mo, d, h, mi, s = map(int, m.groups())
                return datetime(y, mo, d, h, mi, s)
            raise ValueError(f"Unrecognized ISO-Z timestamp format: {ts!r}")
    
    # Case 3: ISO 8601 with offset (+02:00 etc.)
    try:
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            raise ValueError("Timestamp lacks timezone info")
        # Convert to UTC, then drop tzinfo
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc.replace(tzinfo=None)
    except ValueError:
        pass


timestrings = ["2025-10-01T09:12:34Z", 
               "2025-10-01T11:12:34+02:00",
               "1696150354", 
               "20251001T091234Z",
               '2025-10-01T09:20:00Z', 
               "2025-10-01T09:21:00Z",
               "2025-10-01T09:22:00Z",
               "1696150354"] 


for timestr in timestrings:
    print(timestr, parse_timestamp(timestr)) #.replace(tzinfo=None))
    



