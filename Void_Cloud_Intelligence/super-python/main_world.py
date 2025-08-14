# main_world.py
import glfw
import moderngl
from pyrr import Matrix44
import math
import time

from engine import Scene, Object3D, SphereGeometry

# ------------------- Init -------------------
if not glfw.init():
    raise RuntimeError("glfw.init() failed")

win = glfw.create_window(800, 600, "Engine Sphere Test", None, None)
glfw.make_context_current(win)

ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST)

# ------------------- Shaders -------------------
vertex_shader = '''
#version 330
in vec3 in_vert;
in vec3 in_color;
in vec3 in_normal;

uniform mat4 mvp;

out vec3 v_color;
out vec3 v_normal;

void main() {
    gl_Position = mvp * vec4(in_vert, 1.0);
    v_color = in_color;
    v_normal = in_normal;
}
'''

fragment_shader = '''
#version 330
in vec3 v_color;
in vec3 v_normal;

out vec4 fragColor;

void main() {
    vec3 n = normalize(v_normal);
    float light = max(dot(n, normalize(vec3(0.5, 1.0, 0.3))), 0.0);
    fragColor = vec4(v_color * (0.35 + 0.65 * light), 1.0);
}
'''

prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

# ------------------- Scene Setup -------------------
scene = Scene()

sphere_geo = SphereGeometry(segments=32, rings=18)
sphere_obj = Object3D(sphere_geo.create_vao(ctx, prog))
scene.add(sphere_obj)
scene.add(sphere_obj)

# Projection matrix
proj = Matrix44.perspective_projection(45.0, 800/600, 0.1, 100.0)

start = time.time()

# ------------------- Main Loop -------------------
while not glfw.window_should_close(win):
    glfw.poll_events()
    ctx.clear(0.1, 0.1, 0.15)

    t = time.time() - start
    cam_pos = (math.sin(t * 0.5) * 3.0, 1.5, math.cos(t * 0.5) * 3.0)
    view = Matrix44.look_at(cam_pos, (0, 0, 0), (0, 1, 0))

    for obj in scene.objects:
        model = obj.get_model_matrix()
        mvp = proj * view * model
        prog['mvp'].write(mvp.astype('f4').tobytes())
        obj.vao.render()

    glfw.swap_buffers(win)

glfw.terminate()
