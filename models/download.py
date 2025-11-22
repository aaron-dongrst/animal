import os
import urllib.request
import sys
import time

# --- FILES TO DOWNLOAD ---
# We use the official public links because they allow direct downloading.
# Google Drive links often block scripts with "Virus Scan" warnings.

FILES = [
    {
        "name": "Model Weights (SLOWFAST_8x8_R50.pkl)",
        "url": "https://dl.fbaipublicfiles.com/pyslowfast/model_zoo/kinetics400/SLOWFAST_8x8_R50.pkl",
        "dest_folder": os.path.join("models", "weights"),
        "filename": "SLOWFAST_8x8_R50.pkl"
    },
    {
        "name": "Config File (SLOWFAST_8x8_R50.yaml)",
        "url": "https://raw.githubusercontent.com/facebookresearch/SlowFast/master/configs/Kinetics/c2/SLOWFAST_8x8_R50.yaml",
        "dest_folder": os.path.join("models", "configs"),
        "filename": "SLOWFAST_8x8_R50.yaml"
    }
]

# --- PROGRESS BAR FUNCTION ---
def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration)) if duration > 0 else 0
    
    # Handle unknown total size (common with GitHub raw links)
    if total_size > 0:
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write(f"\r   Downloading... {percent}% | {progress_size / (1024 * 1024):.2f} MB | {speed} KB/s")
    else:
        sys.stdout.write(f"\r   Downloading... {progress_size / 1024:.0f} KB")
    
    sys.stdout.flush()

# --- MAIN SCRIPT ---
def main():
    print(f"🚀 Starting Setup for FaunaVision...")

    for item in FILES:
        print(f"\n\n------------------------------------------------")
        print(f"📦 Processing: {item['name']}")
        
        # 1. Create directory
        if not os.path.exists(item['dest_folder']):
            try:
                os.makedirs(item['dest_folder'])
                print(f"   📁 Created folder: {item['dest_folder']}")
            except OSError as e:
                print(f"   ❌ Error creating folder: {e}")
                continue

        # 2. Define full path
        dest_path = os.path.join(item['dest_folder'], item['filename'])

        # 3. Check if exists
        if os.path.exists(dest_path):
            print(f"   ⚠️  File already exists at: {dest_path}")
            print("      Skipping download.")
            continue

        # 4. Download
        print(f"   ⬇️  Source: {item['url']}")
        try:
            urllib.request.urlretrieve(item['url'], dest_path, reporthook)
            print(f"\n   ✅ Success! Saved to: {dest_path}")
        except Exception as e:
            print(f"\n   ❌ Download Failed: {e}")

    print("\n\n🎉 All tasks completed.")

if __name__ == "__main__":
    main()