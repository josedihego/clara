#!/usr/bin/env python3
"""
Jekyll Gallery Stub Generator

Generates all necessary .md stub files for Jekyll collections
to fix GitHub Pages 404 issues with dynamically generated gallery URLs.

Usage:
    python generate_stubs.py [gallery.yml] [albums_output_dir]
    
    gallery.yml        - Path to your gallery YAML file (default: _data/gallery.yml)
    albums_output_dir  - Output directory for album stub files (default: albums)
"""

import yaml
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

def load_gallery_config(file_path: str) -> Dict[str, Any]:
    """Load and parse the gallery YAML configuration."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ Error: Gallery file '{file_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML: {e}")
        sys.exit(1)

def sanitize_filename(name: str) -> str:
    """Convert album/subalbum names to valid filenames."""
    # Convert to lowercase and replace spaces/special chars with hyphens
    filename = name.lower()
    filename = ''.join(c if c.isalnum() else '-' for c in filename)
    filename = '-'.join(filter(None, filename.split('-')))  # Remove empty parts
    return filename

def create_stub_file(file_path: Path, title: str, subalbum: str = None):
    """Create a stub .md file with proper front matter."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    front_matter = f"""---
layout: gallery
title: "{title}"
"""
    
    if subalbum:
        front_matter += f'subalbum: "{subalbum}"\n'
    
    front_matter += "---\n"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(front_matter)
    
    print(f"✅ Created: {file_path}")

def generate_stubs(gallery_config: Dict[str, Any], output_dir: str):
    """Generate all stub files from gallery configuration."""
    albums_dir = Path(output_dir)
    
    print(f"🎯 Generating stub files in: {albums_dir}")
    print("=" * 50)
    
    albums = gallery_config.get('albums', [])
    
    for album in albums:
        album_name = album.get('name', '')
        if not album_name:
            continue
            
        # Create main album directory and stub file
        album_filename = sanitize_filename(album_name)
        album_file_path = albums_dir / f"{album_filename}.md"
        
        create_stub_file(album_file_path, album_name)
        
        # Process subalbums
        subalbums = album.get('subalbums', [])
        for subalbum in subalbums:
            subalbum_name = subalbum.get('name', '')
            if not subalbum_name:
                continue
                
            # Create subalbum directory and stub file
            subalbum_filename = sanitize_filename(subalbum_name)
            subalbum_dir = albums_dir / album_filename
            subalbum_file_path = subalbum_dir / f"{subalbum_filename}.md"
            
            create_stub_file(subalbum_file_path, album_name, subalbum_name)
    
    print("=" * 50)
    print("🎉 All stub files generated successfully!")
    print(f"📁 Files created in: {albums_dir}")

def print_directory_structure(output_dir: str):
    """Print the generated directory structure."""
    albums_dir = Path(output_dir)
    
    print("\n📂 Generated directory structure:")
    print("=" * 40)
    
    def print_tree(directory: Path, prefix: str = ""):
        if not directory.exists():
            return
            
        items = sorted(directory.iterdir())
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item.name}")
            
            if item.is_dir():
                next_prefix = prefix + ("    " if is_last else "│   ")
                print_tree(item, next_prefix)
    
    print("albums/")
    print_tree(albums_dir, "")

def main():
    """Main function to handle command line arguments and run the generator."""
    # Parse command line arguments
    gallery_file = sys.argv[1] if len(sys.argv) > 1 else "_data/gallery.yml"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "albums"
    
    print("🎨 Jekyll Gallery Stub Generator")
    print("=" * 50)
    print(f"📖 Gallery config: {gallery_file}")
    print(f"📁 Output directory: {output_dir}")
    print()
    
    # Load gallery configuration
    gallery_config = load_gallery_config(gallery_file)
    
    # Generate stub files
    generate_stubs(gallery_config, output_dir)
    
    # Show directory structure
    print_directory_structure(output_dir)
    
    print("\n💡 Next steps:")
    print("1. Copy the generated 'albums/' directory to your Jekyll site")
    print("2. Commit and push to GitHub")
    print("3. Your gallery URLs should now work on GitHub Pages!")
    print("\n🔗 URLs that will work:")
    
    # Show example URLs
    albums = gallery_config.get('albums', [])
    base_url = "https://josedihego.net/siteclaraoliveira"  # You can make this configurable
    
    for album in albums[:3]:  # Show first 3 examples
        album_name = album.get('name', '')
        album_filename = sanitize_filename(album_name)
        print(f"   {base_url}/albums/{album_filename}/")
        
        subalbums = album.get('subalbums', [])
        for subalbum in subalbums[:2]:  # Show first 2 subalbums
            subalbum_name = subalbum.get('name', '')
            subalbum_filename = sanitize_filename(subalbum_name)
            print(f"   {base_url}/albums/{album_filename}/{subalbum_filename}/")
    
    if len(albums) > 3:
        print("   ... and more!")

if __name__ == "__main__":
    main()