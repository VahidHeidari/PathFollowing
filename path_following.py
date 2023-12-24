import Tkinter
import os
import random

import PIL
import PIL.ImageDraw
import PIL.ImageTk

import vector
import vehicle



NUM_VEHICLES = 10

#IS_DRAW_HEAD = True
IS_DRAW_HEAD = False

#IS_SAVE_FRAMES = True
IS_SAVE_FRAMES = False

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
        (320, 120),     # 3
        (320, 200),     # 4
        (300, 240),     # 5
        ( 30, 240),     # 6
        ( 20, 215),     # 7
        ( 30, 190),     # 8
        (170, 190),     # 9
        (200, 160),     # 10
    ], [
        ( 80,  60),     # 0
        (300,  60),     # 1
        (320, 100),     # 2
        (320, 200),     # 3
        (300, 240),     # 4
        ( 30, 240),     # 5
        ( 20, 210),     # 6
        ( 30, 180),     # 7
        (170, 180),     # 8
        (190, 155),     # 9
        (170, 130),     # 10
        ( 80, 130),     # 11
        ( 60, 100),     # 12
    ], [
        (220,  80),     # 0
        (260,  60),     # 1
        (300,  80),     # 2
        (320, 120),     # 3
        (320, 200),     # 4
        (300, 240),     # 5
        ( 30, 240),     # 6
        ( 20, 215),     # 7
        ( 30, 190),     # 8
        ( 80, 190),     # 9
        (100, 170),     # 10
        (110, 140),     # 11
        (130, 130),     # 12
        (150, 140),     # 13
        (180, 140),     # 14
        (200, 130),     # 15
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
    drw.polygon(pts, fill=vehcl.clr, outline='yellow')

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
    # Draw vehicle.
    DrawVehicle(drw, vehcl)
    DrawVectors(drw, vehcl, path_segs)

    # Update scene.
    vehcl.FollowPath(path_segs)
    vehcl.Update(1.0 / 30.0)
    TrimCoord(vehcl)


def UpdateCanvas(canvas):
    # Save/Present scene.
    if IS_SAVE_FRAMES:
        global frame_num
        frame_num += 1
        img.save(os.path.join('frames', 'frame{:04d}.png'.format(frame_num)))

    canvas.delete('all')
    img_tk = PIL.ImageTk.PhotoImage(img)
    canvas.create_image(WIDTH // 2, HEIGHT // 2, image=img_tk)
    canvas.update()
    canvas.after(int(1.0 / 30.0 * 100))


def AppendMirrors(paths):
    NUM_PATHS = len(paths)
    VPT = (WIDTH, 0)
    HPT = (0, HEIGHT)
    HVPT = (WIDTH, HEIGHT)
    for i in range(NUM_PATHS):
        vmirror = []
        hmirror = []
        hvmirror = []
        for j in range(len(paths[i])):
            vneg_pt = (-paths[i][j][0], paths[i][j][1])
            vmirror.append(vector.Add(VPT, vneg_pt))

            hneg_pt = (paths[i][j][0], -paths[i][j][1])
            hmirror.append(vector.Add(HPT, hneg_pt))

            hvneg_pt = vector.Neg(paths[i][j])
            hvmirror.append(vector.Add(HVPT, hvneg_pt))
        paths.append(vmirror)
        paths.append(hmirror)
        paths.append(hvmirror)



if __name__ == '__main__':
    # Create output directory.
    if IS_SAVE_FRAMES and not os.path.isdir('frames'):
        os.makedirs('frames')

    # Initialize entities.
    AppendMirrors(PATHS)
    path_segs = PATHS[int(random.uniform(0, len(PATHS)))]

    vehcls = [ vehicle.Vehicle() for i in range(NUM_VEHICLES) ]
    if vehicle.IS_INIT_RANDOM:
        for v in vehcls:
            v.FindNearestStartSegment(path_segs)

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

