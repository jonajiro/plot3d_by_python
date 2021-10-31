import numpy as np
import cv2
import platform
from PIL import Image, ImageDraw, ImageFont

import numpy as np
import cv2
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
path = "cap3.PNG"
savepath = "temp_out.bmp"
savepath2 = "temp_out2.bmp"
savepath3 = "temp_out3.bmp"

settingval = 0

#マウスイベント処理(leftimg)
def mouse_event_l(event, x, y, flags, param):
    #配列外参照回避
    if pt[0] > (data_num-1):
        cv2.polylines(window_l,[points],True,(0,255,255))


        i = cv2.imread(path, 1)                                        # 画像読み込み
        # 変換前後の対応点を設定
        p_original = np.float32([points])
        p_trans = np.float32([[0,0], [data_x,0], [data_x,data_y], [0,data_y]])

        # 変換マトリクスと射影変換
        M = cv2.getPerspectiveTransform(p_original, p_trans)
        i_trans = cv2.warpPerspective(i, M, (data_x, data_y))

        cv2.imwrite(savepath, i_trans)


        i = cv2.imread(savepath, 1)                                        # 画像読み込み
        # 変換前後の対応点を設定
        p_original = np.float32([[14,77], [64,77], [64,127], [14,127]])
        p_trans = np.float32([[0,0], [256,0], [256,256], [0,256]])

        # 変換マトリクスと射影変換
        M = cv2.getPerspectiveTransform(p_original, p_trans)
        i_trans = cv2.warpPerspective(i, M, (256, 256))

        cv2.imwrite(savepath2, i_trans)

        gray = cv2.cvtColor(i_trans, cv2.COLOR_RGB2GRAY)

        cv2.imwrite("gray" + savepath2 , gray)

        return
    #クリック地点を配列に格納
    if event == cv2.EVENT_LBUTTONUP:
        points[pt[0]] = [x,y] #格納
        cv2.circle(window_l, (x,y), 1, (255,0,0), -1)

        pt[0] += 1 #要素地点を1つ増やす

if settingval == 0:
    #画像の読み込み
    window_l = cv2.imread(path, 1) #leftimg

    #ウィンドウ生成
    cv2.namedWindow("window_l", cv2.WINDOW_KEEPRATIO) #leftimg

    #マウスイベント時に関数mouse_eventの処理を行う
    cv2.setMouseCallback("window_l", mouse_event_l) #leftimg

    #「q」が押されるまでループ
    while True:
        #画像の表示
        cv2.imshow("window_l", window_l) #leftimg

        #キー入力
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()

img_target = cv2.imread("gray" + savepath2,1) # 画像読み込み
gray_target = cv2.cvtColor(img_target, cv2.COLOR_RGB2GRAY)
img_base = cv2.imread("base.bmp")

text = np.array(["あ"]) #ひらがな
text = np.append(text, "い")
text = np.append(text, "う")
text = np.append(text, "え")
text = np.append(text, "お")

text = np.append(text, "か")
text = np.append(text, "き")
text = np.append(text, "く")
text = np.append(text, "け")
text = np.append(text, "こ")

text = np.append(text, "さ")
text = np.append(text, "し")
text = np.append(text, "す")
text = np.append(text, "せ")
text = np.append(text, "そ")

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
  "Windows": "C:/Windows/Fonts/BIZ-UDMinchoM.TTC"
  #C:/Windows/Fonts/meiryo.ttc
}

cycle = len(text)
dism = np.zeros(cycle) #非類似度
# for z in range(cycle):
#     dism[z] = 0
for z in range(cycle):
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
    ratio = 0.07

    img1 = cv2.resize(i , (int(width*ratio), int(height*ratio)))
    img2 = cv2.resize(img1 , (int(width), int(height)))
    # img3 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    gray_base = cv2.blur(img2,(40,40))

    width, height = gray_base.shape

    for y in range(height):
        for x in range(width):
            dism[z] = dism[z] + (gray_target[x,y] - gray_base[x,y])*(gray_target[x,y] - gray_base[x,y])
    dism[z] = dism[z] / (width * height)
    print(dism[z])
resultdata = np.stack([text, dism], 1)
resultdata_sort_col_num = resultdata[np.argsort(resultdata[:, 1])]

pil_image = Image.fromarray(img_base)
draw = ImageDraw.Draw(pil_image)
font_path = font_path_dict.get(platform.system())
if font_path is None:
  assert False, "想定してないOS"

draw.font = ImageFont.truetype(font_path, font_size)  # font設定
draw.text((text_x, text_y), resultdata_sort_col_num[0,0], text_color)  # pil_imageに直接書き込み
result_image = np.array(pil_image)  # OpenCV/numpy形式に変換
i = cv2.cvtColor(result_image, cv2.COLOR_RGB2GRAY)
height = i.shape[0]
width = i.shape[1]
ratio = 0.07

img1 = cv2.resize(i , (int(width*ratio), int(height*ratio)))
img2 = cv2.resize(img1 , (int(width), int(height)))
# img3 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
gray_base = cv2.blur(img2,(40,40))

cv2.imwrite("gray" + savepath3 , gray_base)
# dism_str = [str(n) for n in dism]
# savedata = np.stack([text, dism_str], 1)
# print(type(savedata))
# print(savedata)
np.savetxt('result.csv', resultdata_sort_col_num, delimiter = ",", fmt = "%s")
