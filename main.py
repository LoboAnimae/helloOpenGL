import pygame
import numpy
import sys
import time

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

print('IN CASE YOU DIDN\'T KNOW: main.py [OPENGL_VERSION] [WIDTH] [HEIGHT]')

# Make it cute
print('Reading arguments', end='')
for _ in range(5):
  print('.', end='', flush=True)
  time.sleep(0.5)
print()

try:
  programVersion = sys.argv[1]
  programVersionSelection = 'USER_SELECTION'
except:
  programVersion = 450
  programVersionSelection = 'DEFAULT_SELECTION'

print('Set OpenGL version as %s (%s)'% (programVersion, programVersionSelection))

# Set the arguments
width, height = None, None
try: 
  width, height = sys.argv[2], sys.argv[3]
  screenDimSelection = 'USER_SELECTION'
except:
  if width is None: width = 800
  if height is None: height = 600
  screenDimSelection = 'DEFAULT_SELECTION'

print('Width has been set as %s and height has been set as %s (%s)' % (width, height, screenDimSelection))
try:
  pygame.init()
  screen = pygame.display.set_mode((int(width), int(height)), pygame.OPENGL | pygame.DOUBLEBUF)
except Exception as e:
  print(e)

vertex_shader = \
  '''
  #version %s
  layout (location = 0) in vec3 position;

  void main()
  {
    gl_Position = vec4(position.x, position.y, position.z, 1.0);
  }
  ''' % programVersion

fragment_shader = \
  '''
  #version %s
  layout(location = 0) out vec4 fragColor;
  
  void main()
  {
    fragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
  }
  ''' % programVersion

shader = compileProgram(
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(fragment_shader, GL_FRAGMENT_SHADER)
  )

vertex_data = numpy.array([
  -0.5, -0.5,  0.0,
   0.5,  -0.5,  0.0,
   0,  0.5,  0.0
], dtype=numpy.float32)

vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)
glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 3*4, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)


running = True
while running: 
  glClearColor(0.5, 1.0, 0.5, 1.0)

  glUseProgram(shader)
  glDrawArrays(GL_TRIANGLES, 0, 3)

  pygame.display.flip()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False