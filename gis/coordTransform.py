import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.14159265358979324  # 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 0.00669342162296594323  # 扁率


class CoordTransform(object):
    """docstring for ClassName"""

    # def __init__(self):

    def bd09_to_wgs84(self, bd_lon, bd_lat):
        lon, lat = self.bd09_to_gcj02(bd_lon, bd_lat)
        return self.gcj02_to_wgs84(lon, lat)

    def gcj02_to_wgs84(self, lng, lat):
        """
        GCJ02(火星坐标系)转GPS84
        :param lng:火星坐标系的经度
        :param lat:火星坐标系纬度
        :return:
        """
        if self.out_of_china(lng, lat):
            return lng, lat
        dlat = self._transformlat(lng - 105.0, lat - 35.0)
        dlng = self._transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * pi
        magic = math.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
        dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [lng * 2 - mglng, lat * 2 - mglat]

    def bd09_to_gcj02(self, bd_lon, bd_lat):
        """
        百度坐标系(BD-09)转火星坐标系(GCJ-02)
        百度——>谷歌、高德
        :param bd_lat:百度坐标纬度
        :param bd_lon:百度坐标经度
        :return:转换后的坐标列表形式
        """
        x = bd_lon - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
        gg_lng = z * math.cos(theta)
        gg_lat = z * math.sin(theta)
        return [gg_lng, gg_lat]

    def gcj02_to_bd09(self, lng, lat):
        """
        火星坐标系(GCJ-02)转百度坐标系(BD-09)
        谷歌、高德——>百度
        :param lng:火星坐标经度
        :param lat:火星坐标纬度
        :return:
        """
        z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
        theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return [bd_lng, bd_lat]

    def wgs84_to_bd09(self, lon, lat):
        lon, lat = self.wgs84_to_gcj02(lon, lat)
        return self.gcj02_to_bd09(lon, lat)

    def wgs84_to_gcj02(self, lng, lat):
        """
        WGS84转GCJ02(火星坐标系)
        :param lng:WGS84坐标系的经度
        :param lat:WGS84坐标系的纬度
        :return:
        """
        if self.out_of_china(lng, lat):  # 判断是否在国内
            return lng, lat
        dlat = self._transformlat(lng - 105.0, lat - 35.0)
        dlng = self._transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * pi
        magic = math.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
        dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [mglng, mglat]

    def _transformlat(self, lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
                math.sin(2.0 * lng * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * pi) + 40.0 *
                math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
                math.sin(lat * pi / 30.0)) * 2.0 / 3.0
        return ret

    def _transformlng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
                math.sin(2.0 * lng * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * pi) + 40.0 *
                math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
                math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
        return ret

    def out_of_china(self, lng, lat):
        """
        判断是否在国内，不在国内不做偏移
        :param lng:
        :param lat:
        :return:
        """
        return not (lng > 72.004 and lng < 137.8347 and lat > 0.8293 and lat < 55.8271)

    def rad(self, d):
        d=d%360
        return d * math.pi / 180.0

    # 单位:米
    def distance(self, x1, y1, x2, y2):
        dLat=self.rad(y2-y1)
        dLon=self.rad(x2-x1)
        lat1=self.rad(y1)
        lat2=self.rad(y2)
        a = math.pow(math.sin(dLat / 2), 2) +math.pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2);
        s=2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        earth_radius = 6371008.8
        s = s * earth_radius
        if s < 0:
            return -s
        else:
            return s
