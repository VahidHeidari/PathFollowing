import Tkinter
import random

import PIL
import PIL.ImageDraw
import PIL.ImageTk

import vector
import vehicle



NUM_VEHICLES = 10

#IS_DRAW_HEAD = True
IS_DRAW_HEAD = False


EL_WIDTH        = 12
EL_WIDTH_HEIGHT = (EL_WIDTH, EL_WIDTH)

TEXT_X_OFF = 2
TEXT_Y_OFF = 1

WIDTH  = 340
HEIGHT = 280

HEAD_RAD   = 6
HEAD_OFF   = (HEAD_RAD, HEAD_RAD)
HEAD_OFF_2 = (HEAD_RAD / 2.0, HEAD_RAD / 2.0)


PATHS = [
    [
        (120,  60),     # 0
        (220,  60),     # 1
        (260,  80),     # 2
        (280, 140),     # 3
        (260, 200),     # 4
        (220, 220),     # 5
        (120, 220),     # 6
        ( 80, 200),     # 7
        ( 60, 140),     # 8
        ( 80,  80),     # 9
    ], [
        (220,  80),     # 0
        (260,  60),     # 1
        (300,  80),     # 2
        (320, 140),     # 3
        (320, 200),     # 4
        (300, 240),     # 5
        ( 60, 240),     # 6
        ( 30, 233),     # 7
        ( 20, 210),     # 8
        ( 30, 187),     # 9
        (170, 187),     # 10
        (200, 160),     # 11
    ],
]



def ClearBackBuffer(drw):
    drw.rectangle(((0, 0), drw.im.size), fill='black')


def DrawPath(drw, path_segments, clr='red'):
    for i in range(len(path_segments) - 1):
        drw.line(( path_segments[i], path_segments[i + 1] ), clr)
    drw.line(( path_segments[0], path_segments[-1] ), clr)

    for i in range(len(path_segments)):
        pt = path_segments[i]
        st = (pt[0] - EL_WIDTH // 2, pt[1] - EL_WIDTH // 2)
        ed = vector.Add(st, EL_WIDTH_HEIGHT)
        drw.ellipse((st, ed), fill='blue', outline=clr)
        drw.text((pt[0] - TEXT_X_OFF, st[1] + TEXT_Y_OFF), str(i), 'white')


def DrawVehicle(drw, vehcl):
    vel_nrm = vector.Normalize(vehcl.velocity)
    vel_neg = vector.Mult(15, vector.Neg(vel_nrm))
    vel_ngm = vector.Mult(20, vector.Neg(vel_nrm))
    orth = vector.Orth(vel_nrm)
    vel_ort = vector.Add(vector.Mult( 8, orth), vel_ngm)
    vel_orn = vector.Add(vector.Mult(-8, orth), vel_ngm)

    pts = (
        vehcl.xy,
        vector.Add(vehcl.xy, vel_ort),
        vector.Add(vehcl.xy, vel_neg),
        vector.Add(vehcl.xy, vel_orn)
    )
    drw.polygon(pts, fill='yellow', outline='red')

    if IS_DRAW_HEAD:
        cntr = vector.Add(vehcl.xy, vector.MultNorm(vehicle.FRONT, vehcl.velocity))
        top = vector.Sub(HEAD_OFF_2, cntr)
        end = vector.Add(top, HEAD_OFF)
        drw.line((vehcl.xy, cntr), 'yellow')
        drw.ellipse((top, end), fill='blue', outline='yellow')


def DrawVectors(drw, vehcl, path_segs):
    if not IS_DRAW_HEAD:
        return

    drw.line((vehcl.xy, path_segs[vehcl.idx]), 'yellow')
    drw.line((vehcl.xy, path_segs[(vehcl.idx + 1) % len(path_segs)]), 'cyan')


def TrimCoord(vehcl):
    if vehcl.xy[0] > WIDTH:
        vehcl.xy = (0, vehcl.xy[1])
    elif vehcl.xy[0] < 0:
        vehcl.xy = (WIDTH, vehcl.xy[1])
    if vehcl.xy[1] > HEIGHT:
        vehcl.xy = (vehcl.xy[0], 0)
    elif vehcl.xy[1] < 0:
        vehcl.xy = (vehcl.xy[0], HEIGHT)


frame_num = 0
def Update(vehcl, path_segs):
    global frame_num
    frame_num += 1

    # Draw vehicle.
    DrawVehicle(drw, vehcl)
    DrawVectors(drw, vehcl, path_segs)

    # Save/Present scene.
    #img.save('img{:04d}.png'.format(frame_num))

    # Update scene.
    vehcl.FollowPath(path_segs)
    vehcl.Update(1.0 / 30.0)
    TrimCoord(vehcl)


def UpdateCanvas(canvas):
    canvas.delete('all')
    img_tk = PIL.ImageTk.PhotoImage(img)
    canvas.create_image(WIDTH // 2, HEIGHT // 2, image=img_tk)
    canvas.update()
    canvas.after(int(1.0 / 30.0 * 100))



if __name__ == '__main__':
    # Initialize entities.
    path_segs = PATHS[int(random.uniform(0, len(PATHS)))]
    vehcls = [ vehicle.Vehicle() for i in range(NUM_VEHICLES) ]

    # Initialize back-buffer graphics.
    img = PIL.Image.new('RGB', (WIDTH, 280))
    drw = PIL.ImageDraw.ImageDraw(img)

    # Initialize window.
    root = Tkinter.Tk()
    root.title('Path Following Swarm')
    root.wm_geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, 1000, 100))

    canvas = Tkinter.Canvas(root, width=WIDTH, height=HEIGHT, backgroun='black')
    canvas.pack()

    while True:
        # Draw scene.
        ClearBackBuffer(drw)
        DrawPath(drw, path_segs)

        # Update scene.
        for v in vehcls:
            Update(v, path_segs)

        # Update window.
        try:
            UpdateCanvas(canvas)
        except Tkinter.TclError:        # TODO: Solve this exception at exit time!
            break

    root.mainloop()

