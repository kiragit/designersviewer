# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 12:08:31 2015

@author: kentarokira
"""

import pytest
from app.angouka import * 

def test_up_from_0_length():
    with pytest.raises(AngoukaError) as excinfo:
        value = up("")
        #aassert excinfo.message == "E-AGK-001"

def test_up_from_1_length():
    value = up("a")
    assert value == "01a01234567890123456789012345678"

def test_up_from_10_length():
    value = up("abcdefghij")
    assert value == "10a0b1c2d3e4f5g6h7i8j90123456789"

def test_up_from_29_length():
    value = up("abcdefghijabcdefghijabcdefghi")
    assert value == "29a0bcdefghijabcdefghijabcdefghi"

def test_up_from_30_length():
    value = up("abcdefghijabcdefghijabcdefghij")
    assert value == "30abcdefghijabcdefghijabcdefghij"

def test_up_from_31_length():
    with pytest.raises(AngoukaError) as excinfo:
        value = up("1234567890123456789012345678901")
        #assert excinfo.message == "E-AGK-002"

def test_up_over_32_length():
    with pytest.raises(AngoukaError) as excinfo:
        value = up("123456789012345678901234567890123")
        #assert excinfo.message == "E-AGK-002"

def test_down_from_30_length():
    value = down("30abcdefghijabcdefghijabcdefghij")
    assert value == "abcdefghijabcdefghijabcdefghij"

def test_down_from_1_length():
    value = down("01a01234567890123456789012345678")
    assert value == "a"

def test_down_from_10_length():
    value = down("10a0b1c2d3e4f5g6h7i8j90123456789")
    assert value == "abcdefghij"

def test_down_from_14_length():
    value = down("14a0b1c2d3e4f5g6h7i8j9a0b1c2d345")
    assert value == "abcdefghijabcd"

def test_down_from_15_length():
    value = down("15a0b1c2d3e4f5g6h7i8j9a0b1c2d3e4")
    assert value == "abcdefghijabcde"

def test_down_from_16_length():
    value = down("16a0b1c2d3e4f5g6h7i8j9a0b1c2d3ef")
    assert value == "abcdefghijabcdef"

def test_encode_14_length():
    value = encode("abcdefghijabcd")
    assert value == b'2\xbfJ\xb5}\xbe(\xaf,T\xed\x1a^.j?\xfd\xd9\xc8\xaa[\x89\xa1\x8d\xd4\xe0\xa0CT\x03P\xfd'

def test_decode_14_length():
    value = decode(b'2\xbfJ\xb5}\xbe(\xaf,T\xed\x1a^.j?\xfd\xd9\xc8\xaa[\x89\xa1\x8d\xd4\xe0\xa0CT\x03P\xfd')
    assert value == "abcdefghijabcd"

def test_encode_15_length():
    value = encode("abcdefghijabcde")
    assert value == b'~\x06,\xb0JS\x90)\xe9N\xfc%\xadL\x9c\xd6G\xfe\x97\x00\x8f\xa3Q\x92\xd5J2\xf8\t&Q\x8b'

def test_decode_15_length():
    value = decode(b'~\x06,\xb0JS\x90)\xe9N\xfc%\xadL\x9c\xd6G\xfe\x97\x00\x8f\xa3Q\x92\xd5J2\xf8\t&Q\x8b')
    assert value == "abcdefghijabcde"

def test_encode_16_length():
    value = encode("abcdefghijabcdef")
    assert value == b"\x9f\xb5Ta\xf0S3\x0c\xc7\xf0\xadE\x07qW\x1c>*<\xbe\xdfr\xd4\x8b\x07\xcd\xcc'\x0b\x8f\x08\xe2"

def test_decode_16_length():
    value = decode(b"\x9f\xb5Ta\xf0S3\x0c\xc7\xf0\xadE\x07qW\x1c>*<\xbe\xdfr\xd4\x8b\x07\xcd\xcc'\x0b\x8f\x08\xe2")
    assert value == "abcdefghijabcdef"

def test_decode_15_length():
    value = decode(b'~\x06,\xb0JS\x90)\xe9N\xfc%\xadL\x9c\xd6G\xfe\x97\x00\x8f\xa3Q\x92\xd5J2\xf8\t&Q\x8b')
    assert value == "abcdefghijabcde"

def test_encode_29_length():
    value = encode("abcdefghijabcdefghijabcdefghi")
    assert value == b'\x0b\x1a\x88\xc3b\x97\xf0\xf5\x8foQ\xf15Mx\x8a\x1b\xff\x0e\xb25\xd1\xae\xdb\xc9\xda&\x84\x90\x92\xfe\xe2'

def test_decode_29_length():
    value = decode(b'\x0b\x1a\x88\xc3b\x97\xf0\xf5\x8foQ\xf15Mx\x8a\x1b\xff\x0e\xb25\xd1\xae\xdb\xc9\xda&\x84\x90\x92\xfe\xe2')
    assert value == "abcdefghijabcdefghijabcdefghi"
    
def test_encode_30_length():
    value = encode("abcdefghijabcdefghijabcdefghij")
    assert value == b'\xf5X\x00\x1a\x03j\x0buY\xae\xab\xde\xed\xe6\xe1"\xf8\x9cE\xa3\r\xd2\xdd6\x17\xf0\t\x99\x05\xaa\x81u'
    
def test_decode_30_length():
    value = decode(b'\xf5X\x00\x1a\x03j\x0buY\xae\xab\xde\xed\xe6\xe1"\xf8\x9cE\xa3\r\xd2\xdd6\x17\xf0\t\x99\x05\xaa\x81u')
    assert value == "abcdefghijabcdefghijabcdefghij"