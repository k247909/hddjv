# SHADOWHACKER-GOD: scripts/restore_data.py (Windows/tarfile Compatible)
import sys, os, requests, base64
import tarfile

def restore_data(gist_id, token, target_dir):
    """Downloads data from Gist, decodes, and extracts it."""
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
    url = f"https://api.github.com/gists/{gist_id}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raises an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not fetch Gist data: {e}")
        return
        
    gist_data = response.json()
    file_content = gist_data['files'].get('fixed_data.b64', {}).get('content', '')
    
    if file_content and file_content.strip() != 'INIT':
        try:
            compressed_data = base64.b64decode(file_content)
            
            # Save the compressed data temporarily
            temp_file = "restored_data.tar.gz"
            with open(temp_file, "wb") as f:
                f.write(compressed_data)
            
            # Use Python's tarfile module for extraction (compatible on Windows)
            with tarfile.open(temp_file, "r:gz") as tar:
                # Extracts contents into the target directory
                tar.extractall(target_dir)
            
            os.remove(temp_file) # Cleanup temporary file
            print("SUCCESS: Data restored from Gist.")
            
        except Exception as e:
            print(f"WARNING: Could not decode/extract data, possibly first run or corruption: {e}")
    else:
        print("INFO: Gist is empty or 'INIT'. Starting clean.")
            
if __name__ == "__main__":
    restore_data(sys.argv[1], sys.argv[2], sys.argv[3])
