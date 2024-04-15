import pytest


def test_equal_not_equal():
    assert 1 == 1
    assert 1 != 2
    
def test_is_instance():
    assert isinstance(1, int)
    assert isinstance(1.0, float)
    assert isinstance("hello", str)
    
def test_boolean():
    assert True
    assert not False
    assert ('hello' == 'hello') is True
    
def test_in_not_in():
    assert 1 in [1, 2, 3]
    assert 4 not in [1, 2, 3]
    
def test_greater_less():
    assert 2 > 1
    assert 1 < 2
    assert 1 >= 1
    assert 1 <= 1
    
def test_is_not():
    assert 1 != None
    assert 1 != 2
    assert 1 != "hello"
    assert 1 != [1, 2, 3]

    
def test_not():
    assert not 1 == 2
    assert not 1 == 3
    assert not 1 == "hello"
    assert not 1 == [1, 2, 3]
    
def test_assert_raises():
    with pytest.raises(ValueError):
        raise ValueError("This is a ValueError")
    with pytest.raises(TypeError):
        raise TypeError("This is a TypeError")
    with pytest.raises(ZeroDivisionError):
        raise ZeroDivisionError("This is a ZeroDivisionError")
    

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, year: int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.year = year
        
@pytest.fixture
def student():
    return Student("John", "Doe", "Computer Science", 2023)

def test_student(student):
    assert student.first_name == "John"
    assert student.last_name == "Doe"
    assert student.major == "Computer Science"
    assert student.year == 2023
