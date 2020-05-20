"""
人民币金额小写转大写模块
rmb_toupper: 将金额转成大写字符串

https://www.acc5.com/news-shiwu/detail_11298.html
中国人民银行规定的支票填写规范：

一、中文大写金额数字到“元”为止的，在“元”之后、应写“整”（或“正”）字；在“角”之后，可以不写“整”（或“正”）字；大写金额数字有“分”的，“分”后面不写“整”（或“正”）字。

二、中文大写金额数字前应标明“人民币”字样，大写金额数字应紧接“人民币”字样填写，不得留有空白。大写金额数字前未印“人民币”字样的，应加填“人民币”三字，在票据和结算凭证大写金额栏内不得预印固定的“仟、佰、拾、万、仟、佰、拾、元、角、分”字样。

三、阿拉伯数字小写金额数字中有“0”时，中文大写应按照汉语语言规律、金额数字构成和防止涂改的要求进行书写。举例如下：

1、阿拉伯数字中间有“0”时，中文大写要写“零”字，如￥1409.50应写成人民币壹仟肆佰零玖元伍角；

2、阿拉伯数字中间连续有几个“0”时、中文大写金额中间可以只写一个“零”字，如￥6007.14应写成人民币陆仟零柒元壹角肆分；

3、阿拉伯金额数字万位和元位是“0”，或者数字中间连续有几个“0”，万位、元位也是“0”但千位、角位不是“0”时，中文大写金额中可以只写一个零字，也可以不“零”字，如￥1680.32应写成人民币壹仟陆佰捌拾元零叁角贰分，或者写成人民币壹仟陆佰捌拾元叁角贰分。又如￥107000.53应写成人民币壹拾万柒仟元零伍角叁分，或者写成人民币壹拾万零柒仟元伍角叁分；

4、阿拉伯金额数字角位是“0”而分位不是“0”时，中文大写金额“元”后面应“零”字，如￥16409.02应写成人民币壹万陆仟肆佰零玖元零贰分，又如￥325.04应写成人民币叁佰贰拾伍元零肆分。

四、阿拉伯小写金额数字前面均应填写人民币符号“￥”，阿拉伯小写金额数字要认真填写，不得连写分辨不清。

https://wiki.mbalib.com/wiki/%E3%80%8A%E4%BC%9A%E8%AE%A1%E5%9F%BA%E7%A1%80%E5%B7%A5%E4%BD%9C%E8%A7%84%E8%8C%83%E3%80%8B

　　（三）汉字大写数字金额如零、壹、贰、叁、肆、伍、陆、柒、捌、玖、拾、佰、仟、万、亿等，一律用正楷或者行书体书写，不得用0、一、二、三、四、五、六、七、八、九、十等简化字代替，不得任意自造简化字。大写金额数字到元或者角为止的，在“元”或者“角”字之后应当写“整”字或者“正”字；大写金额数字有分的，分字后面不写“整”或者“正”字。

　　（四）大写金额数字前未印有货币名称的，应当加填货币名称，货币名称与金额数字之间不得留有空白。

　　（五）阿拉伯金额数字中间有“0”时，汉字大写金额要写“零”字；阿拉伯数字金额中间连续有几个“0”时，汉字大写金额中可以只写一个“零”字；阿拉伯金额数字元位是“0”，或者数字中间连续有几个“0”、元位也是“0”但角位不是“0”时，汉字大写金额可以只写一个“零”字，也可以不写“零”字。
"""
import pytest
from collections import deque

# float double
# decimal 2^52 -1
# "
def _rmb_toupper_inner(amount:int,zero=False):
  metas = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
  bases = ['','拾','佰','仟','万']
  chars = deque()
  base = 0
  while amount > 0:
    div = amount // 10
    remain = amount % 10
    if remain:
      if zero:
        chars.appendleft('零')
        zero = False
      chars.appendleft(metas[remain]+bases[base])
    else:
      zero = zero or len(chars) > 0
    amount = div
    base += 1
  return ''.join(chars)



def rmb_toupper(amount:int):
  metas = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
  bases = ['','万','亿','万']
  base = 0
  comps = deque()
  zero = False
  while amount > 0:
    div = amount // 10000
    remain  = amount % 10000
    if remain:
      if zero:
        comps.appendleft('零')
        zero = False
      chars = _rmb_toupper_inner(remain)
      comps.appendleft(chars+ bases[base])
      zero = zero or remain < 1000 or (div > 0 and div % 10 == 0)
    else:
      zero = zero or len(comps) > 0
    base += 1
    amount = div
  if not comps:
    comps.append(metas[amount])
  return ''.join(comps)+'元整'




@pytest.mark.parametrize("amount,upper",[(0, '零元整'), (1, '壹元整'), (2, '贰元整'), (3, '叁元整'), (4, '肆元整'), (5, '伍元整'), (6, '陆元整'), (7, '柒元整'), (8, '捌元整'), (9, '玖元整') ]
                         )
def test_rmb_toupper_one_digit(amount,upper):
  assert rmb_toupper(amount) == upper


@pytest.mark.parametrize("amount,upper",
                         [(10, '壹拾元整'), (11, '壹拾壹元整'), (12, '壹拾贰元整'), (13, '壹拾叁元整')]
                         )
def test_rmb_toupper_two_digit(amount,upper):
  assert rmb_toupper(amount) == upper

@pytest.mark.parametrize("amount,upper",
                         [ (110, '壹佰壹拾元整'), (120, '壹佰贰拾元整'), (133, '壹佰叁拾叁元整')]
                         )
def test_rmb_toupper_three_digit(amount,upper):
  assert rmb_toupper(amount) == upper


@pytest.mark.parametrize("amount,upper",
                         [ (101, '壹佰零壹元整'), (304, '叁佰零肆元整'), (609, '陆佰零玖元整')]
                         )
def test_rmb_toupper_three_digit_with_zero(amount,upper):
  assert rmb_toupper(amount) == upper


@pytest.mark.parametrize("amount,upper",
                         [ (1110, '壹仟壹佰壹拾元整'), (1200, '壹仟贰佰元整'), (1234, '壹仟贰佰叁拾肆元整')]
                         )
def test_rmb_toupper_four_digit(amount,upper):
  assert rmb_toupper(amount) == upper

@pytest.mark.parametrize("amount,upper",
                         [ (1101, '壹仟壹佰零壹元整'), (3004, '叁仟零肆元整'), (6009, '陆仟零玖元整')]
                         )
def test_rmb_toupper_four_digit_with_zero(amount,upper):
  assert rmb_toupper(amount) == upper


@pytest.mark.parametrize("amount,upper",
                         [ (11120, '壹万壹仟壹佰贰拾元整'), (12000, '壹万贰仟元整'), (12345, '壹万贰仟叁佰肆拾伍元整')]
                         )
def test_rmb_toupper_five_digit(amount,upper):
  assert rmb_toupper(amount) == upper


@pytest.mark.parametrize("amount,upper",
                         [ (10020, '壹万零贰拾元整'), (10200, '壹万零贰佰元整'), (10004, '壹万零肆元整'),
                           (10304, '壹万零叁佰零肆元整'),
                           (13004, '壹万叁仟零肆元整')
                           ]
                         )
def test_rmb_toupper_five_digit_with_zero(amount,upper):
  assert rmb_toupper(amount) == upper


@pytest.mark.parametrize("amount,upper",
                         [ (111200, '壹拾壹万壹仟贰佰元整'), (120000, '壹拾贰万元整'), (123456, '壹拾贰万叁仟肆佰伍拾陆元整')]
                         )
def test_rmb_toupper_six_digit(amount,upper):
  assert rmb_toupper(amount) == upper

@pytest.mark.parametrize("amount,upper",
                         [(103004, '壹拾万零叁仟零肆元整'), (100304, '壹拾万零叁佰零肆元整'), (100020, '壹拾万零贰拾元整'), (100200, '壹拾万零贰佰元整'), (100004, '壹拾万零肆元整'),


                           (133004, '壹拾叁万叁仟零肆元整')
                           ]
                         )
def test_rmb_toupper_six_digit_with_zero(amount,upper):
  assert rmb_toupper(amount) == upper



@pytest.mark.parametrize("amount,upper",
                         [ (1112000, '壹佰壹拾壹万贰仟元整'), (1200000, '壹佰贰拾万元整'), (1234567, '壹佰贰拾叁万肆仟伍佰陆拾柒元整')]
                         )
def test_rmb_toupper_seven_digit(amount,upper):
  assert rmb_toupper(amount) == upper

@pytest.mark.parametrize("amount,upper",
                         [ (1012000, '壹佰零壹万贰仟元整'), (1200008, '壹佰贰拾万零捌元整'), (1004567, '壹佰万零肆仟伍佰陆拾柒元整')]
                         )
def test_rmb_toupper_seven_digit_with_zero(amount,upper):
  assert rmb_toupper(amount) == upper

@pytest.mark.parametrize("amount,upper",
                         [ (11120000, '壹仟壹佰壹拾贰万元整'), (12000000, '壹仟贰佰万元整'), (12345678, '壹仟贰佰叁拾肆万伍仟陆佰柒拾捌元整')]
                         )
def test_rmb_toupper_eight_digit(amount,upper):
  assert rmb_toupper(amount) == upper

@pytest.mark.parametrize("amount,upper",
                         [ (10120000, '壹仟零壹拾贰万元整'), (12050403, '壹仟贰佰零伍万零肆佰零叁元整'), (10005678, '壹仟万零伍仟陆佰柒拾捌元整')]
                         )
def test_rmb_toupper_eight_digit_with_zero(amount,upper):
  assert rmb_toupper(amount) == upper

@pytest.mark.parametrize("amount,upper",
                         [ (111200000, '壹亿壹仟壹佰贰拾万元整'), (120000000, '壹亿贰仟万元整'), (912345678, '玖亿壹仟贰佰叁拾肆万伍仟陆佰柒拾捌元整')]
                         )
def test_rmb_toupper_nine_digit(amount,upper):
  assert rmb_toupper(amount) == upper

@pytest.mark.parametrize("amount,upper",
                         [ (101200000, '壹亿零壹佰贰拾万元整'), (120050306, '壹亿贰仟零伍万零叁佰零陆元整'), (900005678, '玖亿零伍仟陆佰柒拾捌元整')]
                         )
def test_rmb_toupper_nine_digit_with_zero(amount,upper):
  assert rmb_toupper(amount) == upper


@pytest.mark.parametrize("amount,upper",
                         [
                           (   99086510000000, '玖拾玖万零捌佰陆拾伍亿壹仟万元整'),
                           (  100086510000000, '壹佰万零捌佰陆拾伍亿壹仟万元整'),
                           (  103086510000000, '壹佰零叁万零捌佰陆拾伍亿壹仟万元整'),
                           ( 1003086510000000, '壹仟零叁万零捌佰陆拾伍亿壹仟万元整'),
                         ]
                         )
def test_rmb_toupper_big(amount,upper):
  # 2019 中国 GDP 99086510000000
  assert rmb_toupper(amount) == upper