import ast

def check_file(file_path):
    print(f"\n=== Checking {file_path} ===")
    try:
        with open(file_path, "r") as f:
            content = f.read()
        tree = ast.parse(content)
        
        # Check for permission_required import
        has_import = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if (node.module == 'django.contrib.auth.decorators' and 
                    any(alias.name == 'permission_required' for alias in node.names)):
                    has_import = True
                    print(f"✓ Found: from {node.module} import permission_required")
                    break
        
        # Check for usage
        has_usage = "permission_required(" in content
        print(f"✓ permission_required used in code: {has_usage}")
        
        # Show exact lines where permission_required is used
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'permission_required(' in line:
                print(f"  Line {i}: {line.strip()}")
        
        return has_import and has_usage
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Test both files
result1 = check_file("relationship_app/views.py")
result2 = check_file("bookshelf/views.py")

print(f"\n=== SUMMARY ===")
print(f"relationship_app/views.py passes: {result1}")
print(f"bookshelf/views.py passes: {result2}")
print(f"Both files have permission_required: {result1 and result2}")
