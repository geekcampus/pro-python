from collections import namedtuple


def test_namedtuple():
    Point = namedtuple("Point", ["x", "y"])
    p = Point(x=1, y=2)
    assert p.x == 1
    assert p.y == 2


from typing import NamedTuple


def test_NamedTuple():
    class Point(NamedTuple):
        x: int
        y: int

    p = Point(x=1, y=2)
    assert p.x == 1
    assert p.y == 2


def test_classic_class():
    import functools

    @functools.total_ordering
    class PhoneNumber:
        def __init__(self, areaCode: int, prefix: int, lineNum: int):
            self.areaCode = areaCode
            self.prefix = prefix
            self.lineNum = lineNum

        def __eq__(self, other):
            if self is other:
                return True
            if not isinstance(other, PhoneNumber):
                return False

            return (
                self.areaCode == other.areaCode
                and self.prefix == other.prefix
                and self.lineNum == other.lineNum
            )

        def __hash__(self):
            # 里面的 tuple 是可 hash 的.
            return hash(self.as_tuple())

        def __repr__(self):
            return f"{self.areaCode:03}-{self.prefix:03}-{self.lineNum:04}"

        def as_tuple(self):
            return (self.areaCode, self.prefix, self.lineNum)

        def as_dict(self):
            return {
                "areaCode": self.areaCode,
                "prefix": self.prefix,
                "lineNum": self.lineNum,
            }

        def __copy__(self):
            return PhoneNumber(
                areaCode=self.areaCode, prefix=self.prefix, lineNum=self.lineNum
            )

        def __lt__(self, other):
            if not isinstance(other, PhoneNumber):
                return False
            return self.as_tuple() < other.as_tuple()

    pn1 = PhoneNumber(areaCode=707, prefix=867, lineNum=5309)
    assert repr(pn1) == "707-867-5309"
    assert str(pn1) == "707-867-5309"
    pn2 = PhoneNumber(areaCode=707, prefix=867, lineNum=5309)
    assert pn1 == pn2
    assert hash(pn1) == hash(pn2)
    import copy

    pn3 = copy.copy(pn1)
    assert pn3 == pn2
    assert pn1.as_dict() == {"areaCode": 707, "prefix": 867, "lineNum": 5309}
    assert pn1.as_tuple() == (707, 867, 5309)
    pn4 = PhoneNumber(areaCode=708, prefix=867, lineNum=5309)
    assert pn1 < pn4
    assert pn4 > pn1


def test_dataclass():

    import dataclasses

    @dataclasses.dataclass(order=True, unsafe_hash=True)
    class PhoneNumber:
        areaCode: int
        prefix: int
        lineNum: int

    pn1 = PhoneNumber(areaCode=707, prefix=867, lineNum=5309)
    assert "PhoneNumber(areaCode=707, prefix=867, lineNum=5309)" in repr(pn1)
    pn2 = PhoneNumber(areaCode=707, prefix=867, lineNum=5309)
    assert pn1 == pn2
    assert hash(pn1) == hash(pn2)
    import copy

    pn3 = copy.copy(pn1)
    assert pn3 == pn2
    assert dataclasses.asdict(pn1) == {"areaCode": 707, "prefix": 867, "lineNum": 5309}
    assert dataclasses.astuple(pn1) == (707, 867, 5309)
    pn4 = PhoneNumber(areaCode=708, prefix=867, lineNum=5309)
    assert pn1 < pn4
    assert pn4 > pn1
    # replace 用于创建副本,并同时进行更新
    pn5 = dataclasses.replace(pn1, lineNum=2019)
    assert dataclasses.astuple(pn5) == (707, 867, 2019)


def test_union():
    from typing import Union, Optional

    assert Union[None, int] == Optional[int]
    assert Union[int, int, str, str] == Union[int, str]
    assert Union[int, int, str, str] == Union[str, int]
    assert Union[int] == int
    assert Union[Union[int, str], float] == Union[int, str, float]


def test_http_method_enum():
    import enum

    class HttpMethod(str, enum.Enum):
        GET = "GET"
        POST = "POST"
        PUT = "PUT"
        PATCH = "PATCH"
        HEAD = "HEAD"
        OPTIONS = "OPTIONS"
        DELETE = "DELETE"

    def request(method: HttpMethod):
        pass

    assert HttpMethod.GET.upper() == "GET"
    assert HttpMethod.DELETE.upper() == "DELETE"


def test_http_method_literal():
    from typing import Literal

    HttpMethod = Literal["GET", "POST", "PUT", "HEAD", "PATCH", "OPTIONS" "DELETE"]

    def request(method: HttpMethod):
      pass


def test_final():
  from typing import Final
  MY_LUCKY_SEED: Final[int] = 4096

  MY_LUCKY_SEED = 240 # 报错: 'MY_LUCKY_SEED' is 'Final' and could not be reassigned

  class Base:
      STATUS_ON:Final = 1

  class Sub(Base):
      STATUS_ON = 2 # 报错: 'Base.STATUS_ON' is 'Final' and could not be reassigned

def test_noreturn():
    import pytest
    from typing import NoReturn
    def abort(msg:str)-> NoReturn:
        raise RuntimeError(msg)
    with pytest.raises(RuntimeError):
      abort("段错误")

def test_tuple():
    from typing import Tuple

    def get_host_and_port() -> Tuple[str,int]:
        return 'qq.com',443

    host,port = get_host_and_port()
    assert host == "qq.com"
    assert port == 443


def test_callable():
    from typing import Callable,Union
    def join(a:str,b:str) -> str:
        return f"{a}:{b}"

    def make_key_maker(prefix:str,join:Callable[[str,str], str]):
        key:str = prefix
        def make(part:Union[str,int]) -> str:
            nonlocal key
            key = join(key,str(part))
            return key
        return make

    todo_key_maker = make_key_maker("todo", join=join)
    assert todo_key_maker(1) == "todo:1"
    assert todo_key_maker('tag') == "todo:1:tag"
    assert todo_key_maker('color') == "todo:1:tag:color"







def test_type():
    from typing import Type
    # from django.db import models
    #
    # def get_content_type(model_class:Type[models.Model]):
    #   return ContentType.objects.get_for_model(model_class)

def test_generic():
    from typing import TypeVar, Generic,Optional
    K = TypeVar('K')
    V = TypeVar('V')
    class Map(Generic[K,V]):
        def __init__(self):
            self.data = {}

        def __getitem__(self,key: K) -> Optional[V]:
          return self.data[key]

        def __contains__(self, key:K) -> bool:
          return key in self.data

        def __setitem__(self, key:K, value:V) -> None:
          self.data[key] = value

    m1:Map[int,int] = Map()
    m1['a'] = 2 #警告: Expected type 'int' (matched generic type 'K'), got 'str' instead
    m1[2] = 'b' #警告:  Expected type 'int' (matched generic type 'V'), got 'str' instead


def test_covariant():
    import re
    import pytest
    from typing import List
    class Animal:pass
    class Dog(Animal):
        def walk(self):pass
    class Bird(Animal):pass

    dogs:List[Dog] = []
    animals: List[Animal] = dogs

    bird = Bird()
    animals.append(bird)

    with pytest.raises(AttributeError,match=re.escape("'Bird' object has no attribute 'walk'")):
        dogs[0].walk()
