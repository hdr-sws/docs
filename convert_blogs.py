#!/usr/bin/env python3
import os
import re
import shutil
from datetime import datetime

# Source directory with markdown files
source_dir = "first version of docs/Blog articles/Ready to publish"

# Target directory for MDX files
target_base_dir = "blog"

# Categories mapping with icons (using Font Awesome icons)
categories = {
    "bitcoin": {
        "keywords": ["What is Bitcoin", "Sending Bitcoin", "All the Ways to Buy Bitcoin", "How to Buy Bitcoin"],
        "icon": "bitcoin-sign"
    },
    "security": {
        "keywords": ["Seed Phrase Security", "Withdrawing Bitcoin"],
        "icon": "shield"
    },
    "getting-started": {
        "keywords": ["Getting Started with Bitcoin"],
        "icon": "rocket"
    }
}

# Create category directories if they don't exist
for category in categories.keys():
    category_dir = os.path.join(target_base_dir, category)
    os.makedirs(category_dir, exist_ok=True)

def clean_filename(title):
    """Convert title to a clean filename."""
    # Remove special characters and convert spaces to hyphens
    clean = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    clean = re.sub(r'\s+', '-', clean).lower()
    return clean

def get_category_and_icon(title):
    """Determine the category based on the title."""
    for category, info in categories.items():
        for keyword in info["keywords"]:
            if keyword in title:
                return category, info["icon"]
    return "general", "book-open"  # Default category and icon

def convert_to_mdx(md_file, output_dir):
    """Convert markdown file to MDX with frontmatter."""
    # Read the markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title (first heading)
    title_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(md_file).replace('.md', '')
    
    # Extract summary if available
    summary_match = re.search(r'^## Summary\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.MULTILINE)
    description = summary_match.group(1).strip() if summary_match else ""
    
    # If no summary, use first paragraph
    if not description:
        paragraph_match = re.search(r'\n\n(.*?)\n\n', content, re.DOTALL | re.MULTILINE)
        if paragraph_match:
            description = paragraph_match.group(1).strip()
    
    # Truncate description if too long
    if len(description) > 160:
        description = description[:157] + "..."
    
    # Determine category and icon
    category, icon = get_category_and_icon(title)
    
    # Generate frontmatter
    frontmatter = f"""---
title: '{title}'
description: '{description}'
icon: '{icon}'
---

"""
    
    # Clean up the content (removing title since it will be in frontmatter)
    if title_match:
        content = content.replace(title_match.group(0), "", 1)
    
    # Combine frontmatter and content
    mdx_content = frontmatter + content.strip()
    
    # Create clean filename
    clean_name = clean_filename(title) + ".mdx"
    
    # Create output path
    output_path = os.path.join(output_dir, category, clean_name)
    
    # Make sure category directory exists
    os.makedirs(os.path.join(output_dir, category), exist_ok=True)
    
    # Write the MDX file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(mdx_content)
    
    print(f"Converted {os.path.basename(md_file)} → {output_path}")
    
    return output_path, category

# Process all markdown files
converted_files = []
for filename in os.listdir(source_dir):
    if filename.endswith(".md"):
        md_path = os.path.join(source_dir, filename)
        output_path, category = convert_to_mdx(md_path, target_base_dir)
        converted_files.append((output_path, category))

print(f"\nSuccessfully converted {len(converted_files)} files.")

# Print summary of files by category
categories_count = {}
for _, category in converted_files:
    categories_count[category] = categories_count.get(category, 0) + 1

print("\nFiles by category:")
for category, count in categories_count.items():
    print(f"- {category}: {count} files") 