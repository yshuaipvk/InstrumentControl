#origin、python编程的Demo


import OriginExt as O
import tempfile
app = O.ApplicationSI();app.Visible = app.MAINWND_SHOW  #创建项目
#开始
pageName=app.CreatePage(app.OPT_WORKSHEET)     #创建worksheet 可在后面加名字 默认为book
app.PutPageString(pageName, "testPageStr", "testPageValue")
testData=[[5,87,90],[3.14,24.6,68.09]]
app.PutWorksheet(pageName,testData)            #将数据放入worksheet
#app.SetWorksheet()
#outputData=app.GetWorksheet(pageName)          #读取worksheet数据
#temDir=tempfile.mkdtemp()
#temFile=temDir+'\\OriginExTest.opju'
#app.Save(temFile)
#app.NewProject()
#app.Load(temFile)
#if app.BeginSession():
#    app.EndSession()
#退出
#tempDir = tempfile.mkdtemp()
##tempFile = tempDir + "\\ys.opju"
#app.Save(tempFile)
#app.NewProject()
#app.Load(tempFile)
#app.Exit()
#app.CreatePage(app.OPT_GRAPH,'name')   #创建图形
#for pg in app.GraphPages:              #查看所有图形名称
    #print(pg.Name)
#app.CreatePage(app.OPT_LAYOUT)
#for pg in app.LayoutPages:
#    print(pg.Name)
