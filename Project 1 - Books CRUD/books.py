from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{title}")
async def read_book(title: str):
    for book in BOOKS:
        if book["title"].casefold() == title.casefold():
            return book


@app.get("/books/")
async def read_category_by_query(category: str):
    books = []
    for book in BOOKS:
        if book["category"].casefold() == category.casefold():
            books.append(book)
    return books


@app.get("/books/byauthor/{author}")
async def get_all_books_by_author(author: str):
    books = []
    for book in BOOKS:
        if book["author"].casefold() == author.casefold():
            books.append(book)
    return books


@app.get("/books/{author}/")
async def read_author_category_by_query(author: str, category: str):
    books = []
    for book in BOOKS:
        if book["category"].casefold() == category.casefold() and book["author"].casefold() == author.casefold():
            books.append(book)
    return books


@app.post("/books/create_book")
async def create_new_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"].casefold() == updated_book["title"].casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{title}")
async def delete_book(title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"].casefold() == title.casefold():
            BOOKS.pop(i)
            break
