# Internet Explorer에서 https://trac.osgeo.org/osgeo4w/ 접속하여 ​OSGeo4W network installer로 설치
# 설치는 https://blog.naver.com/8iseoii/221622615818 참고
# qgis-full: QGIS Full Desktop 선택하고 설치
# pip install pyproj==2.4.1
# pip install --upgrade pyproj
# pip3 install -U pyproj Proj
# test
# test 2

from pyproj import Proj, transform

# 구형 좌표계 설정 : EPSG:4326
WGS84 = {'proj':'latlong', 'datum':'WGS84', 'ellps':'WGS84',}

# 투영 좌표계 설정 : KATEC
KATEC = {'proj':'tmerc', 'lat_0':'38N', 'lon_0':'128E', 'ellps':'bessel',
   'x_0':'400000', 'y_0':'600000', 'k':'0.9999', 'a':'6377397.155', 'b':'6356078.9628181886',
   'towgs84':'-115.80,474.99,674.11,1.16,-2.31,-1.63,6.43', 'units':'m'}

inProj = Proj(**WGS84)
outProj = Proj(**KATEC)

x1, y1 = 126, 38
x2, y2 = transform(inProj, outProj, x1, y1) # 구형 좌표계를 투영 좌표계로 변환
print(x2,y2)