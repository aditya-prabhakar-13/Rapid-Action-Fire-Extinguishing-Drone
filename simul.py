import pybullet as p
import pybullet_data
import time
import numpy as np
import os
import urllib.request
from PIL import Image
import random
from collections import deque
import math
import random

# Connect to the PyBullet physics server
physicsClient = p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)
p.setGravity(0, 0, -9.81)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Create textures directory
textures_dir = "textures"
os.makedirs(textures_dir, exist_ok=True)

def create_texture(filename, color, size=(512, 512)):
    img = Image.new('RGB', size, color)
    filepath = os.path.join(textures_dir, filename)
    img.save(filepath)
    return filepath

class FireParticleSystem:
    def __init__(self, position, max_particles=100):
        self.position = position
        self.max_particles = max_particles
        self.particles = deque(maxlen=max_particles)
        self.colors = [
            [1.0, 0.3, 0.1, 0.7],
            [1.0, 0.5, 0.0, 0.6],
            [1.0, 0.7, 0.0, 0.5],
            [0.8, 0.8, 0.0, 0.4],
            [0.6, 0.6, 0.6, 0.3],
            [0.4, 0.4, 0.4, 0.2],
            [0.2, 0.2, 0.2, 0.1]
        ]
        
    def update(self):
        active_particles = []
        for particle in self.particles:
            particle_id, life, velocity = particle
            if life > 0:
                pos, orn = p.getBasePositionAndOrientation(particle_id)
                new_pos = [pos[0] + velocity[0], 
                          pos[1] + velocity[1], 
                          pos[2] + velocity[2]]
                p.resetBasePositionAndOrientation(particle_id, new_pos, orn)
                
                color_index = int((1.0 - life) * len(self.colors))
                if color_index >= len(self.colors):
                    color_index = len(self.colors) - 1
                p.changeVisualShape(particle_id, -1, rgbaColor=self.colors[color_index])
                
                active_particles.append((particle_id, life - 0.01, velocity))
            else:
                p.removeBody(particle_id)
        
        self.particles = deque(active_particles, maxlen=self.max_particles)
        
        if len(self.particles) < self.max_particles:
            self.spawn_particle()
    
    def spawn_particle(self):
        vx = random.uniform(-0.02, 0.02)
        vy = random.uniform(-0.02, 0.02)
        vz = random.uniform(0.05, 0.12)
        
        radius = random.uniform(0.1, 0.2)
        
        visual_id = p.createVisualShape(
            shapeType=p.GEOM_SPHERE,
            radius=radius,
            rgbaColor=self.colors[0]
        )
        
        x_offset = random.uniform(-0.2, 0.2)
        y_offset = random.uniform(-0.2, 0.2)
        particle_id = p.createMultiBody(
            baseMass=0,
            baseVisualShapeIndex=visual_id,
            basePosition=[self.position[0] + x_offset, 
                         self.position[1] + y_offset, 
                         self.position[2]]
        )
        
        self.particles.append((particle_id, 1.0, [vx, vy, vz]))

# Create textures with appropriate colors
dark_wall_texture = create_texture("dark_wall.png", (60, 120, 90))
wood_floor_texture = create_texture("wood_floor.png", (150, 120, 90))
gray_sofa_texture = create_texture("gray_sofa.png", (120, 120, 125))
dark_brown_wood = create_texture("dark_brown_wood.png", (500, 45, 35))
light_gray_texture = create_texture("light_gray.png", (200, 200, 200))
black_texture = create_texture("black.png", (20, 20, 20))
glass_texture = create_texture("glass.png", (200, 220, 255, 100))
carpet_texture = create_texture("carpet.png", (100, 100, 110))

# Room dimensions
room_width = 10
room_length = 12
room_height = 6
wall_thickness = 0.2

# Create floor with wood texture
floor_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[room_width/2, room_length/2, 0.1])
floor_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[room_width/2, room_length/2, 0.1], 
                                rgbaColor=[0.8, 0.6, 0.4, 1])
floor = p.createMultiBody(0, floor_shape, floor_visual, [0, 0, -0.1])
floor_texture_id = p.loadTexture(wood_floor_texture)
p.changeVisualShape(floor, -1, textureUniqueId=floor_texture_id)

# Create walls
back_wall_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[room_width/2, wall_thickness/2, room_height/2])
back_wall_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[room_width/2, wall_thickness/2, room_height/2], 
                                    rgbaColor=[0.15, 0.15, 0.15, 1])
back_wall = p.createMultiBody(0, back_wall_shape, back_wall_visual, [0, -room_length/2, room_height/2])
wall_texture_id = p.loadTexture(dark_wall_texture)
p.changeVisualShape(back_wall, -1, textureUniqueId=wall_texture_id)

# Left wall
left_wall_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[wall_thickness/2, room_length/2, room_height/2])
left_wall_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[wall_thickness/2, room_length/2, room_height/2], 
                                    rgbaColor=[0.15, 0.15, 0.15, 1])
left_wall = p.createMultiBody(0, left_wall_shape, left_wall_visual, [-room_width/2, 0, room_height/2])
p.changeVisualShape(left_wall, -1, textureUniqueId=wall_texture_id)

# Right wall with windows
top_frame_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[wall_thickness/2, room_length/2, 0.2])
top_frame_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[wall_thickness/2, room_length/2, 0.2], 
                                    rgbaColor=[0.3, 0.3, 0.3, 1])
top_frame = p.createMultiBody(0, top_frame_shape, top_frame_visual, [room_width/2, 0, room_height-0.2])

bottom_frame_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[wall_thickness/2, room_length/2, 0.2])
bottom_frame_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[wall_thickness/2, room_length/2, 0.2], 
                                       rgbaColor=[0.3, 0.3, 0.3, 1])
bottom_frame = p.createMultiBody(0, bottom_frame_shape, bottom_frame_visual, [room_width/2, 0, 0.2])

# Middle divider
mid_divider_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[wall_thickness/2, room_length/2, 0.1])
mid_divider_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[wall_thickness/2, room_length/2, 0.1], 
                                      rgbaColor=[0.3, 0.3, 0.3, 1])
mid_divider = p.createMultiBody(0, mid_divider_shape, mid_divider_visual, [room_width/2, 0, room_height/2])

# Vertical window dividers
for i in range(4):
    pos_y = -room_length/2 + i*(room_length/4)
    vert_divider_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[wall_thickness/2, 0.1, room_height/2])
    vert_divider_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[wall_thickness/2, 0.1, room_height/2], 
                                          rgbaColor=[0.3, 0.3, 0.3, 1])
    vert_divider = p.createMultiBody(0, vert_divider_shape, vert_divider_visual, [room_width/2, pos_y, room_height/2])

# Glass panels for windows
for i in range(3):
    pos_y = -room_length/2 + (i+0.5)*(room_length/4)
    # Upper glass
    upper_glass_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, room_length/8-0.1, room_height/4-0.2])
    upper_glass_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.05, room_length/8-0.1, room_height/4-0.2], 
                                         rgbaColor=[0.9, 0.9, 0.95, 0.2])
    upper_glass = p.createMultiBody(0, upper_glass_shape, upper_glass_visual, [room_width/2, pos_y, room_height*3/4])
for i in range(0):   
    # Lower glass
    lower_glass_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, room_length/8-0.1, room_height/4-0.2])
    lower_glass_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.05, room_length/8-0.1, room_height/4-0.2], 
                                         rgbaColor=[0.9, 0.9, 0.95, 0.2])
    lower_glass = p.createMultiBody(0, lower_glass_shape, lower_glass_visual, [room_width/2, pos_y, room_height/4])

# Ceiling
ceiling_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[room_width/2, room_length/2, 0.1])
ceiling_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[room_width/2, room_length/2, 0.1], 
                                  rgbaColor=[0.95, 0.95, 0.95, 1])
ceiling = p.createMultiBody(0, ceiling_shape, ceiling_visual, [0, 0, room_height+0.1])

# TV wall
tv_wall_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.1, 3, 1.5])
tv_wall_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.1, 3, 1.5], 
                                  rgbaColor=[0.3, 0.2, 0.15, 1])
tv_wall = p.createMultiBody(0, tv_wall_shape, tv_wall_visual, [-room_width/2+0.3, 0, 1.5])
p.changeVisualShape(tv_wall, -1, textureUniqueId=p.loadTexture(dark_brown_wood))

# Bookshelves
for i in range(4):
    shelf_height = 0.6 + i*0.8
    # Left bookshelf
    shelf_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.4, 1.2, 0.05])
    shelf_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.4, 1.2, 0.05], 
                                    rgbaColor=[0.3, 0.2, 0.15, 1])
    shelf = p.createMultiBody(0, shelf_shape, shelf_visual, [-room_width/2+0.5, -2.2, shelf_height])
    p.changeVisualShape(shelf, -1, textureUniqueId=p.loadTexture(dark_brown_wood))
    
    back_panel_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.02, 1.2, 0.4])
    back_panel_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.02, 1.2, 0.4], 
                                         rgbaColor=[0.25, 0.17, 0.13, 1])
    back_panel = p.createMultiBody(0, back_panel_shape, back_panel_visual, [-room_width/2+0.12, -2.2, shelf_height-0.4])
    p.changeVisualShape(back_panel, -1, textureUniqueId=p.loadTexture(dark_wall_texture))

    # Right bookshelf
    shelf = p.createMultiBody(0, shelf_shape, shelf_visual, [-room_width/2+0.5, 2.2, shelf_height])
    p.changeVisualShape(shelf, -1, textureUniqueId=p.loadTexture(dark_brown_wood))
    
    back_panel = p.createMultiBody(0, back_panel_shape, back_panel_visual, [-room_width/2+0.12, 2.2, shelf_height-0.4])
    p.changeVisualShape(back_panel, -1, textureUniqueId=p.loadTexture(dark_wall_texture))

# TV screen
tv_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 1.8, 1])
tv_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.05, 1.8, 1], 
                             rgbaColor=[0.05, 0.05, 0.05, 1])
tv = p.createMultiBody(0, tv_shape, tv_visual, [-room_width/2+0.45, 0, 1.5])
p.changeVisualShape(tv, -1, textureUniqueId=p.loadTexture(black_texture))

# Sofas
sofa1_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[1.8, 1, 0.4])
sofa1_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[1.8, 1, 0.4], 
                                rgbaColor=[0.7, 0.7, 0.7, 1])
sofa1 = p.createMultiBody(0, sofa1_shape, sofa1_visual, [2, -3, 0.4])
p.changeVisualShape(sofa1, -1, textureUniqueId=p.loadTexture(gray_sofa_texture))

sofa_corner_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[1, 1, 0.4])
sofa_corner_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[1, 1, 0.4], 
                                      rgbaColor=[0.7, 0.7, 0.7, 1])
sofa_corner = p.createMultiBody(0, sofa_corner_shape, sofa_corner_visual, [4, -2, 0.4])
p.changeVisualShape(sofa_corner, -1, textureUniqueId=p.loadTexture(gray_sofa_texture))

sofa2_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[1, 1.8, 0.4])
sofa2_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[1, 1.8, 0.4], 
                                rgbaColor=[0.7, 0.7, 0.7, 1])
sofa2 = p.createMultiBody(0, sofa2_shape, sofa2_visual, [5, 0, 0.4])
p.changeVisualShape(sofa2, -1, textureUniqueId=p.loadTexture(gray_sofa_texture))

# Sofa cushions
cushion_positions = [
    [2, -3, 0.9], [3.5, -3, 0.9], [0.5, -3, 0.9],  # First sofa
    [5, 0, 0.9], [5, 1.5, 0.9], [5, -1.5, 0.9]     # Second sofa
]

for pos in cushion_positions:
    cushion_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.4, 0.4, 0.1])
    cushion_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.4, 0.4, 0.1], 
                                      rgbaColor=[0.75, 0.75, 0.75, 1])
    cushion = p.createMultiBody(0, cushion_shape, cushion_visual, pos)
    p.changeVisualShape(cushion, -1, textureUniqueId=p.loadTexture(light_gray_texture))

# Coffee table
table_base_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.8, 0.8, 0.2])
table_base_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.8, 0.8, 0.2], 
                                     rgbaColor=[0.2, 0.2, 0.2, 1])
table_base = p.createMultiBody(0, table_base_shape, table_base_visual, [2, -0.5, 0.2])
p.changeVisualShape(table_base, -1, textureUniqueId=p.loadTexture(black_texture))

# Glass top
glass_top_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[1.2, 1.2, 0.02])
glass_top_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[1.2, 1.2, 0.02], 
                                    rgbaColor=[0.9, 0.9, 0.95, 0.3])
glass_top = p.createMultiBody(0, glass_top_shape, glass_top_visual, [2, -0.5, 0.42])
p.changeVisualShape(glass_top, -1, textureUniqueId=p.loadTexture(glass_texture))

# Area rug
rug_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[3, 3, 0.01])
rug_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[3, 3, 0.01], 
                              rgbaColor=[0.4, 0.4, 0.45, 1])
rug = p.createMultiBody(0, rug_shape, rug_visual, [2, -1, 0.01])
p.changeVisualShape(rug, -1, textureUniqueId=p.loadTexture(carpet_texture))

# Pendant light
light_base_shape = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.1, height=0.05)
light_base_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.1, length=0.05, 
                                     rgbaColor=[0.2, 0.2, 0.2, 1])
light_base = p.createMultiBody(0, light_base_shape, light_base_visual, [2, -1, room_height-0.05])

# Glass pendant lights
for i in range(8):
    angle = i * (2*np.pi/8)
    x = 2 + 0.5 * np.cos(angle)
    y = -1 + 0.5 * np.sin(angle)
    z = room_height - 0.5 - 0.1 * i
    
    wire_shape = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.01, height=0.5)
    wire_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.01, length=0.5, 
                                   rgbaColor=[0.1, 0.1, 0.1, 1])
    wire = p.createMultiBody(0, wire_shape, wire_visual, [x, y, room_height-0.25])
    
    bubble_shape = p.createCollisionShape(p.GEOM_SPHERE, radius=0.1)
    bubble_visual = p.createVisualShape(p.GEOM_SPHERE, radius=0.1, 
                                     rgbaColor=[0.9, 0.9, 0.9, 0.3])
    bubble = p.createMultiBody(0, bubble_shape, bubble_visual, [x, y, z])

# Create fire sources
fire_sources = [
    FireParticleSystem([random.randint(-4,4),random.randint(-4,4), 0.2], max_particles=100),
    FireParticleSystem([random.randint(-4,4),random.randint(-4,4), 0.2], max_particles=100),
    FireParticleSystem([random.randint(-4,4),random.randint(-4,4), 0.2], max_particles=100),
    FireParticleSystem([random.randint(-4,4),random.randint(-4,4), 0.2], max_particles=100),
    FireParticleSystem([random.randint(-4,4),random.randint(-4,4), 0.2], max_particles=100),
    FireParticleSystem([random.randint(-4,4),random.randint(-4,4), 0.2], max_particles=100),
    FireParticleSystem([random.randint(-4,4),random.randint(-4,4), 0.2], max_particles=100),
    FireParticleSystem([random.randint(-4,4),random.randint(-4,4), 0.2], max_particles=100)
]

def create_drone(position, orientation):
    drone_body_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.15, 0.15, 0.05])
    drone_body_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.15, 0.15, 0.05], 
                                       rgbaColor=[0.2, 0.2, 0.2, 1])
    
    drone_mass = 1.0
    drone_id = p.createMultiBody(
        baseMass=drone_mass,
        baseCollisionShapeIndex=drone_body_shape,
        baseVisualShapeIndex=drone_body_visual,
        basePosition=position,
        baseOrientation=orientation
    )
    
    rotors = []
    for i, (x, y) in enumerate([(0.1, 0.1), (-0.1, 0.1), (-0.1, -0.1), (0.1, -0.1)]):
        rotor_shape = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.06, height=0.01)
        rotor_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.06, length=0.01, 
                                      rgbaColor=[0.8, 0.8, 0.8, 0.8])
        rotor = p.createMultiBody(
            baseMass=0.1,
            baseCollisionShapeIndex=rotor_shape,
            baseVisualShapeIndex=rotor_visual,
            basePosition=[position[0]+x, position[1]+y, position[2]+0.05]
        )
        rotors.append(rotor)
        
        p.createConstraint(
            parentBodyUniqueId=drone_id,
            parentLinkIndex=-1,
            childBodyUniqueId=rotor,
            childLinkIndex=-1,
            jointType=p.JOINT_FIXED,
            jointAxis=[0, 0, 0],
            parentFramePosition=[x, y, 0.05],
            childFramePosition=[0, 0, 0]
        )
    
    tank_shape = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.06, height=0.1)
    tank_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.06, length=0.1, 
                                  rgbaColor=[1, 0, 0, 1])
    tank = p.createMultiBody(
        baseMass=0.5,
        baseCollisionShapeIndex=tank_shape,
        baseVisualShapeIndex=tank_visual,
        basePosition=[position[0], position[1], position[2]-0.1]
    )
    
    p.createConstraint(
        parentBodyUniqueId=drone_id,
        parentLinkIndex=-1,
        childBodyUniqueId=tank,
        childLinkIndex=-1,
        jointType=p.JOINT_FIXED,
        jointAxis=[0, 0, 0],
        parentFramePosition=[0, 0, -0.1],
        childFramePosition=[0, 0, 0]
    )
    
    return drone_id, rotors, tank

class DroneController:
    def __init__(self, drone_id, initial_position):
        self.drone_id = drone_id
        self.initial_position = initial_position
        self.current_position = initial_position
        
        self.drone_mass = 1.0
        self.max_force = 120.0
        self.hover_height = 2.3
        
        self.STATE_TAKEOFF = 0
        self.STATE_SEARCH_FIRE = 1
        self.STATE_APPROACH_FIRE = 2
        self.STATE_EXTINGUISH_FIRE = 3
        self.STATE_MISSION_COMPLETE = 4
        
        self.state = self.STATE_TAKEOFF
        
        self.detected_fires = []
        self.current_fire_target = None
        
        self.extinguishing_particles = []
        self.is_extinguishing = False
        self.extinguishing_start_time = 0
        self.extinguishing_duration = 3

    def update(self, fire_positions, obstacles):
        if time.time() % 0.5 < 0.1:
            print(f"Drone state: {self.state}, Is extinguishing: {self.is_extinguishing}, Target: {self.current_fire_target}")
        
        pos, orn = p.getBasePositionAndOrientation(self.drone_id)
        self.current_position = pos
        
        print(f"Drone state: {self.state}, position: {[round(p,2) for p in pos]}")
        
        if self.state == self.STATE_TAKEOFF:
            target = [self.initial_position[0], self.initial_position[1], self.hover_height]
            self._apply_flight_control(target, obstacles)
            
            if abs(pos[2] - self.hover_height) < 1.0:
                self.state = self.STATE_SEARCH_FIRE
                print("Takeoff complete. Searching for fires...")
        
        elif self.state == self.STATE_SEARCH_FIRE:
            self._detect_fires(fire_positions)
            
            if self.detected_fires:
                self.current_fire_target = self._find_closest_fire(self.detected_fires)
                self.state = self.STATE_APPROACH_FIRE
                print(f"Fire detected at {self.current_fire_target}. Moving to extinguish.")
            else:
                t = time.time() * 0.3
                
                radius = 1.0 + (t % 5)
                search_pos = [
                    2 + radius * math.sin(t),
                    -1 + radius * math.cos(t),
                    self.hover_height
                ]
                
                if int(t) % 10 == 0 and t % 1 < 0.1:
                    search_pos = [
                        random.uniform(-4, 4),
                        random.uniform(-4, 4),
                        self.hover_height
                    ]
                    print(f"Exploring new area: {[round(x,2) for x in search_pos]}")
                    
                self._apply_flight_control(search_pos, obstacles)
        
        elif self.state == self.STATE_APPROACH_FIRE:
            if self.current_fire_target:
                target_pos = [
                    self.current_fire_target[0], 
                    self.current_fire_target[1], 
                    self.hover_height - 0.5
                ]
                self._apply_flight_control(target_pos, obstacles)
                
                distance_to_fire = self._distance([pos[0], pos[1], 0], 
                                               [self.current_fire_target[0], self.current_fire_target[1], 0])
                if distance_to_fire < 0.5:
                    p.addUserDebugLine(
                        self.current_position,
                        [self.current_fire_target[0], self.current_fire_target[1], 0],
                        [0, 0, 1],
                        lineWidth=10,
                        lifeTime=0.5
                    )
                    
                    for fire in fire_sources:
                        if (abs(fire.position[0] - self.current_fire_target[0]) < 1.0 and
                            abs(fire.position[1] - self.current_fire_target[1]) < 1.0):
                            fire.max_particles = 0
                            
                            for particle in list(fire.particles):
                                if isinstance(particle, tuple) and len(particle) > 0:
                                    p.removeBody(particle[0])
                            fire.particles.clear()
                            print(f"Fire at {fire.position} instantly extinguished!")
                            
                            if self.current_fire_target in self.detected_fires:
                                self.detected_fires.remove(self.current_fire_target)
                            self.current_fire_target = None
                            self.state = self.STATE_SEARCH_FIRE
                            break
            else:
                self.state = self.STATE_SEARCH_FIRE
                
        elif self.state == self.STATE_EXTINGUISH_FIRE:
            if self.is_extinguishing:
                if self.current_fire_target:
                    target = [
                        self.current_fire_target[0], 
                        self.current_fire_target[1], 
                        self.hover_height - 0.5
                    ]
                    self._apply_flight_control(target, obstacles)
                
                    p.addUserDebugLine(
                        self.current_position,
                        [self.current_fire_target[0], self.current_fire_target[1], 0],
                        [0, 0, 1],
                        lineWidth=5,
                        lifeTime=0.1
                    )
                
                    self._deploy_extinguishing_compound()
                    
                    for fire in fire_sources:
                        if (abs(fire.position[0] - self.current_fire_target[0]) < 1.0 and
                            abs(fire.position[1] - self.current_fire_target[1]) < 1.0):
                            fire.max_particles = max(0, fire.max_particles - 5)
                            if fire.max_particles % 10 == 0:
                                print(f"Extinguishing: {fire.max_particles} particles left")
                            
                            if fire.max_particles <= 0:
                                for particle in list(fire.particles):
                                    if isinstance(particle, tuple) and len(particle) > 0:
                                        p.removeBody(particle[0])
                                fire.particles.clear()
                                print(f"Fire at {fire.position} extinguished!")
                                
                                self.is_extinguishing = False
                                if self.current_fire_target in self.detected_fires:
                                    self.detected_fires.remove(self.current_fire_target)
                                self.current_fire_target = None
                                self.state = self.STATE_SEARCH_FIRE
                                print("Fire extinguished. Returning to search mode.")
                                break
                
                    extinguishing_elapsed = time.time() - self.extinguishing_start_time
                    if extinguishing_elapsed > self.extinguishing_duration and self.is_extinguishing:
                        print("Extinguishing timeout. Moving to next fire.")
                        self.is_extinguishing = False
                        if self.current_fire_target in self.detected_fires:
                            self.detected_fires.remove(self.current_fire_target)
                        self.current_fire_target = None
                        self.state = self.STATE_SEARCH_FIRE
            else:
                self.state = self.STATE_SEARCH_FIRE
                
        elif self.state == self.STATE_MISSION_COMPLETE:
            self._apply_flight_control([pos[0], pos[1], self.hover_height], obstacles)
    
    def _apply_flight_control(self, target_position, obstacles):
        pos, orn = p.getBasePositionAndOrientation(self.drone_id)
        lin_vel, ang_vel = p.getBaseVelocity(self.drone_id)
        
        if time.time() % 2 < 0.1:
            print(f"Moving toward: {[round(x,2) for x in target_position]}, Current position: {[round(x,2) for x in pos]}")
        
        avoid_vector = self._get_obstacle_avoidance_vector(pos, obstacles)
        
        adjusted_target = [
            target_position[0] + avoid_vector[0],
            target_position[1] + avoid_vector[1],
            target_position[2] + avoid_vector[2]
        ]
        
        kp = 1000.0
        kd = 1000.0
        
        error = [adjusted_target[i] - pos[i] for i in range(3)]
        
        force_p = [kp * error[i] for i in range(3)]
        force_d = [-kd * lin_vel[i] for i in range(3)]
        
        gravity_comp = [0, 0, 9.81 * self.drone_mass]
        
        total_force = [
            force_p[0] + force_d[0] + gravity_comp[0],
            force_p[1] + force_d[1] + gravity_comp[1],
            force_p[2] + force_d[2] + gravity_comp[2]
        ]
        
        self.max_force = 500.0
        
        for i in range(3):
            if abs(total_force[i]) > self.max_force:
                total_force[i] = self.max_force if total_force[i] > 0 else -self.max_force
        
        p.applyExternalForce(
            self.drone_id,
            -1,
            total_force,
            pos,
            p.WORLD_FRAME
        )
        
        force_scale = 0.02
        p.addUserDebugLine(
            pos,
            [pos[0] + total_force[0] * force_scale, 
             pos[1] + total_force[1] * force_scale, 
             pos[2] + total_force[2] * force_scale],
            [0, 1, 0],
            lifeTime=0.1
        )

    def _get_obstacle_avoidance_vector(self, position, obstacles):
        avoid_vector = [0, 0, 0]
        margin = 0.8
        
        for obstacle in obstacles:
            obstacle_pos = obstacle["position"]
            obstacle_size = obstacle["size"]
            
            dx = position[0] - obstacle_pos[0]
            dy = position[1] - obstacle_pos[1]
            dz = position[2] - obstacle_pos[2]
            
            distance_sq = dx*dx + dy*dy + dz*dz
            
            if distance_sq < (margin + max(obstacle_size)) ** 2:
                distance = math.sqrt(distance_sq)
                if distance > 0:
                    scale = max(0, margin - distance) / margin
                    avoid_vector[0] += dx / distance * scale
                    avoid_vector[1] += dy / distance * scale
                    avoid_vector[2] += dz / distance * scale
        
        return avoid_vector
   
    def _detect_fires(self, fire_positions):
        self.detected_fires = []
        
        if fire_positions and time.time() % 2 < 0.1:
            print(f"Available fire sources: {len(fire_positions)}")
        
        for fire_pos in fire_positions:
            distance = self._distance(self.current_position, fire_pos)
            
            if distance < 15.0 and fire_pos not in self.detected_fires:
                self.detected_fires.append(fire_pos)
                print(f"Fire detected at {fire_pos} (distance: {distance:.2f}m)")
        
                p.addUserDebugText(
                    "FIRE DETECTED",
                    [fire_pos[0], fire_pos[1], fire_pos[2] + 0.5],
                    textColorRGB=[1, 0, 0],
                    textSize=1.5,
                    lifeTime=2.0
                )

    def _deploy_extinguishing_compound(self):
        for _ in range(20):
            particle_pos = [
                self.current_position[0] + random.uniform(-0.2, 0.2),
                self.current_position[1] + random.uniform(-0.2, 0.2),
                self.current_position[2] - 0.5
            ]
            
            particle_visual = p.createVisualShape(
                p.GEOM_SPHERE,
                radius=0.25,
                rgbaColor=[0.9, 0.9, 0.9, 0.9]
            )

            p.addUserDebugText(
                "EXTINGUISHING",
                [self.current_position[0], self.current_position[1], self.current_position[2] + 0.5],
                [1, 0, 0],
                1.0,
                lifeTime=0.2
            )
             
            particle_id = p.createMultiBody(
                baseMass=0.01,
                baseVisualShapeIndex=particle_visual,
                basePosition=particle_pos
            )
            
            p.applyExternalForce(
                particle_id,
                -1,
                [0, 0, -2.0],
                particle_pos,
                p.WORLD_FRAME
            )
            
            self.extinguishing_particles.append((particle_id, time.time()))
        
        new_particles = []
        for particle_id, creation_time in self.extinguishing_particles:
            if time.time() - creation_time < 2.0:
                new_particles.append((particle_id, creation_time))
            else:
                p.removeBody(particle_id)
        self.extinguishing_particles = new_particles
        
    def _extinguish_fire(self):
        if self.current_fire_target:
            for fire in fire_sources:
                if (abs(fire.position[0] - self.current_fire_target[0]) < 0.5 and
                    abs(fire.position[1] - self.current_fire_target[1]) < 0.5):
                    fire.max_particles = max(0, fire.max_particles - 25)
                    
                    if fire.max_particles <= 0:
                        for particle in list(fire.particles):
                            if isinstance(particle, tuple) and len(particle) > 0:
                                p.removeBody(particle[0])
                        fire.particles.clear()
                        print(f"Fire at {fire.position} extinguished!")
                        break
                  
            if self.current_fire_target in self.detected_fires:
                self.detected_fires.remove(self.current_fire_target)
            
            self.current_fire_target = None
            self.detected_fires = []

    def _find_closest_fire(self, fire_list):
        closest_fire = None
        min_distance = float('inf')
        
        for fire_pos in fire_list:
            distance = self._distance(self.current_position, fire_pos)
            if distance < min_distance:
                min_distance = distance
                closest_fire = fire_pos
                
        return closest_fire
        
    def _distance(self, pos1, pos2):
        return math.sqrt(sum((pos1[i] - pos2[i])**2 for i in range(3)))
        
    def _check_fire_status(self):
        active_fires = 0
        for fire in fire_sources:
            if fire.max_particles > 0:
                active_fires += 1
        
        print(f"Status: {active_fires} active fires remaining in the room")
        return active_fires == 0

def identify_obstacles_in_room():
    obstacles = []
    
    fire_particle_ids = []
    for fire in fire_sources:
        for particle in fire.particles:
            if isinstance(particle, tuple) and len(particle) > 0:
                fire_particle_ids.append(particle[0])
    
    for i in range(p.getNumBodies()):
        if i == drone_id or i in fire_particle_ids:
            continue
            
        try:
            object_pos, object_orn = p.getBasePositionAndOrientation(i)
            
            collision_shapes = []
            
            try:
                shapes = p.getCollisionShapeData(i, -1)
                for shape in shapes:
                    collision_shapes.append(shape)
            except Exception:
                pass
                
            try:
                num_joints = p.getNumJoints(i)
                for j in range(num_joints):
                    try:
                        shapes = p.getCollisionShapeData(i, j)
                        for shape in shapes:
                            collision_shapes.append(shape)
                    except Exception:
                        pass
            except Exception:
                pass
            
            if collision_shapes:
                max_size = [0, 0, 0]
                try:
                    for shape in collision_shapes:
                        if len(shape) > 3:
                            shape_type = shape[2]
                            if shape_type == p.GEOM_BOX:
                                half_extents = shape[3]
                                max_size[0] = max(max_size[0], half_extents[0])
                                max_size[1] = max(max_size[1], half_extents[1])
                                max_size[2] = max(max_size[2], half_extents[2])
                            elif shape_type == p.GEOM_SPHERE:
                                radius = shape[3][0]
                                max_size = [radius, radius, radius]
                            elif shape_type == p.GEOM_CYLINDER:
                                radius = shape[3][0]
                                height = shape[3][1]
                                max_size = [radius, radius, height/2]
                except Exception:
                    max_size = [0.3, 0.3, 0.3]
                
                if max(max_size) > 0.1:
                    obstacles.append({
                        "id": i,
                        "position": object_pos,
                        "orientation": object_orn,
                        "size": max_size
                    })
        except Exception:
            continue
    
    print(f"Identified {len(obstacles)} obstacles for drone to avoid")
    return obstacles

drone_initial_position = [10, -2, 2]
drone_orientation = p.getQuaternionFromEuler([0, 0, 0])
drone_id, rotors, tank = create_drone(drone_initial_position, drone_orientation)

drone_controller = DroneController(drone_id, drone_initial_position)

fire_source_pos = fire_sources[0].position
print(f"Main fire source at: {fire_source_pos}")
drone_controller.hover_height = 1.8

obstacles = identify_obstacles_in_room()
print(f"Identified {len(obstacles)} obstacles for drone to avoid")

def fixed_update_rate_simulation():
    fixed_time_step = 1.0/240
    max_substeps = 4
    target_fps = 30
    
    camera_yaw = 90
    camera_pitch = -30
    camera_distance = 5
    camera_target = [2, -1, 1]
    
    def update_camera():
        camera_position = [
            camera_target[0] + camera_distance * math.cos(math.radians(camera_yaw)) * math.cos(math.radians(camera_pitch)),
            camera_target[1] + camera_distance * math.sin(math.radians(camera_yaw)) * math.cos(math.radians(camera_pitch)),
            camera_target[2] + camera_distance * math.sin(math.radians(camera_pitch))
        ]
        p.resetDebugVisualizerCamera(camera_distance, camera_yaw, camera_pitch, camera_target)
    
    last_time = time.time()
    
    fire_marker = p.addUserDebugLine([0, 0, 0], [0, 0, 0], [1, 0, 0], 5.0)
    
    while True:
        current_time = time.time()
        pos, orient = p.getBasePositionAndOrientation(drone_id)
    
    # Convert the current orientation quaternion to Euler angles (roll, pitch, yaw)
        roll, pitch, yaw = p.getEulerFromQuaternion(orient)
    
    # Construct a new quaternion that preserves only yaw (vertical attitude)
        new_orientation = p.getQuaternionFromEuler([0, 0, yaw])
    
    # Reset the drone's orientation to the new vertical one without disturbing the position
        p.resetBasePositionAndOrientation(drone_id, pos, new_orientation)
    
    # Optionally include a sleep/delay here to manage simulation speed
        elapsed = current_time - last_time
        
        if elapsed >= 1.0/target_fps:
            
            
            fire_positions = [fire.position for fire in fire_sources if fire.max_particles > 0]
            
            if fire_positions:
                p.addUserDebugLine(
                    [fire_positions[0][0], fire_positions[0][1], 0],
                    [fire_positions[0][0], fire_positions[0][1], 3],
                    [1, 0, 0], 2.0, replaceItemUniqueId=fire_marker
                )
            
            drone_controller.update(fire_positions, obstacles)
            
            for fire in fire_sources:
                if fire.max_particles > 0:
                    fire.update()
            
            for particle_id, creation_time in drone_controller.extinguishing_particles:
                try:
                    particle_pos, _ = p.getBasePositionAndOrientation(particle_id)
                    
                    for fire_source in fire_sources:
                        if fire_source.max_particles > 0:
                            fire_pos = fire_source.position
                            distance = math.sqrt(sum((particle_pos[i] - fire_pos[i])**2 for i in range(3)))
                            
                            if distance < 2:
                                fire_source.max_particles -= 20
                                print(f"Fire at {fire_source.position}: {fire_source.max_particles} particles remaining")
                                
                                if fire_source.max_particles <= 0:
                                    for fire_particle in list(fire_source.particles):
                                        if isinstance(fire_particle, tuple) and len(fire_particle) > 0:
                                            p.removeBody(fire_particle[0])
                                    fire_source.particles.clear()
                                    print(f"Fire at {fire_source.position} extinguished!")
                except:
                    pass
            
            for _ in range(min(int(elapsed / fixed_time_step), max_substeps)):
                p.stepSimulation()
            
            last_time = current_time
            time.sleep(0.001)

fixed_update_rate_simulation()
