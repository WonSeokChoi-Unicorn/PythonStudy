import pyproj

KATEC = "+proj=tmerc +lat_0=38N +lon_0=128E +ellps=bessel +x_0=400000 +y_0=600000 +k=0.9999 +units=m +towgs84=-115.80,474.99,674.11,1.16,-2.31,-1.63,6.43"
WGS84 = "+proj=latlong +datum=WGS84 +ellps=WGS84"

KATEC_proj = pyproj.CRS(KATEC)
WGS84_proj = pyproj.CRS(WGS84)

def from_to_coords(fromcoords, tocoords, x, y):
    trans_func = pyproj.Transformer.from_crs(fromcoords, tocoords, always_xy = True)
    return trans_func.transform(x, y)

# 경기 수원시 영통구 영통동 1069 망포역 수인분당선
print(from_to_coords(WGS84_proj, KATEC_proj, 127.05686152624504, 37.245814939981706))