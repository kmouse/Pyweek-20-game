from code.calculations import collide_point_square

def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z
    

class Screen_Object:
    offset = (0, 0)
    def move(self):
        self.x += Screen_Object.offset[0]
        self.y += Screen_Object.offset[1]
        
        
        
        
class Data_Type(Screen_Object):
    # A class variable to check if there is already a data_type grabbed
    grabbed = False
    data = 0
    stored_data = 0
        
    def carry(self, x, y, pressed):
        if collide_point_square((x, y), self.rect.topleft, self.rect.bottomright):
            if pressed and self.carried == 0 and Data_Type.grabbed == False:
                self.carried = 2
                Data_Type.grabbed = True
        elif (pressed or Data_Type.grabbed == True) and self.carried != 2:
            self.carried = 1
        if not pressed:
            Data_Type.grabbed = False
            self.carried = 0
        
        if self.carried == 2:
            self.x = x
            self.y = y
            
        self.rect.center = self.x, self.y
            
    def right_click(self, x, y, pressed):
        if collide_point_square((x, y), self.rect.topleft, self.rect.bottomright):
            if pressed:
                return (merge_dicts(self.exponent_data, self.linear_data))
        return None
            
    # self.exponent_data should be a dict with all the counted data
    def count_data(self):
        bits = 0
        for point in self.exponent_data:
            bits += get_data_size_int(self.exponent_data[point])
        bits += STATIC_DATA_COST*len(self.linear_data)
        # X, y are also attributes
        bits += 2 * STATIC_DATA_COST
        return bits