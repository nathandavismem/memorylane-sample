from supabase import create_client, Client

# Load Supabase credentials
SUPABASE_URL = "SUPABASE_URL"
SUPABASE_KEY = "SUPABASE_KEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_batch_centre_id(link_code: str):
    """
    Fetches the centre ID using the given linkCode.

    :param link_code: The linkCode to search for
    :return: Centre ID if found, else None
    """
    response = (
        supabase.table("batch")
        .select("centreId")
        .eq("linkCode", link_code)
        .single()  # Fetch a single row (assuming linkCode is unique)
        .execute()
    )

    return response.data["centreId"] if response.data else None

def get_centre_events(
    link_code: str,
    category: str = None,
    event_date: list[str] = None,  # Now accepts a list of dates
    start_time: str = None,
    end_time: str = None,
    sequence_uid: str = None
):
    """
    Fetches centre events by centre_id (from linkCode) and optional filters.

    :param link_code: The linkCode to get the centre_id
    :param category: (Optional) Program category to filter
    :param event_date: (Optional) List of dates (YYYY-MM-DD) to filter
    :param start_time: (Optional) Start time (HH:MM:SS)
    :param end_time: (Optional) End time (HH:MM:SS)
    :param sequence_uid: (Optional) The sequence UID to filter events
    :return: List of filtered events
    """
    centre_id = get_batch_centre_id(link_code)
    if not centre_id:
        return []  # Return empty list if no centre_id found

    query = supabase.table("centre_events").select("*").eq("centre_id", centre_id)

    if category:
        query = query.eq("category", category)
    if event_date:
        query = query.ov("date", event_date)  # Overlaps with array of dates
    if start_time:
        query = query.gte("time_start", start_time)
    if end_time:
        query = query.lte("time_end", end_time)
    if sequence_uid:
        query = query.eq("sequence_uid", sequence_uid)

    response = query.execute()
    
    return response.data



# Example Usage
if __name__ == "__main__":
    events = get_centre_events("JU5JE", category="Arts & Culture", event_date=["2025-02-28"], start_time="08:00:00", end_time="18:00:00")
    print(events)