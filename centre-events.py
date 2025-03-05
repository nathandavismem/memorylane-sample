from supabase import create_client, Client

# Load Supabase credentials
SUPABASE_URL = "SUPABASE_URL"
SUPABASE_KEY = "SUPABASE_KEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_centre_activities(
    centre_id: int,
    category: str = None,
    event_date: str = None,  # Now accepts a list of dates
    start_time: str = None,
    end_time: str = None,
    min_date: str = None,
):
    query = supabase.table("centre_activities").select("*").eq("centre_id", centre_id)
    
    if min_date:
        query = query.gte("min_date", min_date)
    
    if category:
        query = query.eq("program_category", category)
        
    if event_date:
        query = query.ov("date", [event_date])  # Overlaps with array of dates
        
    if start_time:
        query = query.gte("time_start", start_time)
        
    if end_time:
        query = query.lte("time_end", end_time)

    response = query.execute()
    
    return response.data


# Example Usage
if __name__ == "__main__":
    events = get_centre_activities(11, min_date="2025-02-28")
    print(events)