# sphere_chunk_demo.py
import glfw
import moderngl
import numpy as np
from pyrr import Matrix44
import time
import math

# ---------- Helpers: build a sphere geometry (pos + normal only) ----------
def make_sphere(radius=0.5, segments=24, rings=16):
    positions = []
    normals = []
    indices = []

    for y in range(rings + 1):
        v = y / rings
        phi = v * math.pi
        for x in range(segments + 1):
            u = x / segments
            theta = u * 2.0 * math.pi
            px = radius * math.sin(phi) * math.cos(theta)
            py = radius * math.cos(phi)
            pz = radius * math.sin(phi) * math.sin(theta)
            positions.extend([px, py, pz])
            nx, ny, nz = px / radius, py / radius, pz / radius
            normals.extend([nx, ny, nz])

    for y in range(rings):
        for x in range(segments):
            i0 = y * (segments + 1) + x
            i1 = i0 + 1
            i2 = i0 + (segments + 1)
            i3 = i2 + 1
            indices += [i0, i2, i1, i1, i2, i3]

    # interleave: pos(3), normal(3)
    verts = []
    for i in range(len(positions)//3):
        verts.extend(positions[3*i:3*i+3])
        verts.extend(normals[3*i:3*i+3])

    vertices = np.array(verts, dtype='f4')
    indices = np.array(indices, dtype='i4')
    return vertices, indices

# ---------- Shaders (instancing) ----------
vertex_shader = '''
#version 330
in vec3 in_pos;
in vec3 in_normal;

// per-instance attributes
in vec3 instance_offset;
in vec3 instance_color;

uniform mat4 mvp;
out vec3 v_normal;
out vec3 v_color;

void main() {
    vec4 world_pos = vec4(in_pos + instance_offset, 1.0);
    gl_Position = mvp * world_pos;
    v_normal = in_normal;
    v_color = instance_color;
}
'''

fragment_shader = '''
#version 330
in vec3 v_normal;
in vec3 v_color;
out vec4 fragColor;

void main() {
    vec3 n = normalize(v_normal);
    float light = max(dot(n, normalize(vec3(0.5, 1.0, 0.3))), 0.0);
    vec3 base = v_color;
    fragColor = vec4(base * (0.35 + 0.65 * light), 1.0);
}
'''

# ---------- Chunk using instanced rendering ----------
class Chunk:
    """
    Holds sphere centers for a chunk and builds an per-instance buffer.
    """
    def __init__(self, ctx, program, sphere_vertices, sphere_indices):
        self.ctx = ctx
        self.program = program

        # base geometry buffers (shared across chunks ideally)
        self.vbo = ctx.buffer(sphere_vertices.tobytes())
        self.ibo = ctx.buffer(sphere_indices.tobytes())
        self.index_count = len(sphere_indices)

        self.instance_buf = None
        self.instance_count = 0
        self.vao = None

    def build_instances(self, centers, colors=None):
        centers = np.array(centers, dtype='f4')
        n = len(centers)
        if colors is None:
            colors = np.ones((n, 3), dtype='f4') * 0.8
        else:
            colors = np.array(colors, dtype='f4')

        # interleave instance data: offset(x,y,z), color(r,g,b)
        inst_data = np.empty((n, 6), dtype='f4')
        inst_data[:, 0:3] = centers
        inst_data[:, 3:6] = colors
        inst_bytes = inst_data.tobytes()

        if self.instance_buf is None:
            self.instance_buf = self.ctx.buffer(inst_bytes)
        else:
            self.instance_buf.orphan(size=len(inst_bytes))
            self.instance_buf.write(inst_bytes)

        self.instance_count = n

        # IMPORTANT: buffer attribute formats must match shader inputs exactly.
        # Here the vertex VBO has '3f 3f' => in_pos, in_normal
        # The instance buffer is '3f 3f/i' => instance_offset, instance_color (per-instance)
        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (self.vbo, '3f 3f', 'in_pos', 'in_normal'),
                (self.instance_buf, '3f 3f/i', 'instance_offset', 'instance_color'),
            ],
            self.ibo
        )

    def render(self):
        if self.vao is None or self.instance_count == 0:
            return
        self.vao.render(instances=self.instance_count)

# ---------- Chunk grid generator ----------
def generate_chunk_grid(chunk_size_x=8, chunk_size_z=8, spacing=1.0, height_fn=None):
    centers = []
    colors = []
    hx = chunk_size_x
    hz = chunk_size_z
    for iz in range(hz):
        for ix in range(hx):
            x = (ix - hx/2) * spacing
            z = (iz - hz/2) * spacing
            y = height_fn(x, z) if height_fn else 0.0
            centers.append((x, y, z))
            c = np.clip([(y+2.0)/4.0, 0.6, 1.0 - (y+2.0)/4.0], 0.0, 1.0)
            colors.append(tuple(c))
    return centers, colors

def hill_height(x, z):
    return math.sin(0.4 * x) * math.cos(0.4 * z) * 0.8

# ---------- Main app ----------
def main():
    if not glfw.init():
        raise RuntimeError("glfw.init() failed")
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    win = glfw.create_window(1000, 700, "Spherecraft - Chunk Instancing Demo", None, None)
    glfw.make_context_current(win)

    ctx = moderngl.create_context()
    ctx.enable(moderngl.DEPTH_TEST)

    prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    # create base sphere once (pos + normal)
    verts, inds = make_sphere(radius=0.45, segments=32, rings=18)

    # make a chunk
    chunk = Chunk(ctx, prog, verts, inds)

    centers, colors = generate_chunk_grid(chunk_size_x=20, chunk_size_z=20, spacing=0.95, height_fn=hill_height)
    chunk.build_instances(centers, colors)

    proj = Matrix44.perspective_projection(45.0, 1000/700, 0.1, 100.0)
    view = Matrix44.look_at((8.0, 6.0, 12.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))

    start = time.time()
    while not glfw.window_should_close(win):
        glfw.poll_events()
        ctx.clear(0.08, 0.08, 0.12)

        t = time.time() - start
        cam_pos = (math.sin(t*0.2)*8.0, 4.0, math.cos(t*0.2)*8.0)
        view = Matrix44.look_at(cam_pos, (0, 0, 0), (0, 1, 0))
        mvp = proj * view * Matrix44.identity()

        prog['mvp'].write(mvp.astype('f4').tobytes())

        chunk.render()

        glfw.swap_buffers(win)

    glfw.terminate()

if __name__ == '__main__':
    main()
