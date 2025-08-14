import moderngl
import numpy as np
from pyrr import Matrix44
import math

# ----------------------
# Utility: Generate Normals
# ----------------------
def generate_normals(vertices, indices):
    normals = np.zeros((len(vertices)//6, 3), dtype='f4')
    verts = vertices.reshape(-1, 6)[:, :3]  # only xyz positions

    for i in range(0, len(indices), 3):
        i1, i2, i3 = indices[i:i+3]
        v1, v2, v3 = verts[i1], verts[i2], verts[i3]
        edge1, edge2 = v2 - v1, v3 - v1
        normal = np.cross(edge1, edge2)
        normal /= np.linalg.norm(normal) if np.linalg.norm(normal) != 0 else 1
        normals[i1] += normal
        normals[i2] += normal
        normals[i3] += normal

    # Normalize all normals
    normals = np.array([n/np.linalg.norm(n) if np.linalg.norm(n) != 0 else n for n in normals], dtype='f4')

    # Add normals back into vertex array
    verts_with_normals = []
    for i, (x, y, z, r, g, b) in enumerate(vertices.reshape(-1, 6)):
        nx, ny, nz = normals[i]
        verts_with_normals.extend([x, y, z, r, g, b, nx, ny, nz])

    return np.array(verts_with_normals, dtype='f4')

# ----------------------
# Scene & Object System
# ----------------------
class Object3D:
    def __init__(self, vao):
        self.vao = vao
        self.position = np.array([0.0, 0.0, 0.0])
        self.rotation = np.array([0.0, 0.0, 0.0])
        self.scale = np.array([1.0, 1.0, 1.0])

    def get_model_matrix(self):
        return Matrix44.from_translation(self.position) @ \
               Matrix44.from_eulers(self.rotation) @ \
               Matrix44.from_scale(self.scale)

class Scene:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

# ----------------------
# Base Geometry
# ----------------------
class Geometry:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices

    def create_vao(self, ctx, prog):
        vbo = ctx.buffer(self.vertices.tobytes())
        ibo = ctx.buffer(self.indices.tobytes())
        vao = ctx.vertex_array(prog, [(vbo, '3f 3f 3f', 'in_vert', 'in_color', 'in_normal')], ibo)
        return vao

# ----------------------
# BoxGeometry
# ----------------------
class BoxGeometry(Geometry):
    def __init__(self):
        vertices = np.array([
            # pos         color
            -1, -1, -1, 1, 0, 0,
             1, -1, -1, 0, 1, 0,
             1,  1, -1, 0, 0, 1,
            -1,  1, -1, 1, 1, 0,
            -1, -1,  1, 1, 0, 1,
             1, -1,  1, 0, 1, 1,
             1,  1,  1, 1, 1, 1,
            -1,  1,  1, 0, 0, 0
        ], dtype='f4')

        indices = np.array([
            0, 1, 2, 2, 3, 0,
            4, 5, 6, 6, 7, 4,
            0, 1, 5, 5, 4, 0,
            2, 3, 7, 7, 6, 2,
            0, 3, 7, 7, 4, 0,
            1, 2, 6, 6, 5, 1
        ], dtype='i4')

        vertices = generate_normals(vertices, indices)
        super().__init__(vertices, indices)

# ----------------------
# SphereGeometry
# ----------------------
class SphereGeometry(Geometry):
    def __init__(self, segments=16, rings=16):
        vertices = []
        indices = []

        for y in range(rings + 1):
            for x in range(segments + 1):
                x_segment = x / segments
                y_segment = y / rings
                x_pos = math.cos(x_segment * 2 * math.pi) * math.sin(y_segment * math.pi)
                y_pos = math.cos(y_segment * math.pi)
                z_pos = math.sin(x_segment * 2 * math.pi) * math.sin(y_segment * math.pi)

                vertices.extend([x_pos, y_pos, z_pos, 1, 1, 1])  # white color for now

        for y in range(rings):
            for x in range(segments):
                i1 = y * (segments + 1) + x
                i2 = i1 + segments + 1
                indices.extend([i1, i2, i1 + 1, i1 + 1, i2, i2 + 1])

        vertices = np.array(vertices, dtype='f4')
        indices = np.array(indices, dtype='i4')
        vertices = generate_normals(vertices, indices)
        super().__init__(vertices, indices)

# ----------------------
# PlaneGeometry
# ----------------------
class PlaneGeometry(Geometry):
    def __init__(self, width=1, height=1):
        vertices = np.array([
            -width/2, -height/2, 0, 1, 0, 0,
             width/2, -height/2, 0, 0, 1, 0,
             width/2,  height/2, 0, 0, 0, 1,
            -width/2,  height/2, 0, 1, 1, 0
        ], dtype='f4')

        indices = np.array([0, 1, 2, 2, 3, 0], dtype='i4')
        vertices = generate_normals(vertices, indices)
        super().__init__(vertices, indices)
