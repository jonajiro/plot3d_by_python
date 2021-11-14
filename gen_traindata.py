import numpy as np
import cv2
import platform
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
#データ点数
data_num = 4;

#データサイズ
data_x = 330;
data_y = 165;

#データ点格納用
points = np.zeros([data_num,2],dtype = int) #格納配列
pt = np.array([0,0]) #要素地点管理

# 画像のパス

savepath = "train_data/"
str_extension = ".bmp"

settingval = 0

alpha = 1.1 # コントラスト項目
beta = 10    # 明るさ項目

resolution = 0.09#解像度劣化具合
filtcoef = 60#ぼかし具合

resolution_table = np.array(0.05)
# resolution_table = np.append(resolution_table,0.06)
# resolution_table = np.append(resolution_table,0.07)
resolution_table = np.append(resolution_table,0.075)
# resolution_table = np.append(resolution_table,0.09)
resolution_table = np.append(resolution_table,0.1)
# resolution_table = np.append(resolution_table,0.3)
# resolution_table = np.append(resolution_table,0.5)
# resolution_table = np.append(resolution_table,0.7)
# resolution_table = np.append(resolution_table,0.9)
resolution_table = np.append(resolution_table,1)

filtcoef_table = np.array(10)
# filtcoef_table = np.append(filtcoef_table,20)
# filtcoef_table = np.append(filtcoef_table,40)
# filtcoef_table = np.append(filtcoef_table,60)
filtcoef_table = np.append(filtcoef_table,30)
filtcoef_table = np.append(filtcoef_table,60)

img_base = cv2.imread("base.bmp")

# text = np.array(["り"]) #ひらがな
# text = np.append(text, "に")
# text = np.append(text, "ま")

text = np.array(["あ"]) #ひらがな#0
text = np.append(text, "い")#0
text = np.append(text, "う")#0
text = np.append(text, "え")#0
text = np.append(text, "お")

text = np.append(text, "か")
text = np.append(text, "き")
text = np.append(text, "く")
text = np.append(text, "け")
text = np.append(text, "こ")

text = np.append(text, "さ")#0
text = np.append(text, "し")
text = np.append(text, "す")#0
text = np.append(text, "せ")#0
text = np.append(text, "そ")#0

text = np.append(text, "た")
text = np.append(text, "ち")
text = np.append(text, "つ")
text = np.append(text, "て")
text = np.append(text, "と")

text = np.append(text, "な")
text = np.append(text, "に")
text = np.append(text, "ぬ")
text = np.append(text, "ね")
text = np.append(text, "の")

text = np.append(text, "は")
text = np.append(text, "ひ")
text = np.append(text, "ふ")
text = np.append(text, "へ")
text = np.append(text, "ほ")

text = np.append(text, "ま")
text = np.append(text, "み")
text = np.append(text, "む")
text = np.append(text, "め")
text = np.append(text, "も")

text = np.append(text, "や")
text = np.append(text, "ゆ")
text = np.append(text, "よ")

text = np.append(text, "ら")
text = np.append(text, "り")
text = np.append(text, "る")
text = np.append(text, "れ")
text = np.append(text, "ろ")

text = np.append(text, "わ")
text = np.append(text, "を")
text = np.append(text, "ん")

text_x, text_y = 28, 28  # テキスト表示する左上の座標
font_size = 200
text_color = (0, 0, 0)  # 赤文字, 元がOpenCV画像のためBGR表記

# OSごとにパスが異なる
font_path_dict = {
  # この例だとメイリオを使用. ほかのフォントにも当然変更できる
  # "Windows": "C:/workspace/027_HIRAGANA/program/v001/FZcarnumberJA-OTF_ver10.ttf"
  "Windows": "C:/Windows/Fonts/BIZ-UDMinchoM.ttc"
  # "Windows": "C:/Windows/Fonts/HGRPRE.TTC"
  # "Windows": "C:/Windows/Fonts/meiryo.ttc"
  # "Windows": "C:/Windows/Fonts/TrmFontJB.ttf"
}

for z in range(len(text)):
    print(z)
    pil_image = Image.fromarray(img_base)
    draw = ImageDraw.Draw(pil_image)
    font_path = font_path_dict.get(platform.system())
    if font_path is None:
      assert False, "想定してないOS"

    draw.font = ImageFont.truetype(font_path, font_size)  # font設定
    draw.text((text_x, text_y), text[z], text_color)  # pil_imageに直接書き込み
    result_image = np.array(pil_image)  # OpenCV/numpy形式に変換
    i = cv2.cvtColor(result_image, cv2.COLOR_RGB2GRAY)
    height = i.shape[0]
    width = i.shape[1]
    for j in range(len(resolution_table)):
        for k in range(len(filtcoef_table)):
            img1 = cv2.resize(i , (int(width*resolution_table[j]), int(height*resolution_table[j])))
            img2 = cv2.resize(img1 , (int(width), int(height)))
            gray_base = cv2.blur(img2,(filtcoef_table[k],filtcoef_table[k]))

            # gray_base = cv2.equalizeHist(gray_base)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(3, 3))
            gray_base = clahe.apply(gray_base)

            cv2.imwrite(savepath + str(z) + '-' + str(j) + '-' + str(k) + str_extension , gray_base)
