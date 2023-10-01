import math
class Reward:
    
    def __init__(self,params):

        self.speed=params['speed']
        self.waypoints=params['waypoints']
        self.closest_waypoints=params['closest_waypoints']
        self.heading = params['heading']
        self.distance_from_center=params['distance_from_center']
        self.track_width=params['track_width']
        self.steering=params['steering_angle']
        self.steps=params['steps']
        self.progress=params['progress']
        self.MIN_REWARD=-1e3
        
    def speed_reward(self,current_reward):
        # If speed up  more reward

        if self.speed>=1.0:
            current_reward+=(self.speed*1.2)
        elif 1.0>self.speed>=0.9:
            current_reward+=(self.speed)
        elif 0.9>self.speed>=0.8:
            current_reward+=(self.speed*0.8)
            
        return current_reward
        

    def direction_reward(self,current_reward):


        next_point = self.waypoints[self.closest_waypoints[1]]
        prev_point = self.waypoints[self.closest_waypoints[0]]

        # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
        direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
        # Convert to degrees
        direction = math.degrees(direction)

        # Calculate difference between track direction and car heading angle
        direction_diff = abs(direction - self.heading)

        # Positive reward if the difference between track direction and car heading angle low
        
        if direction_diff<=10:
            current_reward +=(self.speed*1.2)
        else:
            current_reward =self.MIN_REWARD
        return current_reward
    
        
        
    def distance_from_center_reward(self,current_reward):
        marker_1 = 0.10 * self.track_width
        marker_2 = 0.25* self.track_width
        marker_3 = 0.5 * self.track_width
        # Give higher reward if the car is closer to center     line and vice versa
        if self.distance_from_center <= marker_1:
            current_reward += (self.speed*1.2)
        elif self.distance_from_center <= marker_2:
            current_reward += (self.speed*0.6)
        elif self.distance_from_center <= marker_3:
            current_reward += (self.speed*0.1)
        else:
            current_reward = self.MIN_REWARD
        return current_reward
        
    def cut_corner_reward(self,current_reward):
        marker=0.25*self.track_width
        # when car turn right incentivizes to cut corner
        if self.steering<-18 and self.distance_from_center >marker:
            current_reward+=self.speed
        # while car turn left incentivizes to close center
        elif self.steering>18 and self.distance_from_center <marker:
            current_reward+=self.speed        
        return current_reward
    
    def progress_reward(self,current_reward):
        #EXPECTED TOTAL STEP 15 step p/s x 180 seconds
        TOTAL_NUM_STEPS = 2700
        
        if (self.steps % 10) == 0 and self.progress > (self.steps / TOTAL_NUM_STEPS)  :
            current_reward += 10
        return current_reward

            
def reward_function(params):
    reward=0
    reward_object=Reward(params)
    reward = reward_object.progress_reward(reward)
    reward = reward_object.speed_reward(reward)
    reward = reward_object.cut_corner_reward(reward)
    reward = reward_object.direction_reward(reward)
    reward = reward_object.distance_from_center_reward(reward)

    return float(reward)
    
