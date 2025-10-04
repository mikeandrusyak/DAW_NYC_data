from sodapy import Socrata

# Generates the quarterly data ranges for given years
def generate_quarters(start_year, end_year) -> list:
    quarters = []
    for year in range(start_year, end_year + 1):
        quarters.append((f"{year}-01-01T00:00:00", f"{year}-03-31T23:59:59"))
        quarters.append((f"{year}-04-01T00:00:00", f"{year}-06-30T23:59:59"))
        quarters.append((f"{year}-07-01T00:00:00", f"{year}-09-30T23:59:59"))
        quarters.append((f"{year}-10-01T00:00:00", f"{year}-12-31T23:59:59"))
    return quarters

# Creates the Socrata client to fetch data from NYC Open Data 
def create_client(BASE_URL: str) -> Socrata:
    return Socrata(BASE_URL, None, timeout=60) 