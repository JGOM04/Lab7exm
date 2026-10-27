import pytest
import library
import main
from library import Library
from book import Book
from user import User


@pytest.fixture
def biblioteca():
    lib = Library()
    lib.add_book(Book("1984", "George Orwell", 1949, "ISBN001"))
    lib.add_book(Book("To Kill a Mockingbird", "Harper Lee", 1960, "ISBN002"))
    lib.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, "ISBN003"))
    lib.add_user(User("Anna", "U001"))
    lib.add_user(User("Juan", "U002"))
    return lib


def test_prestar_libro(biblioteca):
    biblioteca.borrow_book("U001", "ISBN001")
    assert biblioteca._find_book("ISBN001").borrowed is True


def test_devolver_libro(biblioteca):
    biblioteca.borrow_book("U001", "ISBN001")
    biblioteca.return_book("U001", "ISBN001")
    assert biblioteca._find_book("ISBN001").borrowed is False


# =====================================================================
# 1. monkeypatch.setattr() Sustituye TODO el atributo "settings" del módulo library por otro
# diccionario que esta desactivados los prestamos 
# =====================================================================
def test_setattr_desactiva_prestamos(monkeypatch, biblioteca):
    monkeypatch.setattr(library, "settings", {"loans_enabled": False})
    biblioteca.borrow_book("U001", "ISBN001")
    assert biblioteca._find_book("ISBN001").borrowed is False


# =====================================================================
# 2. monkeypatch.delattr() Elimina temporalmente el método borrow de la clase Book.
# borrow_book() lo necesita, así que debe fallar con AttributeError.
# =====================================================================
def test_delattr_sin_metodo_borrow(monkeypatch, biblioteca):
    monkeypatch.delattr(Book, "borrow")
    with pytest.raises(AttributeError):
        biblioteca.borrow_book("U001", "ISBN001")


# =====================================================================
# 3. monkeypatch.setitem() cambia SOLO la llave "loans_enabled" del diccionario settings.
# =====================================================================
def test_setitem_desactiva_prestamos(monkeypatch, biblioteca):
    monkeypatch.setitem(library.settings, "loans_enabled", False)
    biblioteca.borrow_book("U002", "ISBN002")
    assert biblioteca._find_book("ISBN002").borrowed is False
    assert biblioteca._find_user("U002").get_history() == []


# =====================================================================
# 4 y 5. MARCADORES (registrado en pytest.ini)
#Solo la primera prueba lleva el marcador.
# =====================================================================
@pytest.mark.prestamos
def test_historial_registra_prestamo(biblioteca):
    biblioteca.borrow_book("U001", "ISBN001")
    historial = biblioteca._find_user("U001").get_history()
    assert len(historial) == 1
    assert "1984" in historial[0]


def test_usuario_nuevo_sin_historial():
    usuario = User("Mary", "U003")
    assert usuario.get_history() == []


# =====================================================================
# 6. PARAMETRIZE
# Una sola función prueba tres ISBN distintos.
# =====================================================================
@pytest.mark.parametrize("isbn, titulo", [
    ("ISBN001", "1984"),
    ("ISBN002", "To Kill a Mockingbird"),
    ("ISBN003", "The Great Gatsby"),
])
def test_buscar_libro(biblioteca, isbn, titulo):
    assert biblioteca._find_book(isbn).title == titulo


# =====================================================================
# 8. COBERTURA DE CAJA BLANCA
# El reporte marcaba book.py línea 16 como no ejecutada: el raise
# cuando se devuelve un libro que NO está prestado.
# =====================================================================
def test_devolver_libro_no_prestado(biblioteca):
    with pytest.raises(ValueError, match="not currently borrowed"):
        biblioteca.return_book("U001", "ISBN001")


# =====================================================================
# 9. pytest.raises()
# Prestar un libro que ya está prestado debe lanzar ValueError.
# =====================================================================
def test_prestar_libro_ya_prestado(biblioteca):
    biblioteca.borrow_book("U001", "ISBN001")
    with pytest.raises(ValueError, match="already borrowed"):
        biblioteca.borrow_book("U002", "ISBN001")


# =====================================================================
# 10. try-except
# El único try-except está en main.py: atrapa el ValueError y muestra
# "Error: ...". Library NO tiene try-except, así que ahí se propaga.
# =====================================================================
def test_excepcion_capturada_en_main(monkeypatch, capsys):
    # Respuestas simuladas para cada input(): opción, ISBN, usuario, salir
    respuestas = iter(["2", "ISBN999", "U001", "0"])
    monkeypatch.setattr("builtins.input", lambda mensaje: next(respuestas))
    main.run()  # no truena: el except atrapa el error
    captured = capsys.readouterr()
    assert "Error: Book not found" in captured.out


def test_excepcion_se_propaga_en_library(biblioteca):
    with pytest.raises(ValueError, match="Book not found"):
        biblioteca.borrow_book("U001", "ISBN999")


# =====================================================================
# 11. capsys
# Prueba que el mensaje de préstamos desactivados se muestre correctamente.
# =====================================================================
def test_mensaje_prestamos_desactivados(monkeypatch, biblioteca, capsys):
    monkeypatch.setitem(library.settings, "loans_enabled", False)
    biblioteca.borrow_book("U001", "ISBN001")
    captured = capsys.readouterr()
    assert captured.err == "Loans are disabled\n"