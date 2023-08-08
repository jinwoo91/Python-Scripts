#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 아무 파이썬 개발환경이나 받아서 실행하면 됨
# v1.1(2022-10-18) 가상의 차량속도와 통신 주기를 알기 쉬운 형태로 변경
# v1.2(2022-10-19) 차량 1대 추가
# v1.3(2022-10-20) 차량 7대 추가, 총 10대(2호~11호)
# v1.4(2022-10-20) GPS경로셋 순서 변경.

import math

def buildWaypoint(vertexList, velocity, period):
    """입력된 각 꼭지점과 속도를 바탕으로 웨이포인트를 생성한다."""
    """vertexList[]:각 지점의 GPS좌표값 튜플(Lat, Lon)의 리스트"""
    """velocity: 속도(km/h)"""
    """period: 측정주기(s) -> 몇 초마다 점을 찍는가?"""
    
    velocity_mps = velocity/3.6
    
    # "각 구간을 몇 등분할 것인가?" 정보를 담은 리스트
    section_float = []
    for a in range(0, len(vertexList), 1):
        b = 0 if a>=len(vertexList)-1 else a+1
        m = math.pow(vertexList[b][0]-vertexList[a][0], 2)
        n = math.pow(vertexList[b][1]-vertexList[a][1], 2)
        section_float.append( math.sqrt(m+n) * 1e5 / velocity_mps / period )
        section_int = [math.floor(x)+1 for x in section_float]
        
#     print(section_int)
#     print(len(vertexList))
#     print(range(0, len(vertexList)))
#     print(list(range(0, 5)))
    
    # 출력할 웨이포인트 리스트
    waypoint = []
    # 각 직선구간에 대하여,
    for i in range(0,len(vertexList)):
        j = 0 if i>=len(vertexList)-1 else i+1
        # 분할된 새로운 GPS좌표를 계산해서 웨이포인트에 추가한다.
        for q in range(0,section_int[i]):
            myLat = vertexList[i][0] + (vertexList[j][0]-vertexList[i][0])/section_int[i]*q
            myLon = vertexList[i][1] + (vertexList[j][1]-vertexList[i][1])/section_int[i]*q
            waypoint.append((myLat,myLon))
#     print(waypoint)
#     print(len(waypoint))
    
    return waypoint


# In[ ]:


import json
import time
import requests
from datetime import datetime

def HttpPost_cold(gpsLat, gpsLon, url:str, coldSerNum:str, timeStamp:str=datetime.now().strftime('%y%m%d%H%M%S')):
    """gpsLat: Latitude"""
    """gpsLon: longitude"""
    """coldSerNum: ex) \"PLZ2022C2\" """
    """timeStamp: ex) \"221017210459\", default: current system time"""
    
    myJson = {
        "data": 
        [
            {"ser_num":coldSerNum,"lat_c":round(gpsLat,6),"lon_c":round(gpsLon,6),
             "dof_vib":3.2,"dof_tilt":1,"err_code":0,"temp_in":8,"temp_out":24,"temp_goal":5,
             "cold_min_left":251,"bat_level":82,"bat_volt":14.23,
             "time_stamp":timeStamp,"wifi_ssid":"plzhwtest","sd_mb_now":84},
        ]
    }
#     print(myJson)
    
    myHeader = {"DeviceID": coldSerNum, "Content-Type": "application/json;charset=UTF-8"}
    x = requests.post(url, json = myJson, headers= myHeader)
    
#     print(x.text)
#     print(x.status_code)
    
    

def HttpPost_vehicle(gpsLat, gpsLon, url:str, vehiclePhoneNum:str, vehicleID:str, timeStamp:str=datetime.now().strftime('%y%m%d%H%M%S')):
    """gpsLat: Latitude"""
    """gpsLon: longitude"""
    """vehiclePhoneNum: ex) \"01001001002\" """
    """vehicleID: ex) \"PLZ2022V2\"" """
    """timeStamp: ex) \"221017210459\", default: current system time"""
    
    myJson = {
        "data": 
        [
            {"01":1,"11":vehiclePhoneNum,"12":vehicleID,"13":"d47c44400348","16":"abcde12345","17":"354481106012345",
             "18":"AMM574A","19":"AMM574A-10-00-LG","1A":"0612345","21":timeStamp,"32":100,"33":1,"31":55,"34":55,"35":12,
             "36":1,"37":"00","38":1,"41":round(gpsLat,6),"42":round(gpsLon,6),"43":0.798,"44":231.8,"45":"06","46":13.91,"51":1,"52":1,"5E":1,
             "5F":1,"61":-75,"62":-16,"63":13,"64":-50,"65":"0034190E","66":"450","67":"08","68":"0002"},
        ]       
    }
#     print(myJson)
    
    myHeader = {"DeviceID": vehicleID, "Content-Type": "application/json;charset=UTF-8"}
    x = requests.post(url, json = myJson, headers= myHeader)
    
#     print(x.text)
#     print(x.status_code)
    

    


# In[ ]:


# GPS좌표 알아내는 주소 tablog.neocities.org/keywordposition.html

gps = []
# 처음 3개: 황금동
gps.append([(36.116854,128.124157),(36.116672,128.125938),(36.115368,128.125482),(36.115368,128.125279),(36.115018,128.125049),(36.115875,128.124098)])
gps.append([(36.117443425663296, 128.12418318369785),(36.11690767033565, 128.12413667264497),(36.11692608297747, 128.1236149201702),(36.11679777532781, 128.12336319160906),
           (36.11603501399149, 128.1239798476338),(36.11531719745706, 128.12460823927523),(36.11482784942129, 128.12441800545983),(36.11432089701373, 128.12418309780142),
           (36.11445095028408, 128.12376846342192),(36.11458566355966, 128.12333723448108),(36.11503944043846, 128.1234769752631),(36.114913997527076, 128.12388057248953),
           (36.11591641959613, 128.12413364917433),(36.11624441521254, 128.12327200943326),(36.11692349924917, 128.12244867968133),(36.116853308303156, 128.12176461899594),
           (36.117146855899925, 128.12217419053985),(36.11752946882608, 128.12365683799385)])
gps.append([(36.11774202642444, 128.12693082363836),(36.11762471143179, 128.12838413724793),(36.11820405182148, 128.12858679767575),(36.1180637152269, 128.1291345785003),
           (36.11886606291565, 128.12957923937526),(36.11909523838072, 128.12821080777186),(36.118276755591644, 128.12804360080935),(36.11834902764326, 128.12706722773447),
           (36.11942735058909, 128.12739363803067),(36.11963559302317, 128.1277687025699),(36.11992213905228, 128.12748401586347),(36.11973202106264, 128.12709810266426),
           (36.11944246423286, 128.1238673646178),(36.11916954642626, 128.12414115016918),(36.11877553687952, 128.1238745194953),(36.118209771979664, 128.12510487315578),
           (36.11885617472147, 128.12536400307334),(36.118531990341616, 128.12629791161726),(36.117777986681524, 128.12598170460288),(36.11743247305798, 128.126787565241)])
# 나머지 7개: 율곡동
gps.append([(36.124039661000104, 128.18770755695155),(36.12417240395391, 128.19067529762043),(36.121324186730284, 128.19073224878875),(36.12118265315686, 128.187742268562),
               (36.12032179229347, 128.1877681754574),(36.12035333712074, 128.18731325925123),(36.12077731261892, 128.18726966144365),(36.12121289089066, 128.1865098216519),(36.1212011691264, 128.18769256497188),(36.12336389527366, 128.18769737643308)])
gps.append([(36.125933906875304, 128.1783999064053),(36.127192119712745, 128.17782998681116),(36.128067502164875, 128.18044794097938),(36.12766618005193, 128.18093624355473),
           (36.12763509684831, 128.18134677912255),(36.1283255839628, 128.18123493678615),( 36.12856706490646, 128.18187728122516),(36.129250459792125, 128.18157093966806),
           (36.1296507023783, 128.18164914429607),(36.13025143823797, 128.182413529081),(36.13036204488466, 128.1830761455547),(36.13038435099079, 128.1830986974263),
           (36.127509652980265, 128.1830999825138),(36.12708700665212, 128.18118305227918),(36.1265651652496, 128.179956130881),(36.126987679091236, 128.17983193571482),
           (36.127214166224825, 128.1803962838101),(36.12772117420312, 128.18015671959708),(36.12712235278531, 128.17896752182145),(36.126431058133974, 128.17939039384686),
           (36.12604428227283, 128.17840155634056)])
gps.append([(36.11656464240948, 128.17536661791263),(36.11605785063272, 128.17512582755035),(36.11626956564388, 128.17421269222908),( 36.11650263503464, 128.17433833502844),
            (36.116368120754544, 128.17473061483827),(36.11775726527074, 128.1750511914606),(36.117894400778326, 128.17576962201366),(36.11889937139629, 128.17575128632294),
            (36.1196499474665, 128.1754848027165),(36.120019306813774, 128.17687313989282),(36.119148399075485, 128.1770045315906),(36.11748095674164, 128.1770351764059),
            (36.117464158521216, 128.1764518232095),(36.116397370115344, 128.17634150243197)])
gps.append([(36.1200420193382, 128.17501859690972),(36.119628847416465, 128.17304094340994),(36.11993454380438, 128.17311213365804),(36.12026791402589, 128.17357803875356),
           (36.12026791402589, 128.17357803875356),(36.121062340166674, 128.17343436213784),(36.122170393734834, 128.17301211184937),(36.1218780624723, 128.1720358702855),
           (36.12370612027161, 128.17124663774436),(36.12433534840142, 128.17324981581876),(36.12331321813483, 128.17364003000245),(36.12324000390747, 128.17329460662282),
           (36.12233207946275, 128.17352545798158),(36.12246667775122, 128.17404395654899),(36.121643423904416, 128.17437047039255),(36.122013667575764, 128.1756699922382),
           (36.1208833313871, 128.1765250525221),( 36.12070543683634, 128.17582819984244),(36.12026208101987, 128.17601040906254)])
gps.append([(36.113382731786096, 128.18641977645228),(36.112914534018884, 128.18546871815053),(36.11422028037788, 128.18100142088508),(36.11506406797626, 128.1813361415245),
           (36.11550090254944, 128.17998770050036),( 36.11666873343335, 128.18036058609277),(36.11586448985792, 128.18332508544455),( 36.11669332178731, 128.1833486291642),
           (36.11749909227922, 128.18479348635378),(36.11885005833374, 128.1830477879639),(36.11939178256936, 128.18385561812798),(36.11941659601243, 128.18772121885075),
           ( 36.1175226884546, 128.18787039954188),(36.117335590018136, 128.18492430999606),( 36.11371819972321, 128.1862138056926)])
gps.append([(36.1194271907518, 128.1930027442659),(36.11977778816161, 128.1926359637017),(36.12001387766969, 128.19245626833205),(36.12031419894228, 128.19216091866187),
           (36.12058303984913, 128.19276476873767),(36.12097879813031, 128.19238755766162),(36.12099750828363, 128.1918658025715),(36.12129484488012, 128.19187029728755),
           (36.12130128086964, 128.1934864972108),(36.12201347347787, 128.19345840234175),(36.122019017604956, 128.1956133089508),(36.1216561848941, 128.1963020118226),
           (36.120656395195894, 128.19489844974942),(36.11953804840132, 128.1931821333195)])
gps.append([(36.12293142864784, 128.1940332248569),(36.12291257216734, 128.19343869014483),(36.12415427928215, 128.19340194888633),(36.124172183146605, 128.19069750956896),(36.12516609861124, 128.19088469207801),
           (36.12580474977753, 128.19145528741413),(36.125499110563524, 128.19251146552645),(36.12510020249639, 128.19229993748158),(36.12499846251661, 128.19301484898673),
           (36.124498120379684, 128.19303504647243),(36.12444480258442, 128.1934119006185),(36.12543152894973, 128.1934157302449),(36.1254411001454, 128.19471548965464),
           (36.1241797296262, 128.19469082022334),(36.12418080020172, 128.19503517321644),(36.12305816307164, 128.19420175646897)])


print(len(gps))

for i in range(0,len(gps)):
#     print(gps[i])
    print(len(gps[i]))


# In[ ]:


# # 좌표값 확인용 그래프 출력
# import matplotlib.pyplot as plt
# # %matplotlib inline
# # 그래프를 새 창에서 띄우는 경우
# %matplotlib qt5

# waypoint_plot = []
# for i in range(len(gps)):
#     waypoint_plot.append(buildWaypoint(gps[i], velocity=25, period=3))

# # print(ykd_waypoint)
# # print(hgd_waypoint)

# lat_plot = []
# lon_plot = []

# for i in range(len(gps)):
#     lat_plot.append([k[0] for k in waypoint_plot[i]])
#     lon_plot.append([k[1] for k in waypoint_plot[i]])

# # print(ykdLat)
# fig = plt.figure(figsize=(20,8))
# ax = [plt.subplot(2,5,x) for x in range(1,10+1)]

# plt.autoscale(enable=True)

# for i in range(len(gps)):
#     ax[i].scatter(lon_plot[i],lat_plot[i])
    
# # ax[1].scatter(hgdLon,hgdLat)
# # ax[2].scatter(cryLon,cryLat)

# fig.show()


# In[ ]:


import time

def main():
    velocity = 25.0  # 차량 이동속도(단위: km/h)
    period = 3  # 전송 주기(단위: 초)
    
    waypoint = []
    for i in range(len(gps)):
        waypoint.append(buildWaypoint(gps[i], velocity=velocity, period=period))
    
    c=[0,0,0,0,0,0,0,0,0,0]

    while(True):
        # i = 장비 번호
        for i in range(len(gps)):
            # "c[i]" = 각 장비별 카운트
            c[i]= c[i]+1 if c[i]<len(waypoint[i])-1 else 0
            lat = waypoint[i][c[i]][0]
            lon = waypoint[i][c[i]][1]
            
            coldSerNum = "PLZ2022C"+str(i+2)
            phoneNumStr = "010010010"+(("0" + str(i+2)) if i+2<10 else str(i+2))
            vehicleDeviceNum = "PLZ2022V"+str(i+2)
            
            print("「---------","no.",i+2,":",c[i],"/",len(waypoint[i])," : ",coldSerNum,phoneNumStr,vehicleDeviceNum,"----------")
            HttpPost_cold(lat, lon, "http://gps.plzlab.com/coldChain/insert", coldSerNum)
            HttpPost_vehicle(lat, lon, "http://gps.plzlab.com/pmIot/devices/SUL01", phoneNumStr, vehicleDeviceNum)

        time.sleep(period)
        
#         HttpPost_cold(yLat, yLon, "http://gps.plzlab.com/coldChain/insert", "PLZ2022C4")
#         HttpPost_vehicle(yLat, yLon, "http://gps.plzlab.com/pmIot/devices/SUL01", "01001001004", "PLZ2022V4")
        
        
#         h= 0 if h>=hLen-1 else h+1
#         hLat = hgd_waypoint[h][0]
#         hLon = hgd_waypoint[h][1]

#         print("「---------","no3(황금동)",h,"/",hLen,"----------")
#         HttpPost_cold(hLat, hLon, "http://gps.plzlab.com/coldChain/insert", "PLZ2022C3")
#         HttpPost_vehicle(hLat, hLon, "http://gps.plzlab.com/pmIot/devices/SUL01", "01001001003", "PLZ2022V3")
# #         HttpPost_cold(hLat, hLon, "http://gps.plzlab.com/coldChain/insert", "PLZ2022C5")
# #         HttpPost_vehicle(hgd_waypoint[h][0], hgd_waypoint[h][1], "http://gps.plzlab.com/pmIot/devices/SUL01", "01001001005", "PLZ2022V5")

#         c= c+1 if c<cLen-1 else 0
#         cLat = cry_waypoint[c][0]
#         cLon = cry_waypoint[c][1]

#         print("「---------","no4(율곡동)",c,"/",cLen,"----------")
#         HttpPost_cold(cLat, cLon, "http://gps.plzlab.com/coldChain/insert", "PLZ2022C4")
#         HttpPost_vehicle(cLat, cLon, "http://gps.plzlab.com/pmIot/devices/SUL01", "01001001004", "PLZ2022V4")
    
        
        
main()


# In[ ]:




