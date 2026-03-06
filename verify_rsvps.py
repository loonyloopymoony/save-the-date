import urllib.request
import json
from datetime import datetime

FIREBASE_URL = "https://g3kr7-be157-default-rtdb.asia-southeast1.firebasedatabase.app/rsvps.json"

def check_rsvps():
    print(f"📡 Querying Firebase Realtime Database at {FIREBASE_URL}...\n")
    
    try:
        # Fetch data from Firebase REST API
        with urllib.request.urlopen(FIREBASE_URL) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode('utf-8'))
                
                if data:
                    print(f"✅ Success! Found {len(data)} RSVP(s) in the database:\n")
                    print("-" * 60)
                    print(f"{'Guest Name':<25} | {'Attending':<10} | {'Count':<5} | {'Date Submited'}")
                    print("-" * 60)
                    
                    for key, rsvp in data.items():
                        name = rsvp.get('name', 'Unknown')
                        is_attending = "Yes" if rsvp.get('attending') == "yes" else "No"
                        count = rsvp.get('count', '-')
                        
                        # Format timestamp if it exists
                        timestamp = rsvp.get('timestamp')
                        if timestamp:
                            date_str = datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%d %H:%M')
                        else:
                            date_str = "N/A"
                            
                        print(f"{name:<25} | {is_attending:<10} | {count:<5} | {date_str}")
                    print("-" * 60)
                else:
                    print("⚠️ Database is empty. Waiting for the first RSVP...")
            else:
                print(f"❌ Failed to fetch data. HTTP Status: {response.getcode()}")
                
    except urllib.error.URLError as e:
        print(f"❌ Network Error: Could not connect to Firebase. {e.reason}")
    except json.JSONDecodeError:
        print("❌ Error: Received invalid JSON data from Firebase.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    check_rsvps()
