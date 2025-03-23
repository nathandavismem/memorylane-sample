from supabase import create_client, Client
from dateutil import parser
import pytz

# Load Supabase credentials
SUPABASE_URL = "SUPABASE_URL"
SUPABASE_KEY = "SUPABASE_KEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def convert_times_to_timezone(activity: dict):
    """
    Converts the time values in the 'time' array to the correct time based on 'time_zone',
    formatting them as "yyyy-MM-dd HH:mm".

    :param activity: Dictionary containing 'time' (list of timestamps) and 'time_zone'.
    :return: Updated activity dictionary with formatted 'time' values.
    """
    if not activity.get("time") or not activity.get("time_zone"):
        return activity  # No changes if time or time_zone is missing

    target_tz = pytz.timezone(activity["time_zone"])

    converted_times = []
    for timestamp in activity["time"]:
        dt_utc = parser.isoparse(timestamp)  # Parse string to datetime (UTC)
        dt_local = dt_utc.astimezone(target_tz)  # Convert to target timezone
        formatted_time = dt_utc.strftime("%Y-%m-%d %H:%M")  # Format as "yyyy-MM-dd HH:mm"
        converted_times.append(formatted_time)

    return {**activity, "time": converted_times}  # Return updated activity

def get_centre_activities(
    centre_id: int,
    category: str = None,
    event_dates: list[str] = None,
    min_date: str = None,
    max_date: str = None,
):
    query = supabase.table("centre_activities").select("*").eq("centre_id", centre_id)

    if min_date:
        query = query.gte("date", min_date)
    
    if max_date:
        query = query.lte("date", max_date)

    if category:
        query = query.eq("program_category", category)

    if event_dates:
        if len(event_dates) == 1:
            query = query.eq("date", event_dates[0])
        else:
            query = query.in_("date", event_dates)

    response = query.execute()
    
    # Convert and format the times for each activity
    activities = response.data or []
    return [convert_times_to_timezone(activity) for activity in activities]


# Example Usage
if __name__ == "__main__":
    events = get_centre_activities(11)
    print(events)
