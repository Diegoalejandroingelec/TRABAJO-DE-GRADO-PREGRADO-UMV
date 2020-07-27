import math

def deg2utm(latitude,longitude):
    sa = 6378137.000000
    sb = 6356752.314245  
    e = math.sqrt(math.pow(sa,2)-math.pow(sb,2))/sb
    e_square = math.pow(e,2)
    c = (math.pow(sa,2))/sb
    lat = latitude * (math.pi/180)
    lon = longitude * (math.pi/180)
    
    if lon > 0:
        Huso = math.ceil((longitude/6)+31)
    else:
        Huso = math.floor((longitude/6)+31)
    
    S = (Huso*6)-183
    dS = lon - (S*(math.pi/180))
    if latitude < -72:
        zone = 'C'
    elif latitude < -64:
        zone = 'D'
    elif latitude < -56:
        zone = 'E'
    elif latitude < -48:
        zone = 'F'
    elif latitude < -40:
        zone = 'G'
    elif latitude < -32:
        zone = 'H'
    elif latitude < -24:
        zone = 'J'
    elif latitude < -16:
        zone = 'K'
    elif latitude <-8:
        zone = 'L'
    elif latitude < 0:
        zone = 'M'
    elif latitude <8:
        zone = 'N'
    elif latitude <16:
        zone = 'P'
    elif latitude <24:
        zone = 'Q'
    elif latitude <32:
        zone = 'R'
    elif latitude <40:
        zone = 'S'
    elif latitude <48:
        zone = 'T'
    elif latitude <56:
        zone = 'U'
    elif latitude <64:
        zone = 'V'
    elif latitude <72:
        zone = 'W'
    else:
        zone = 'X'
        
    a = math.cos(lat)*math.sin(dS)
    epsilon = 0.5 * math.log((1+a)/(1-a))
    nu = math.atan2(math.tan(lat),math.cos(dS))-lat
    tao = (e_square/2)*math.pow(epsilon,2)*math.pow(math.cos(lat),2)
    v = (c/math.sqrt((1+e_square*math.pow(math.cos(lat),2))))*0.9996
    a1 = math.sin(2*lat)
    a2 = a1*math.pow(math.cos(lat),2)
    alfa = (3/4)*e_square
    beta = (5/3)*math.pow(alfa,2)
    gama = (35/27)*math.pow(alfa,3)
    j2 = lat+(a1/2)
    j4 = ((3*j2)+a2)/4
    j6 = (5*j4)+(a2*math.pow(math.cos(lat), 2))/3
    Bm = 0.9996*c*(lat-alfa*j2+beta*j4-gama*j6)
    x = epsilon*v*(1+(tao/3))+500000
    y = nu*v*(1+tao)+Bm
    zone = str(Huso)+zone
    
    return x,y,zone
    
      

def utm2deg(x,y,utmzone):
    zone_n = int(utmzone[0:2])
    zone_l = utmzone[2]
    
    sa = 6378137.000000
    sb = 6356752.314245  
    e = math.sqrt(math.pow(sa,2)-math.pow(sb,2))/sb
    e_square = math.pow(e,2)
    c = (math.pow(sa,2))/sb
    x = x - 500000
    
    if zone_l < 'M':
        y = y - 10000000
    
    S = (zone_n*6)-183
    lat =  y/(6366197.724*0.9996)
    v = (c/math.sqrt((1+e_square*math.pow(math.cos(lat),2))))*0.9996
    a = x/v
    a1 = math.sin(2*lat)
    a2 = a1*math.pow(math.cos(lat),2)
    alfa = (3/4)*e_square
    beta = (5/3)*math.pow(alfa,2)
    gama = (35/27)*math.pow(alfa,3)
    j2 = lat+(a1/2)
    j4 = ((3*j2)+a2)/4
    j6 = (5*j4)+(a2*math.pow(math.cos(lat), 2))/3
    Bm = 0.9996*c*(lat-alfa*j2+beta*j4-gama*j6)
    b = (y-Bm)/v
    Epsi = ((e_square*math.pow(a,2))/2) * math.pow(math.cos(lat),2)
    Eps = a*(1-(Epsi/3))
    nab = (b*(1-Epsi))+lat
    senoheps = (math.exp(Eps)-math.exp(-Eps))/2
    Delt = math.atan2(senoheps,(math.cos(nab)))
    Tao = math.atan(math.cos(Delt)*math.tan(nab))
    longitude = (Delt *(180 / math.pi ) ) + S
    latitude = ( lat + ( 1 + e_square* math.pow(math.cos(lat),2) - (3/2)*e_square*math.sin(lat)*math.cos(lat)*(Tao-lat))*(Tao - lat ) ) * (180 / math.pi)
    
    return latitude,longitude


def move_position(latitude,longitude,noth_angle,distance,angle):
    
    x,y,utmzone = deg2utm(latitude,longitude)
    if noth_angle > angle:
        new_angle = 360 - (noth_angle-angle)
        if new_angle <= 90:
            new_x = x + (distance*math.sin(new_angle*(math.pi/180)))
            new_y = y + (distance*math.cos(new_angle*(math.pi/180)))
            
        elif new_angle <= 180:
            new_angle -= 90
            new_x = x + (distance*math.cos(new_angle*(math.pi/180)))
            new_y = y - (distance*math.sin(new_angle*(math.pi/180)))
            
        elif new_angle <= 270:
            new_angle -= 180
            new_x = x - (distance*math.sin(new_angle*(math.pi/180)))
            new_y = y - (distance*math.cos(new_angle*(math.pi/180))) 
        else:
            new_angle -=270
            new_x = x - (distance*math.cos(new_angle*(math.pi/180)))
            new_y = y + (distance*math.sin(new_angle*(math.pi/180)))
    else:
        new_angle = 360 - (angle-noth_angle)
        if new_angle <= 90:
            new_x = x - (distance*math.sin(new_angle*(math.pi/180)))
            new_y = y + (distance*math.cos(new_angle*(math.pi/180)))
            
        elif new_angle <= 180:
            new_angle -= 90
            new_x = x - (distance*math.cos(new_angle*(math.pi/180)))
            new_y = y - (distance*math.sin(new_angle*(math.pi/180)))
            
        elif new_angle <= 270:
            new_angle -= 180
            new_x = x + (distance*math.sin(new_angle*(math.pi/180)))
            new_y = y - (distance*math.cos(new_angle*(math.pi/180))) 
        else:
            new_angle -=270
            new_x = x + (distance*math.cos(new_angle*(math.pi/180)))
            new_y = y + (distance*math.sin(new_angle*(math.pi/180)))
    new_latitude,new_longitude = utm2deg(new_x, new_y, utmzone)
    
    return new_latitude,new_longitude

def Great_Circle_distance(latitude1,longitude1,latitude2,longitude2):
    r = 6371008.8
    dlat = (latitude1-latitude2)*math.pi/180
    dlon = (longitude1-longitude2)*math.pi/180
    lat1 = latitude1*math.pi/180
    lat2 = latitude2*math.pi/180
    a = math.pow(math.sin(dlat/2),2)+math.cos(lat1)*math.cos(lat2)*math.pow(math.sin(dlon/2),2)
    b = 2*math.asin(math.sqrt(a))
    distance = r*b
    
    return distance