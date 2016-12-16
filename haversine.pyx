cdef extern from "math.h":
    double cos(double theta)
    double sin(double theta)
    double asin(double theta)
    double sqrt(double x)
    double fabs(double x)
 
def haversine(double lon1,double lat1,double lon2,double lat2):
    cdef double r = 6371.0
    cdef double pi = 3.14159265
    cdef double x = pi/180.0
    cdef double dlon,dlat,a,b,c
    dlon = (lon2-lon1)*(x)
    lat1 = lat1*(x)
    lat2 = lat2*(x)
    dlat = lat2-lat1
    a = sin(dlat/2)*sin(dlat/2)+cos(lat1) * cos(lat2) * sin(dlon/2)* sin(dlon/2)
    c = 2*asin(sqrt(a))
    return r*c*1000

def Candinate(double t_lon,double t_lat,double s_lon,double s_lat,\
              double e_lon,double e_lat,double se):
    cdef double st,te,flag,dis,lon,lat
    st = haversine(t_lon,t_lat,s_lon,s_lat)
    te = haversine(t_lon,t_lat,e_lon,e_lat)
    flag = (st*st+se*se-te*te)/(2*se*se)
    if flag <= 0:
        dis = st
        lon = s_lon
        lat = s_lat
    elif flag >= 1:
        dis = te
        lon = e_lon
        lat = e_lat        
    else:
        dis = sqrt(fabs(st*st-(flag*se)*(flag*se)))
        lon = flag*(e_lon-s_lon)+s_lon
        lat = flag*(e_lat-s_lat)+s_lat
    return dis,lon,lat
    
    
def condition(double a1,double a2,\
              double b1,double b2,double b3,double b4,\
              double c1,double c2,double c3,double c4,\
              double d1,double d2,double d3,double d4,\
              double e1,double e2,double e3,double e4):
    cdef int a,b,c,d,e,result
    if (a1>(1000-a2)):
        a = 1
    else:
        a = 0
    if (b1<b2)and(b3>b4):
        b=1
    else:
        b=0
    if (c1<c2)and(c3>c4):
        c=1
    else:
        c=0
    if (d1<d2)and(d3>d4):
        d=1
    else:
        d=0
    if (e1<e2)and(e3>e4):
        e=1
    else:
        e=0
    if a or (b and c and d and e):
        result=1
    else:
        result=0    
    return result
        