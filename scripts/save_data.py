# SHADOWHACKER-GOD: scripts/save_data.py (Windows/tarfile Compatible)
import sys, os, requests, base64
import tarfile

def save_data(gist_id, token, source_dir):
    """Compresses the data folder, encodes, and uploads to Gist."""
    
    temp_file = "saved_data.tar.gz"
    
    try:
        # 1. ضغط مجلد البيانات باستخدام مكتبة tarfile
        with tarfile.open(temp_file, "w:gz") as tar:
            # arcname يضمن حفظ المجلد بنفس الاسم عند فك الضغط
            tar.add(source_dir, arcname=os.path.basename(source_dir))
            
        # 2. تشفير الملف المضغوط إلى Base64
        with open(temp_file, "rb") as f:
            encoded_data = base64.b64encode(f.read()).decode('utf-8')
            
    except Exception as e:
        print(f"FATAL ERROR: Compression/Encoding failed: {e}")
        return

    # 3. إرسال البيانات المحدثة إلى Gist API
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
    url = f"https://api.github.com/gists/{gist_id}"
    
    payload = {
        "description": "AEON RDP Persistent Data Backup",
        "files": {
            "fixed_data.b64": {
                "content": encoded_data
            }
        }
    }
    
    try:
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status() 
        print("SUCCESS: Data saved persistently to GitHub Gist.")
        
    except requests.exceptions.RequestException as e:
        print(f"FATAL ERROR: Could not save data to Gist: {e}")
    
    os.remove(temp_file) # Cleanup
    
if __name__ == "__main__":
    save_data(sys.argv[1], sys.argv[2], sys.argv[3])
