import os
import shutil
import re

base_dir = "/home/epmq/Desktop/Projects/Agentic-Orquestrator/antigravity-core/skills"

for skill_name in os.listdir(base_dir):
    skill_path = os.path.join(base_dir, skill_name)
    if not os.path.isdir(skill_path):
        continue
        
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md_path):
        continue
        
    # Find all .md files at root of skill (except SKILL.md)
    root_md_files = [f for f in os.listdir(skill_path) if f.endswith('.md') and f != 'SKILL.md' and os.path.isfile(os.path.join(skill_path, f))]
    
    refs_dir = os.path.join(skill_path, "references")
    
    # Also find files already in references
    existing_refs = []
    if os.path.exists(refs_dir):
        existing_refs = [f for f in os.listdir(refs_dir) if f.endswith('.md')]
        
    all_refs = root_md_files + existing_refs
    
    if all_refs:
        os.makedirs(refs_dir, exist_ok=True)
        
        # Move root files
        for f in root_md_files:
            shutil.move(os.path.join(skill_path, f), os.path.join(refs_dir, f))
            
        # Update SKILL.md
        with open(skill_md_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        modified = False
        
        # Check if 📑 Content Map exists
        if "📑 Content Map" not in content:
            # Create the section at the end of the file
            content_map_section = "\n\n## 📑 Content Map\n\n| File | Description |\n|------|-------------|\n| `SKILL.md` | Main Skill Definition |\n"
            for ref in all_refs:
                content_map_section += f"| `references/{ref}` | Specialized references for {ref.replace('.md', '')} |\n"
            
            content += content_map_section
            modified = True
        else:
            # If it exists, let's update occurrences in the SKILL.md for the ones we just moved.
            for f in root_md_files:
                # Naive replace inside table
                if f"`{f}`" in content:
                    content = content.replace(f"`{f}`", f"`references/{f}`")
                    modified = True
                elif f in content and f"references/{f}" not in content:
                    content = content.replace(f, f"references/{f}")
                    modified = True
                    
        if modified:
            with open(skill_md_path, 'w', encoding='utf-8') as file:
                file.write(content)
                
    else:
        # No extra .md files at all
        with open(skill_md_path, 'r', encoding='utf-8') as file:
            content = file.read()
        if "📑 Content Map" not in content:
            content += "\n\n## 📑 Content Map\n\n| File | Description |\n|------|-------------|\n| `SKILL.md` | Main Skill Definition |\n"
            with open(skill_md_path, 'w', encoding='utf-8') as file:
                file.write(content)

print("Skills reorganized successfully.")
