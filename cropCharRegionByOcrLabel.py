#coding:utf-8
'''
将此脚本放在OcrLabel.txt 同一文件夹下
运行 : python  cropCharRegionByOcrLabel.py
目录结构：
tianfu/
  ---- 1.png 
  ---- 2.png
  ...
  ---- 100.png
  ---- OcrLabel.txt
  ---- cropCharRegionByOcrLabel.py
'''
import os
import random
import cv2

dstimgsz = 416 # 裁剪目标大
NNN = 3 # 每个图随机位置扩展个数
workdir = ""
cropdir = "xcrop" # 裁剪图保存文件夹
savepicsuffix = "jpg"  # 保存图片格式
scriptFolder ="./"

flagSub = False
if flagSub:
    imdir = os.path.join(cropdir,"images")
    labdir=os.path.join(cropdir,"labels")
    if(not os.path.exists(imdir)):
        os.makedirs(imdir)
    if(not os.path.exists(labdir)):
        os.makedirs(labdir)

AllClasschar = []

class LabelObj(object):
    # 所有字符类别
    clschars = []
    def __init__(self):
        self.path = None
        self.width = None
        self.height = None
        self.labels = []
        self.labelsString = "" 
        self.boxs = []
        self.valid = False

def readOcrLabelInfo():
    if not os.path.exists(cropdir):
        os.makedirs(cropdir)
    labelfile = os.path.join(scriptFolder,"OcrLabel.txt")
    with open(labelfile,'r') as f:
        xx = f.readlines()

    AllInfo = []
    # 每个图片
    for a in xx[:]:
        print('==================')
        labels = []
        one = LabelObj()
        #print(one.labels)
        bb = a.strip().split("\t")
        # 可能存在图像未标记boxes的情况
        #print(len(bb))
        if (len(bb)==2):
            one.valid = True
            thisPath = bb[0]
            # read image get width and height
            # 原始图像(可能比较大)
            img = cv2.imread(thisPath,1)
            height,width,c = img.shape
            print(thisPath,"H:", height, " w:", width)
            # 处理box信息,可能多个box
            bx = bb[1]
            info = bx.replace("false","False")
            boxs = eval(info)
            one.boxs = boxs
            print(boxs,len(boxs))
            bigBox = []
            # 根据每张图标记的字符框裁剪小区域
            # 要裁剪区域的坐标表示,左上角和宽高:big_x,big_y ,big_w,big_h  
            big_x = 0
            big_y=0
            big_w = 0
            big_h = 0
            xx = [] # 存放所有点的x
            yy = [] # 存放所有角点的y
            for lb in boxs: 
                # 四个角点按顺序写的,
                # class x_center y_center width height,range (0-1)
                pts = lb["points"]
                x_pos = [p[0] for p in pts]
                y_pos = [p[1] for p in pts]
                xx.extend(x_pos)
                yy.extend(y_pos)
                
                print(x_pos, y_pos)
                # 每个框四个角点坐标
                xmin = min(x_pos)
                xmax = max(x_pos)
                ymin = min(y_pos)
                ymax = max(y_pos)
                charwidth = xmax-xmin+1
                charheight = ymax-ymin+1
                
            print("xx", xx)
            print("yy", yy)
            exdcount = NNN # 随机位置扩展个数
            for n in range(exdcount):
                validone = LabelObj()
                Nx = 1 # 字符偏移个数
                xminlim = min(min(xx)-charwidth*Nx, max(xx)-dstimgsz)
                yminlim = min(min(yy)-charheight*Nx, max(yy)-dstimgsz)
                rndx= random.randint(xminlim, min(xx))
                rndy = random.randint(yminlim, min(yy))
                big_x = max(0,rndx)
                big_y = max(0,rndy)
                # 裁剪目标尺寸宽高的区域
                big_w = dstimgsz #min(width ,max(xx)-min(xx)+1+charwidth*(Nx*2))
                big_h = dstimgsz # min(height,max(yy)-min(yy)+1+charheight*(Nx*2-1))

                # 转换为新的crop内的坐标
                curCropAllboxLabels=[]
                one.labels = []
                for lb in boxs: 
                    lab = lb['transcription']
                    one.clschars.append(lab)
                    oldpts = lb["points"]
                    pts = []
                    # 每个点减去裁剪区域的起点
                    for ppp in oldpts:
                        newp = [ppp[0]-big_x,ppp[1]-big_y]
                        pts.append(newp)

                    lefttop = pts[0]
                    rightbotm = pts[2]
                    xmin = lefttop[0]
                    ymin = lefttop[1]
                    xmax = rightbotm[0]
                    ymax = rightbotm[1]
                    x_center = (xmin+xmax)/2.0/big_w
                    y_center = (ymin+ymax)/2.0/big_h
                    _width = (xmax-xmin)*1.0/big_w
                    _height = (ymax-ymin)*1.0/big_h
                    thisLabel = (lab,x_center,y_center,_width,_height)
                    one.labels.append(thisLabel)
                    validone.labels.append(thisLabel)
                    curCropAllboxLabels.append(thisLabel)
                    print(thisPath, thisLabel)
                cropimg = img[big_y:big_y+big_h,big_x:big_x+big_w,:]
                print(cropimg.shape)

                # dst name 
                newpicname = thisPath[:-5]+"_{}.{}".format(n,savepicsuffix)
                if flagSub:
                    dstname = os.path.join(cropdir,"images",newpicname)
                else:
                    dstname = os.path.join(cropdir,newpicname)
                cv2.imwrite(dstname, cropimg)

                # 更新名称
                validone.path = dstname
                one.path = dstname
                
                #print(one.labelsString)
                print(len(one.labels))
                AllInfo.append(validone)
                AllClasschar = one.clschars


    print("----------------------------")
    # 所有 字符class 类别
    print(AllClasschar) 
    # 去重 排序
    AllClasschar = tuple(sorted(list(set(AllClasschar))))
    print(AllClasschar) 
    AllClassDict ={AllClasschar[k]:k for k in range(len(AllClasschar))} 
    print(AllClassDict)
    print("class count: ", len(AllClasschar))
    # write classs 
    if 1:
        namesStr = ""
        for i in range(len(AllClasschar)):
            xi = "{}:{}\n".format(i, AllClasschar[i])
            namesStr+=xi
        namesStr = namesStr.strip()
        print(namesStr)
        with open("names.txt", 'w') as f:
            f.writelines(namesStr)
        print('write all class names to names.txt')

    # =========== 所有信息写入文件=======
    for x in AllInfo[:]:
        # kkkk.bmp  ---> kkkk.txt
        txtname = x.path[:-4] +".txt"
        if flagSub:
            txtname = txtname.replace("images","labels")
        labelsString = ""
        for bx in x.labels:
            #print(bx)
            lab,x_center,y_center,_width,_height = bx
            # lab -> class num
            indxClss = AllClassDict[lab] 
            infoStr = "{} {:.6f} {:.6f} {:.6f} {:.6f}".format(indxClss,x_center,y_center,_width,_height)
            #print(infoStr)
            labelsString += infoStr+"\n"
        labelsString = labelsString.strip()
        print(txtname)
        print(labelsString)
        with open(txtname, 'w') as f:
            f.writelines(labelsString)


readOcrLabelInfo()

