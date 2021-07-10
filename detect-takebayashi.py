import cv2
import numpy as np

#各画像をディレクトリ配下に設置
dir='./tochigi/'

#1)NDVIをつかっって緑地（木々が生えている場所）を探す
tgt = cv2.imread(dir+'2021-04-07_NDVI.jpg',0)
tgt = tgt[0:800, 0:1200]#トリミング

#2)竹藪が枯れたタイミングを狙った画像を取得　5/15近辺でなおかつ1年前も確認してわかりやすいほうを使用
img1 = cv2.imread(dir+'2021-05-02.jpg',1)
img1 = img1[0:800, 0:1200]
img_bgr1 = cv2.split(img1)  # 色分解
img_r1 = img_bgr1[2]
img_r1[100<img_r1] ==0 
img_r1[20>img_r1] ==0 

#3)竹の葉が緑に戻ったタイミングを狙った画像を取得
img2 = cv2.imread(dir+'2021-06-11.jpg',1)
img2 = img2[0:800, 0:1200]
img_bgr2 = cv2.split(img2)# 色分解
img_r2 = img_bgr2[2]
img_r2[100<img_r2] ==0
img_r2[20>img_r2] ==0

#出力のベースにしたい画像 2の画像でも3の画像でもOK
img3 = cv2.imread(dir+'2021-06-11.jpg',1)
img3 = img3[0:800, 0:1200]

#ブロック数の合計で回す
for x in range(0,2400):＃20ブロック*60ブロック
    #横のブロック数であまりを求める
    a,b = divmod(x, 60)
    x=(b*20)#20pxのブロックで判定
    y=(a*20)#20px
    xe=x+20
    ye=y+20
    ba=img_r1[y:ye, x:xe]
    am=np.mean(ba)
    bb=img_r2[y:ye, x:xe]
    tg1=tgt[y:ye, x:xe]
    tgm=np.mean(tg1)
    if(tgm<50):
        print(tgm)
        bm=np.mean(bb)
        sa=abs(round(bm)-round(am))
        print(sa)
        if(sa>5):
            img3[y:ye, x:xe]=[0,0,255]#赤くぬりつぶす

cv2.imwrite("output.png", img3)
