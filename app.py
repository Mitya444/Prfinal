from flask import Flask, render_template, send_file
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

app = Flask(__name__)

engine = create_engine('sqlite:///books.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
current_directory = os.path.dirname(__file__)
pdf_folder = os.path.join(current_directory, 'static')


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    creator = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)
    image_url = Column(String(100))
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book {self.id}: {self.title}>"


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    photo = Column(String(250))
    genres = Column(String(250))
    birth_year = Column(Integer)

    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"


Base.metadata.create_all(engine)

book_data = [
    {"title": "Пригоди Шерлока Холмса", "creator": "Артур Конан Дойль", "description": "Пригоди Шерлока Холмса - серія детективних оповідань, у яких головним героєм є знаменитий детектив Шерлок Холмс, що розслідує різні загадкові злочини в Лондоні кінця XIX століття.", "image_url": "https://static.yakaboo.ua/media/cloudflare/product/webp/600x840/i/m/img383_1_43.jpg"},
    {"title": "Дракула", "creator": "Брэм Стокер", "description": "Дракула - роман жахів, який розповідає про вампіра на ім'я Дракула і його вплив на життя мешканців Лондона. Це класичне твір вважається одним із найвідоміших у світовій літературі та суттєво вплинув на жанр жахів.", "image_url": "https://static.yakaboo.ua/media/cloudflare/product/webp/600x840/i/s/isbn_978_617_7914_61_6_0.jpg"},
    {"title": "Код Да Вінчі", "creator": "Ден Браун", "description": "Код Да Вінчі - трилер, у якому розслідується загадкове вбивство і водночас розкриваються таємниці, пов'язані з таємними товариствами, мистецтвом та релігією. Роман прославився своїми заплутаними загадками і непередбачуваним сюжетом.", "image_url": "https://upload.wikimedia.org/wikipedia/uk/7/72/Da_vinci_code.jpg"},
    {"title": "ТРИ ТОВАРИЩА", "creator": "Еріх Марія Ремарк", "description": "ТРИ ТОВАРИЩА - роман, що описує життя трьох друзів в Німеччині в період після Першої світової війни. Книга торкається тем дружби, кохання, втрати та надії в складні історичні часи.", "image_url": "https://content.rozetka.com.ua/goods/images/big/262035943.jpg"},
    {"title": "Гаррі Поттер і філософський камінь", "creator": "Джоан Роулінг", "description": "Гаррі Поттер і філософський камінь - це перша книга з сірії про юного чарівника Гаррі Поттера, написана Джоан Роулінг. У цій книзі Гаррі дізнається про своє справжнє походження та вступає до Хогвартсу, школи чарівництва і чаклунства.", "image_url": "https://static.yakaboo.ua/media/cloudflare/product/webp/600x840/4/1/41_1_131.jpg"},
    {"title": "Дванадцять стільців", "creator": "Ілья Ільф, Євген Петров", "description": "Дванадцять стільців - роман-фельетон, у якому описуються пригоди молодої людини у пошуках втраченого спадку. Книга прославилася своїми яскравими персонажами та гумором.", "image_url": "https://readukrainianbooks.com/uploads/posts/books/2/8/8/3/zolote-telja-yevgen-petrovich-petrov.jpg"},
    {"title": "Собаче серце", "creator": "Михайло Булгаков", "description": "Собаче серце - алегорична повість, в якій описується історія професора, який вживляє в людину собаче серце, що призводить до несподіваних наслідків та роздумів про людську природу.", "image_url": "https://static.yakaboo.ua/media/catalog/product/c/o/cover_468_7.jpg"},
    {"title": "Казки Пушкіна", "creator": "Олександр Пушкін", "description": "Казки Пушкіна - збірка казок російського поета", "image_url": "https://knygy.com.ua/pix/b3/e8/2b/b3e82bcc7fdeef9ca96c9b91addfc142.jpg"},
    {"title": "Граф Монте-Крісто", "creator": "Олександр Дюма", "description": "Граф Монте-Крісто - роман-пригода, що розповідає історію Едмонда Дантеса, який, опинившись невинно засудженим, вчиняє дивовижний втечу з в'язниці і починає мстити своїм образникам", "image_url": "https://lavkababuin.com/image/cachewebp/alias/graf-monte-kristo-570081/graf-monte-kristo-570081-main-1000x1000.webp"},
    {"title": "Двадцять тисяч льє під водою", "creator": "Жюль Верн", "description": "Двадцять тисяч льє під водою - це класичний науково-фантастичний роман, написаний французьким письменником Жюлем Верном та опублікований в 1870 році. Роман розповідає історію капітана Немо і його підводної акустичної човна Наутилус", "image_url": "https://static.yakaboo.ua/media/cloudflare/product/webp/600x840/i/m/img_11966.jpg"},
    {"title": "Гаррі Поттер та Таємна кімната", "creator": "Джоан Роулінг", "description": "Друга книга серії про Гаррі Поттера. В ній Гаррі Поттер повертається до Хогвартсу для другого навчального року, де він та його друзі досліджують таємниці та загадки, пов'язані з Таємною кімнатою.", "image_url": "https://static.yakaboo.ua/media/cloudflare/product/webp/600x840/4/2/42_1_302.jpg"},
    {"title": "Собака Баскервілів", "creator": "Артур Конан Дойль", "description": "Собака Баскервілів - роман, де доктор Ватсон і Шерлок Холмс розслідують загадкове вбивство із залученням легендарного пса-відьмака. Ця книга стала одним із найвідоміших творів Артура Конана Дойля про Шерлока Холмса.", "image_url": "https://knigogo.com.ua/wp-content/uploads/2018/09/sobaka-baskerviliv-36621582-237x327.jpg"},
    {"title": "80 днів навколо світу", "creator": "Жюль Верн", "description": "80 днів навколо світу - роман, який розповідає історію Філеаса Фогга і його слуги Паспарту, які викликають удивлення світу, подолавши всіх 80 днів, щоб об'їхати світ. Ця книга вважається одним із найвідоміших творів Жюля Верна та стала класикою пригодницького жанру.", "image_url": "https://akonit.net/image/cache/catalog/feed_3/2289-296378-1000x1000.jpg"}


]

author_data = [
    {"name": "Артур Конан Дойль", "books": [1], "birth_year": 1859, "genres": ["детектив", "пригоди"], "photo": "https://upload.wikimedia.org/wikipedia/commons/b/bd/Arthur_Conan_Doyle_by_Walter_Benington%2C_1914.png"},
    {"name": "Брэм Стокер", "books": [2], "birth_year": 1847, "genres": ["жахи", "готика"], "photo": "https://upload.wikimedia.org/wikipedia/commons/3/34/Bram_Stoker_1906.jpg"},
    {"name": "Ден Браун", "books": [3], "birth_year": 1964, "genres": ["трилер", "містика"], "photo": "https://upload.wikimedia.org/wikipedia/commons/8/8b/Dan_Brown_bookjacket_cropped.jpg"},
    {"name": "Еріх Марія Ремарк", "books": [4], "birth_year": 1898, "genres": ["роман", "драма"], "photo": "https://library.kname.edu.ua/images/images/%D0%A0%D0%B5%D0%BC%D0%B0%D1%80%D0%BA.jpg"},
    {"name": "Джоан Роулінг", "books": [5, 11], "birth_year": 1965, "genres": ["фентезі", "пригоди"], "photo": "https://static.yakaboo.ua/media/entity/author/f/i/file_15_4.jpg"},
    {"name": "Ілья Ільф, Євген Петров", "books": [6], "birth_year": 1897_1893, "genres": ["фельетон", "пригоди"], "photo": "https://odnb.odessa.ua/img/novini_2017/1868/1.jpg"},
    {"name": "Михайло Булгаков", "books": [7], "birth_year": 1891, "genres": ["алегорія", "фантастика"], "photo": "https://gordonua.com/img/forall/users/127/12733/c632a5686c148c39087f3131f59a5b9e.jpg"},
    {"name": "Олександр Пушкін", "books": [8], "birth_year": 1799, "genres": ["казка", "поезія"], "photo": "https://upload.wikimedia.org/wikipedia/commons/7/7a/Orest_Kiprensky_-_%D0%9F%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82_%D0%BF%D0%BE%D1%8D%D1%82%D0%B0_%D0%90.%D0%A1.%D0%9F%D1%83%D1%88%D0%BA%D0%B8%D0%BD%D0%B0_-_Google_Art_Project.jpg"},
    {"name": "Олександр Дюма", "books": [9], "birth_year": 1802, "genres": ["пригоди", "роман"], "photo": "https://book24.ua/upload/iblock/f6e/f6e905e44e7550a23ba09e06f9827752.jpg"},
    {"name": "Жюль Верн", "books": [10], "birth_year": 1828, "genres": ["пригоди", "наукова фантастика"], "photo": "https://upload.wikimedia.org/wikipedia/commons/f/f5/Jules_verne_nypl.jpg"},
]


def init_db():
    session = Session()
    if session.query(Book).count() < 10:
        for i, data in enumerate(book_data):
            author_name = data["creator"]
            author_id = None
            author_instance = session.query(Author).filter_by(name=author_name).first()
            if author_instance:
                author_id = author_instance.id
            else: 
                new_author_data = next((auth for auth in author_data if auth["name"] == author_name), None)
                if new_author_data:
                    new_author = Author(name=new_author_data["name"], birth_year=new_author_data["birth_year"], genres=', '.join(new_author_data["genres"]), photo=new_author_data["photo"])
                    session.add(new_author)
                    session.commit()
                    author_id = new_author.id
            book_instance = Book(title=data["title"], creator=data["creator"], description=data["description"], image_url=data["image_url"], author_id=author_id)
            session.add(book_instance)
        session.commit()


@app.route('/download_book/<int:book_id>')
def download_book(book_id):
    session = Session()
    book_datas = session.query(Book).filter_by(id=book_id).first()
    if book_datas:
        pdf_path = os.path.join(pdf_folder, f'{book_id}.pdf')
        if os.path.exists(pdf_path):
            try:
                return send_file(pdf_path, as_attachment=True)
            except Exception as e:
                return str(e)
        else:
            return "Файл не найден"
    else:
        return "Книга не найдена"


@app.route('/')
def index():
    session = Session()
    try:
        books = session.query(Book).all()
        return render_template('index.html', books=books)
    except Exception as e:
        return f"Помилка при отриманні даних з бази даних: {e}"
    finally:
        session.close()


@app.route('/book/<int:book_id>')
def book(book_id):
    session = Session()
    try:
        book_dataa = session.query(Book).filter_by(id=book_id).first()
        if book_dataa:
            return render_template('book.html', book=book_dataa)
        else:
            return "Книга не найдена", 404
    finally:
        session.close()


@app.route('/author/<int:author_id>')
def author(author_id):
    session = Session()
    try:
        author_dataa = session.query(Author).filter_by(id=author_id).first()
        author_books = author_dataa.books
        return render_template('authorinfo.html', author_data=author_dataa, author_books=author_books)
    except Exception as e:
        return f"Помилка при отриманні даних з бази даних: {e}"
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
