from math import atan2, pi, sqrt, sin, cos

def direction(point_1, point_2):
    x = point_2[0] - point_1[0]
    y = point_2[1] - point_1[1]
    return compass_lock(atan2(y, x))
    
def distance(point_1, point_2):
    x = point_2[0] - point_1[0]
    y = point_2[1] - point_1[1]
    return sqrt(x**2 + y**2)
    
def compass_lock(angle, positive_range=True):
    if positive_range:
        # 6 is ~2*pi
        if angle >= 6:
            angle %= 2*pi
            
        while angle < 0:
            angle += 2*pi
            
        return angle
    else:
        # 6 is ~2*pi
        while angle >= pi:
            angle -= 2*pi
            
        while angle < -pi:
            angle += 2*pi
            
        return angle
        
def collide_point_square(point, topleft, bottomright, angle=0):
    if angle != 0:
        center = (topleft[0] + abs(topleft[0] - bottomright[0]) / 2, topleft[1] + abs(topleft[1] - bottomright[1]) / 2)
        #print(center, point)
        point_distance = distance(center, point)
        point_angle = direction(center, point)
        angle += point_angle
        point = (point_distance*cos(angle)+center[0], point_distance*sin(angle)+center[1])
        #print (point)
        
    if topleft[0] <= point[0] <= bottomright[0]:
        if topleft[1] <= point[1] <= bottomright[1]:
            #print (True)
            return True
    #print(False)
    return False