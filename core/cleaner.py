import os
import shutil

def clear_downloads_folder():
    """
    Deletes all files inside the 'downloads' directory.
    Asks for user confirmation before deletion.
    """
    downloads_path = os.path.join(os.getcwd(), 'downloads')

    # Check if directory exists
    if not os.path.exists(downloads_path):
        print(f"⚠️ Directory not found: {downloads_path}")
        return

    # Check if directory is empty
    if not os.listdir(downloads_path):
        print("✅ The downloads folder is already empty.")
        return

    print(f"🗑️  Target Directory: {downloads_path}")
    print("⚠️  WARNING: This will delete ALL files in this folder.")
    
    # User Confirmation
    confirm = input("❓ Are you sure? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Operation cancelled.")
        return

    # Deletion Logic
    deleted_count = 0
    try:
        for filename in os.listdir(downloads_path):
            file_path = os.path.join(downloads_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path) # Delete file
                    deleted_count += 1
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path) # Delete folder
                    deleted_count += 1
            except Exception as e:
                print(f"❌ Failed to delete {filename}. Reason: {e}")
        
        print(f"✅ Success! Deleted {deleted_count} items.")

    except Exception as e:
        print(f"❌ Critical Error: {e}")