from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    published_date: int
    rating: int

    def __init__(self, id, title, author, description, published_date, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.published_date = published_date
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    published_date: int = Field(gt=1900, lt=2031)
    rating: int = Field(gt=0, lt=6)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Vedran',
                'description': 'A new description',
                'published_date': 2023,
                'rating': 5
            }
        }


BOOKS = [
    Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "A story of love and the American Dream", 1925, 4),
    Book(2, "To Kill a Mockingbird", "Harper Lee", "A powerful story of racial injustice and moral growth", 1960, 5),
    Book(3, "1984", "George Orwell", "A dystopian novel exploring surveillance and control", 1949, 4),
    Book(4, "Pride and Prejudice", "Jane Austen", "A classic tale of love and societal norms", 1813, 3),
    Book(5, "The Catcher in the Rye", "J.D. Salinger", "A coming-of-age novel with themes of alienation", 1951, 2),
    Book(6, "The Lord of the Rings", "J.R.R. Tolkien", "An epic fantasy adventure in Middle-earth", 1954, 5),
    Book(7, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Introduction to the wizarding world", 1997, 4),
    Book(8, "The Hobbit", "J.R.R. Tolkien", "A prelude to The Lord of the Rings, featuring Bilbo Baggins", 1937, 4),
    Book(9, "Brave New World", "Aldous Huxley", "An exploration of a dystopian future society", 1932, 5),
    Book(10, "The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "A humorous science fiction series", 1979, 4)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_published_date(published_date: int = Query(gt=1900, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)

    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')