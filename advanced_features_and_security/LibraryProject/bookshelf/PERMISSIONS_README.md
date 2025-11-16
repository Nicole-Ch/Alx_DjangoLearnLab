# Permissions and Groups Setup

## Custom Permissions Added to Book Model

- `can_view` - Can view books
- `can_create` - Can create books  
- `can_edit` - Can edit books
- `can_delete` - Can delete books

## Groups Created

- **Viewers**: can_view permission only

- **Editors**: can_view, can_create, can_edit permissions
- **Admins**: All permissions (can_view, can_create, can_edit, can_delete)

## Views Protected with Permissions

- `book_list()` - Protected with @permission_required('bookshelf.can_view')
- `book_create()` - Protected with @permission_required('bookshelf.can_create')
- `book_edit()` - Protected with @permission_required('bookshelf.can_edit')
- `book_delete()` - Protected with @permission_required('bookshelf.can_delete')

## Setup Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py setup_groups
