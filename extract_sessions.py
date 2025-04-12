#!/usr/bin/env python3
"""
GTC Session Extractor
---------------------
Extract session details from the NVIDIA GTC HTML catalog page.
"""

import os
import sys
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def export_to_markdown(sessions):
    print("Generating Markdown table...")
    
    # Consolidate sessions by session_code to avoid duplicate rows
    consolidated_sessions = {}
    for session in sessions:
        session_code = session.get('session_code', '')
        session_id = f"{session_code}_{session.get('title', '')}"
        
        if session_id not in consolidated_sessions:
            consolidated_sessions[session_id] = session.copy()
            # Initialize speakers as a list
            consolidated_sessions[session_id]['speakers'] = []
            
        # Add speaker if not already in the list
        if session.get('speakers'):
            for speaker in session['speakers']:
                speaker_name = speaker.get('name', '')
                if speaker_name and speaker_name not in [s.get('name', '') for s in consolidated_sessions[session_id]['speakers']]:
                    consolidated_sessions[session_id]['speakers'].append(speaker)
    
    # Convert to list
    sessions_list = list(consolidated_sessions.values())
    print(f"Preparing Markdown for {len(sessions_list)} unique sessions...")
    
    # Start building the markdown content
    md_content = "# NVIDIA GTC 2025 Sessions\n\n"
    
    # Create the table header with additional columns for files and replay links
    md_content += "| Session Code | Title | Speakers | Date/Time | Location | Files | Replay | Abstract |\n"
    md_content += "|-------------|-------|----------|-----------|----------|-------|--------|----------|\n"
    
    # Helper function to clean text for markdown
    def clean_text_for_markdown(text):
        if text is None:
            return ""
        # Replace newlines, pipe characters, and excessive spaces
        cleaned = str(text).replace('\n', ' ').replace('|', '\\|').replace('\r', ' ')
        # Remove any non-breaking spaces or other problematic characters
        cleaned = ' '.join(cleaned.split())
        return cleaned
    
    # Helper to validate if text is a time string (containing AM or PM but not as part of another word)
    def is_valid_time(text):
        if not text:
            return False
        return bool((" AM" in text or " PM" in text) and not ("LAM" in text))
    
    # Process each session
    for session in sessions_list:
        session_code = clean_text_for_markdown(session.get('session_code', ''))
        title = clean_text_for_markdown(session.get('title', ''))
        
        # Format speakers as a list with line breaks
        speakers_list = []
        for speaker in session.get('speakers', []):
            if isinstance(speaker, dict) and 'name' in speaker:
                name = speaker['name']
                if speaker.get('title_organization'):
                    name += f" ({speaker['title_organization']})"
                speakers_list.append(name)
            elif isinstance(speaker, str):
                speakers_list.append(speaker)
        
        speakers = "<br>".join([clean_text_for_markdown(s) for s in speakers_list if s])
        
        # Ensure date/time and location are in the correct columns and contain valid data
        date_time = clean_text_for_markdown(session.get('date_time', ''))
        if not is_valid_time(date_time):
            date_time = ""  # Clear invalid time strings
            
        location = clean_text_for_markdown(session.get('location', ''))
        
        # Format files as links with line breaks
        files_list = session.get('files', [])
        if files_list:
            files_md = []
            for file in files_list:
                file_name = clean_text_for_markdown(file.get('file_name', ''))
                file_url = file.get('file_url', '')
                if file_name and file_url:
                    files_md.append(f"[{file_name}]({file_url})")
            files = "<br>".join(files_md)
        else:
            files = ""
        
        # Add replay link if available
        replay_url = session.get('replay_url', '')
        if replay_url:
            replay = f"[Replay]({replay_url})"
        else:
            replay = ""
        
        # Truncate abstract to a reasonable length to avoid huge cells
        abstract = session.get('abstract', '')
        if abstract:
            abstract = clean_text_for_markdown(abstract)
            if len(abstract) > 100:
                abstract = abstract[:100] + "..."
        
        # Add row to the table with the new columns
        row = f"| {session_code} | {title} | {speakers} | {date_time} | {location} | {files} | {replay} | {abstract} |\n"
        md_content += row
    
    # Write to file
    output_file = "gtc_sessions_table.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"Markdown table generated and saved to {output_file}")
    return output_file

def main():
    # Path to the HTML file
    html_file_path = os.path.abspath("Attendee Portal - Session Catalog.html")
    
    if not os.path.exists(html_file_path):
        print(f"Error: HTML file not found at {html_file_path}")
        sys.exit(1)
    
    print(f"Processing HTML file: {html_file_path}")
    
    # Step 1: Load the HTML file using Playwright
    print("Initializing browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Load HTML file in browser
        print("Loading HTML file...")
        page = context.new_page()
        page.goto(f"file://{html_file_path}")

        try:
            print("Waiting for page to load...")
            page.wait_for_load_state('networkidle')  # wait for dynamic content to fully load
        except PlaywrightTimeoutError:
            print("Warning: Page took too long to load, proceeding with current state.")

        # Save fully rendered HTML for parsing
        print("Getting rendered HTML...")
        rendered_html = page.content()
        
        print("Closing browser...")
        browser.close()
    
    # Step 2: Parse the Rendered HTML
    print("Parsing HTML...")
    soup = BeautifulSoup(rendered_html, 'html.parser')
    
    # Step 3: Extract All Sessions Elements
    print("Finding session containers...")
    # First, try to find by exact class
    sessions_containers = soup.find_all('div', class_='catalog-result-title session-title')
    
    if not sessions_containers:
        print("Warning: No sessions found using first selector. Trying alternative...")
        # Try alternative approaches if the first one fails
        sessions_containers = soup.find_all('div', class_=lambda c: c and 'session-title' in c)
    
    print(f"Found {len(sessions_containers)} session containers.")
    
    if not sessions_containers:
        print("Error: No session containers found. Extraction failed.")
        sys.exit(1)
    
    # Step 4: Iterate and Extract Session Data
    print("Extracting session data...")
    sessions_extracted = []
    
    for i, container in enumerate(sessions_containers, 1):
        print(f"Processing session {i}/{len(sessions_containers)}")
        parent = container.find_parent()

        # Title & URL
        title_element = container.find('a')
        session_title = title_element.text.strip() if title_element else None
        session_url = title_element['href'] if title_element and 'href' in title_element.attrs else None
        
        # Find session code/ID
        session_code = None
        code_element = parent.find('div', text=lambda t: t and t.strip().startswith('[') and ']' in t)
        if code_element:
            session_code = code_element.text.strip()
        
        # Abstract
        abstract_div = parent.find('div', class_='description')
        if not abstract_div:
            abstract_div = parent.find('div', class_=lambda c: c and 'description' in c)
        abstract = abstract_div.text.strip() if abstract_div else None

        # Speakers
        speakers_list = []
        speakers_area = parent.find('div', class_=lambda c: c and 'speaker-details' in c)
        if speakers_area:
            # Try to extract speakers with different possible structures
            speaker_elements = speakers_area.find_all('button', class_=lambda c: c and 'speaker' in c)
            if speaker_elements:
                for speaker_elem in speaker_elements:
                    speaker_name = speaker_elem.text.strip()
                    # Try to find associated details for this speaker
                    next_elem = speaker_elem.find_next('span')
                    title_org = next_elem.text.strip() if next_elem else None
                    
                    speakers_list.append({
                        "name": speaker_name,
                        "title_organization": title_org
                    })
            else:
                # If the button method doesn't work, try other selectors
                speaker_texts = speakers_area.get_text().strip().split('\n')
                for text in speaker_texts:
                    if text.strip():
                        speakers_list.append({
                            "name": text.strip(),
                            "title_organization": None
                        })

        # Date and Time
        date_time = None
        # Look for text containing AM/PM
        date_time_div = parent.find(lambda tag: tag.name and tag.string and 
                                  isinstance(tag.string, str) and 
                                  ('AM' in tag.string or 'PM' in tag.string) and
                                  not ('LAM' in tag.string))  # Avoid matching terms like "LAM" which aren't time
        if date_time_div:
            date_time = date_time_div.text.strip()
        
        # Location
        location = None
        # Look for text containing location emoji or "Room" text
        location_div = parent.find(lambda tag: tag.name and tag.string and 
                                 isinstance(tag.string, str) and 
                                 ('📍' in tag.string or 'Room' in tag.string) and
                                 not ('LAM' in tag.string))  # Avoid matching terms like "LAM" which aren't location
        if location_div:
            location = location_div.text.strip()
            if '📍' in location:
                location = location.replace('📍', '').strip()

        # Files (optional)
        files = []
        files_component = parent.find('div', class_=lambda c: c and 'session-files' in c)
        if files_component:
            for link in files_component.find_all('a', href=True):
                files.append({
                    "file_name": link.text.strip(),
                    "file_url": link['href']
                })

        # Replay button/link (optional)
        replay_url = None
        
        # Check all links for replay indicators with detailed HTML inspection
        replay_indicators = ['replay', 'watch', 'video', 'stream', 'recording']
        all_links = parent.find_all('a', href=True)
        
        for link in all_links:
            link_text = link.text.lower()
            link_href = link['href'].lower()
            
            # Check for replay indicators in the link text or URL
            if any(indicator in link_text for indicator in replay_indicators) or any(indicator in link_href for indicator in replay_indicators):
                replay_url = link['href']
                break
        
        # Fallback: If no explicit replay link found, check if the session URL itself could be a replay
        if not replay_url and session_url:
            # For sessions with certain codes, the session URL is likely the replay URL
            session_prefixes = ['D', 'P', 'S']
            if session_code and any(code in session_code for code in session_prefixes):
                replay_url = session_url

        sessions_extracted.append({
            "session_code": session_code,
            "title": session_title,
            "url": session_url,
            "abstract": abstract,
            "speakers": speakers_list,
            "date_time": date_time,
            "location": location,
            "files": files,
            "replay_url": replay_url
        })
    
    # Step 5: Save Extracted Data
    print("Preparing data for export...")
    
    # Export to Markdown table format
    export_to_markdown(sessions_extracted)
    
    # First, count total sessions with replay URLs
    total_replay_urls = sum(1 for session in sessions_extracted if session.get("replay_url"))
    print(f"Found {total_replay_urls} sessions with replay URLs out of {len(sessions_extracted)} total sessions")
    
    # Process each session for CSV export
    flat_sessions = []
    
    # Track the number of sessions with replay URLs in the flattened data
    replay_count = 0
    
    for session in sessions_extracted:
        # Store a local copy of replay_url to ensure it's preserved across all rows
        session_replay_url = session.get("replay_url", "")
        
        # Handle sessions with no speakers
        if not session["speakers"]:
            flat_session = session.copy()
            flat_session["speaker_name"] = None
            flat_session["speaker_title_org"] = None
            flat_session["replay_url"] = session_replay_url  # Ensure replay_url is preserved
            del flat_session["speakers"]
            
            # Count replay URLs for debugging
            if session_replay_url:
                replay_count += 1
                
            flat_sessions.append(flat_session)
        else:
            # For sessions with speakers, create a row for each speaker
            for speaker in session["speakers"]:
                flat_session = session.copy()
                flat_session["speaker_name"] = speaker.get("name")
                flat_session["speaker_title_org"] = speaker.get("title_organization")
                flat_session["replay_url"] = session_replay_url  # Ensure replay_url is preserved
                del flat_session["speakers"]
                
                # Only count the replay URL once per session, even if multiple speakers
                if session_replay_url and speaker == session["speakers"][0]:
                    replay_count += 1
                    
                flat_sessions.append(flat_session)
    
    # Convert files list to string representation for CSV
    for session in flat_sessions:
        if session["files"]:
            file_strings = []
            for file in session["files"]:
                file_strings.append(f"{file['file_name']}: {file['file_url']}")
            session["files"] = "; ".join(file_strings)
        else:
            session["files"] = None
    
    # Create DataFrame
    df_sessions = pd.DataFrame(flat_sessions)
    
    # Log the number of sessions with replay URLs in the flattened data
    print(f"Found {replay_count} sessions with replay URLs in the flattened data")
    
    # Ensure all expected columns are present
    required_columns = [
        "session_code", "title", "url", "abstract", "date_time", 
        "location", "files", "replay_url", "speaker_name", "speaker_title_org"
    ]
    
    for col in required_columns:
        if col not in df_sessions.columns:
            df_sessions[col] = None
    
    # Save to CSV
    output_file = "gtc_sessions_extracted.csv"
    print(f"Saving data to {output_file}...")
    df_sessions.to_csv(output_file, index=False)
    
    print(f"Extraction complete! Extracted {len(sessions_extracted)} sessions.")
    print(f"Data saved to {output_file} and gtc_sessions_table.md")

if __name__ == "__main__":
    main() 