import pyglet
import ctypes
from pyglet.gl import *
from gletools import ShaderProgram, FragmentShader, VertexShader
import itertools


class Knot_Display(pyglet.window.Window):

    def __init__(self, **kwargs):
        super(Knot_Display, self).__init__(**kwargs)

        self.program = ShaderProgram(
	    FragmentShader.open('test.frag'),
            VertexShader.open('test.vert')
        )
	
	self.numpoints = 100000
	self.point_size = (4*4 + 4)
	
	# create_buffer(size, target=34962, usage=35048, vbo=True)
	self.vbos = []
	for i in range(2):
	    vbo = pyglet.graphics.vertexbuffer.create_buffer( self.numpoints*self.point_size, GL_ARRAY_BUFFER, GL_STREAM_DRAW )
	    self.vbos.append(vbo)
	print len(self.vbos)
	
    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-1, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        return pyglet.event.EVENT_HANDLED

    def on_mouse_press(self, x, y, button, modifiers):
        # self.set_exclusive_mouse()
        return

    def on_mouse_release(self, x, y, button, modifiers):
        # self.set_exclusive_mouse(exclusive=False)
        return

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # rotate on left-drag
        return

    def on_draw(self): 
	# Specify the source buffer
        self.vbos[0].target = GL_ARRAY_BUFFER
	self.vbos[0].bind()
	glEnableVertexAttribArray(0)
	glEnableVertexAttribArray(1)
	glEnableVertexAttribArray(2)
	glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, self.point_size, 0)
	glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.point_size, 8)
	glVertexAttribPointer(2, 1, GL_UNSIGNED_INT, GL_FALSE, self.point_size, 16)

	# Specify the target buffer
	self.vbos[1].target = GL_TRANSFORM_FEEDBACK_BUFFER
	self.vbos[1].bind()
	
	# Specify transform feedback output
	LP_c_char = ctypes.POINTER(ctypes.c_char)
	LP_LP_c_char = ctypes.POINTER(LP_c_char)
	ptrs = [ ctypes.cast(ctypes.byref(ctypes.c_char_p(str)), LP_c_char) for str in ['oPosition', 'oVelocity', 'oSeed'] ]
	c_array = ctypes.cast(ctypes.byref(LP_c_char(ptrs)), LP_LP_c_char)
	glTransformFeedbackVaryings(self.program.id, len(ptrs), c_array, GL_INTERLEAVED_ATTRIBS)
	self.program.link()
	
	# Perform simulation step
	with self.program:
	    glEnable(GL_RASTERIZER_DISCARD);
	    glBeginTransformFeedback(GL_POINTS)
	    glDrawArrays(GL_POINTS, 0, self.numpoints)
	    glEndTransformFeedback()
	    glDisable(GL_RASTERIZER_DISCARD);

	with self.program:
	    # Draw points
            glPointSize(1.8)
            glBegin(GL_POINTS)
            glDrawArrays(GL_POINTS, 0, self.numpoints)
	    glEnd()

	self.vbos[0].unbind()
	#self.vbos[1].unbind()

	# Swap A and B
	# self.vbos = vbos[::-1]


def main():

    config = pyglet.gl.Config(sample_buffers=1, samples=4, double_buffer=True, depth_size=24)
    window = Knot_Display(caption='Knotviz in the house', resizable=True, vsync=True, config=config)

    pyglet.app.run()

if __name__ == '__main__': main()
