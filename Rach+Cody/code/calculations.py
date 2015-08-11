from math import atan2, pi

def direction(point_1, point_2):
    x = point_2[0] - point_1[0]
    y = point_2[1] - point_1[1]
    return compass_lock(atan2(y, x))
    
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
        
def collide_point_square(point, topleft, bottomright):
    if topleft[0] <= point[0] <= bottomright[0]:
        if topleft[1] <= point[1] <= bottomright[1]:
            return True
    return False