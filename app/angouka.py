# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 11:49:58 2015

@author: kentarokira
"""

import Crypto.Cipher.AES

KAGI="hellokentarokira"
Engine = Crypto.Cipher.AES.new(KAGI, Crypto.Cipher.AES.MODE_ECB)
MAX_LENGTH=30

class AngoukaError(Exception):
    def __init__(self,code,message):
        self.code = code
        self.message = message

def up(string):
    #入力文字チェック
    if len(string) == 0:
        raise AngoukaError("E-AGK-001","暗号化対象の入力文字列が0文字です。")
    elif len(string) > MAX_LENGTH:
        raise AngoukaError("E-AGK-002","暗号化対象の入力文字列が30文字以上です。")
    #暗号化前処理開始
    position = 3 #追加文字の位置
    counter = 0 #追加文字
    #文字列の長さ(複合時に使用)を先頭に追加
    strlen  = 0 
    if len(string) < 10:
        strlen = "0" + str(len(string))
    else:
        strlen = str(len(string))
    string = strlen + string
    #32文字になるまで繰り返し(+2は先頭の文字列の長さ)
    while len(string) < MAX_LENGTH+2:
        pre=string[:position]
        pos=string[position:]
        string = pre + str(counter) + pos
        if counter < 9:        
            counter += 1
        else:
            counter = 0 
        position += 2
    return string
    
def down(string):
    #文字列の長さ(複合時に使用)を先頭から取得
    strlen=int(string[0:2])
    string = string[2:]
    #MAX_LENGTHの半分より、元の文字列が短い場合は、後ろの不要な付加情報を一括削除し、
    #残りの文字列から、奇数番目を抽出する
    if strlen*2 < MAX_LENGTH:
        string = string[:strlen*2:2]
    #MAX_LENGTHの半分より、元の文字列が長い場合は、奇数番目を抽出すべき位置を決めたのち、
    #文字列を抽出し、さらに修正不要分の文字列を結合する
    else:
        string = string[:(MAX_LENGTH-strlen)*2:2]+string[(MAX_LENGTH-strlen)*2:]
        
    return string
    
def encode(planText):
    # 文字数は16の倍数でなければならない
    ciphertext = Engine.encrypt(up(planText))
    print(ciphertext)
    return ciphertext
    
def decode(angouText):
    ciphertext = Engine.decrypt(angouText).decode('utf-8')
    return down(ciphertext)
