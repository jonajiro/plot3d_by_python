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
path = "test_rowdata/cap4.PNG"
savepath = "test_rowdata/temp_out_seitai.bmp"
savepath2 = "0-3.bmp"

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

def printing1(position):
    buf = 1

def printing2(position):
    buf = 1

def printing3(position):
    buf = 1

def printing4(position):
    buf = 1

def printing5(position):
    buf = 1
# 画像を読み込み
# cv2.imread() を利用しグレースケールで読み込む
img = cv2.imread(savepath, 1)
# img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

img_t = cv2.imread("train_data/0-3-0.bmp")

# img_t = img_t[:,:,:,np.newaxis]
alp = np.full(img_t.shape[0]*img_t.shape[1], 255).reshape(img_t.shape[0], img_t.shape[1], 1)
# print(alp.shape)
img_t = np.append(img_t,alp,axis=2)
# gray_t = cv2.cvtColor(img_t, cv2.COLOR_RGB2GRAY)
# トラックバーを表示するウィンドウを作成
# cv2.namedWindow("window", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("window", cv2.WINDOW_NORMAL)
# 初期値を設定
threshold1 = 0
threshold2 = 800
threshold3 = 255
threshold4 = 0
threshold5 = 0

# トラックバーを作成する
# トラックバーの名前、トラックバーをつけるウィンドウ名、初期値、トラックバーの最大値。コールバック関数

cv2.createTrackbar("track1", "window", threshold1, 360, printing1)
cv2.createTrackbar("track2", "window", threshold2, 1000, printing2)
cv2.createTrackbar("track3", "window", threshold3, 255, printing3)
cv2.createTrackbar("track4", "window", threshold4, 1000, printing4)
cv2.createTrackbar("track5", "window", threshold5, 1000, printing5)
print(int(img.shape[1]*(threshold2/100 + 1)-img_t.shape[1])*100)
while True:

    #高さを定義
    height = img.shape[0]
    #幅を定義
    width = img.shape[1]
    #回転の中心を指定
    center = (int(width/2), int(height/2))
    #回転角を指定
    angle = threshold1
    #スケールを指定
    scale = 1.0
    #getRotationMatrix2D関数を使用
    trans = cv2.getRotationMatrix2D(center, angle , scale)
    #アフィン変換
    img2 = cv2.warpAffine(img, trans, (width,height))

    # img2 = img
    resize_x = int(img2.shape[1]*threshold2/100 + 1)
    resize_y = int(img2.shape[0]*threshold2/100 + 1)
    # print(threshold2/100)
    if resize_x < resize_y:
        if resize_x < img_t.shape[1]:
            resize_x = img_t.shape[1]
            resize_y = int(img2.shape[0]*resize_x/img2.shape[1])
    else:
        if resize_y < img_t.shape[0]:
            resize_y = img_t.shape[0]
            resize_x = int(img2.shape[1]*resize_y/img2.shape[0])
    dst = cv2.resize(
    img2, (resize_x,resize_y), interpolation=cv2.INTER_CUBIC)

    img_t[:,:,3:] = threshold3

    # 貼り付け先座標の設定。とりあえず左上に
    # print(dst.shape)
    # print(img_t.shape)
    ypos = int(threshold4/1000 * (dst.shape[0] - img_t.shape[0]))
    xpos = int(threshold5/1000 * (dst.shape[1] - img_t.shape[1]))

    x1, y1, x2, y2 = xpos+0, ypos+0, xpos+img_t.shape[0], ypos+img_t.shape[1]
    dst[y1:y2, x1:x2] = dst[y1:y2, x1:x2] * (1 - img_t[:, :, 3:] / 255) + img_t[:, :, :3] * (img_t[:, :, 3:] / 255)


    # トラックバーの位置をthreshholdに代入
    threshold1 = cv2.getTrackbarPos("track1", "window")
    threshold2 = cv2.getTrackbarPos("track2", "window")
    threshold3 = cv2.getTrackbarPos("track3", "window")
    threshold4 = cv2.getTrackbarPos("track4", "window")
    threshold5 = cv2.getTrackbarPos("track5", "window")

    # 画像を表示する
    # 引数はWindow名に合わせる
    cv2.imshow('window', dst)

    #キー入力
    if cv2.waitKey(1) & 0xFF == ord("q"):
        # ひらがな部分切り取り（しっかり）
        p_original = np.float32([[x1,y1], [xpos+img_t.shape[0],y1], [xpos+img_t.shape[0],ypos+img_t.shape[1]], [x1,ypos+img_t.shape[1]]])
        p_trans = np.float32([[0,0], [256,0], [256,256], [0,256]])

        # 変換マトリクスと射影変換
        M = cv2.getPerspectiveTransform(p_original, p_trans)

        dst = cv2.resize(
        img2, (int(img2.shape[1]*threshold2/100 + 1), int(img2.shape[0]*threshold2/100 + 1)), interpolation=cv2.INTER_CUBIC)

        outdata = cv2.warpPerspective(dst, M, (256, 256))

        gray = cv2.cvtColor(outdata, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(3, 3))
        gray_base = clahe.apply(gray)
        cv2.imwrite("test_data/" + savepath2 , gray_base)
        break

cv2.destroyAllWindows()
