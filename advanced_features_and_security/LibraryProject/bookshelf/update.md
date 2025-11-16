
# update.md

```markdown
# Update Operation

## Command

```python
book = Book.objects.get(title="1984") ##more like SELECT command
book.title = "Nineteen Eighty-Four"
book.save()
print(Book.objects.get(pk=book.pk).title) ##book.pk returns the primary-key value for that Book instance; get(pk=book.pk) fetches the same row by primary key. print(... .title) then prints the title column value from that row.
##Select the book row we just changed by its primary key (id) from the database, return the Book object, and then get its title value.
