import os
import sys
from pathlib import Path

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)

from file_organizer_app.utils.database import Database
from file_organizer_app.utils.tagging import TagManager

def create_test_files():
    """Create some test files for tagging."""
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    # Create a few test files
    (test_dir / "document1.txt").write_text("This is a test document")
    (test_dir / "document2.txt").write_text("This is another test document")
    (test_dir / "image1.jpg").write_text("This is a fake image file")
    (test_dir / "spreadsheet1.xlsx").write_text("This is a fake spreadsheet file")
    
    return test_dir

def test_tagging():
    """Test the file tagging system."""
    print("Testing file tagging system...")
    
    # Create test files
    test_dir = create_test_files()
    print(f"Created test files in {test_dir}")
    
    # Initialize the tag manager
    tag_manager = TagManager()
    
    # Create some tags
    print("\nCreating tags...")
    document_tag_id = tag_manager.create_tag("document", "#FF5733", "Text documents")
    print(f"Created 'document' tag with ID {document_tag_id}")
    
    image_tag_id = tag_manager.create_tag("image", "#33FF57", "Image files")
    print(f"Created 'image' tag with ID {image_tag_id}")
    
    important_tag_id = tag_manager.create_tag("important", "#3357FF", "Important files")
    print(f"Created 'important' tag with ID {important_tag_id}")
    
    # Tag some files
    print("\nTagging files...")
    document1_path = str(test_dir / "document1.txt")
    document2_path = str(test_dir / "document2.txt")
    image1_path = str(test_dir / "image1.jpg")
    spreadsheet1_path = str(test_dir / "spreadsheet1.xlsx")
    
    tag_manager.tag_file(document1_path, ["document", "important"])
    print(f"Tagged {document1_path} with 'document' and 'important'")
    
    tag_manager.tag_file(document2_path, ["document"])
    print(f"Tagged {document2_path} with 'document'")
    
    tag_manager.tag_file(image1_path, ["image"])
    print(f"Tagged {image1_path} with 'image'")
    
    # Get tags for a file
    print("\nGetting tags for files...")
    document1_tags = tag_manager.get_file_tags(document1_path)
    print(f"Tags for {document1_path}:")
    for tag in document1_tags:
        print(f"  - {tag['name']} ({tag['color']}): {tag['description']}")
    
    # Find files by tag
    print("\nFinding files by tag...")
    document_files = tag_manager.find_files_by_tags(["document"])
    print(f"Files with 'document' tag:")
    for file in document_files:
        print(f"  - {file['path']}")
    
    important_files = tag_manager.find_files_by_tags(["important"])
    print(f"Files with 'important' tag:")
    for file in important_files:
        print(f"  - {file['path']}")
    
    # Find files with multiple tags
    print("\nFinding files with multiple tags...")
    document_important_files = tag_manager.find_files_by_tags(["document", "important"], match_all=True)
    print(f"Files with both 'document' and 'important' tags:")
    for file in document_important_files:
        print(f"  - {file['path']}")
    
    # Suggest tags for a file
    print("\nSuggesting tags for a file...")
    suggested_tags = tag_manager.suggest_tags(spreadsheet1_path)
    print(f"Suggested tags for {spreadsheet1_path}:")
    for tag in suggested_tags:
        print(f"  - {tag}")
    
    # Remove a tag from a file
    print("\nRemoving a tag from a file...")
    tag_manager.untag_file(document1_path, ["important"])
    print(f"Removed 'important' tag from {document1_path}")
    
    document1_tags = tag_manager.get_file_tags(document1_path)
    print(f"Tags for {document1_path} after removal:")
    for tag in document1_tags:
        print(f"  - {tag['name']} ({tag['color']}): {tag['description']}")
    
    print("\nFile tagging test completed successfully!")

if __name__ == "__main__":
    test_tagging()
