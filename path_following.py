import PIL
import PIL.ImageDraw

import vector
import vehicle



NUM_FRAMES = 30

EL_WIDTH = 12
EL_WIDTH_HEIGHT = (EL_WIDTH, EL_WIDTH)

TEXT_X_OFF = 2
TEXT_Y_OFF = 1



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


def DrawVehicle(vehcl):
    vel_nrm = vector.Normalize(vehcl.velocity)
    vel_neg = vector.Mult(15, vector.Neg(vel_nrm))
    vel_ort = vector.Add(vector.Mult( 8, vector.Orth(vel_nrm)), vector.Mult(20, vector.Neg(vel_nrm)))
    vel_orn = vector.Add(vector.Mult(-8, vector.Orth(vel_nrm)), vector.Mult(20, vector.Neg(vel_nrm)))

    pts = (
        vehcl.xy,
        vector.Add(vehcl.xy, vel_ort),
        vector.Add(vehcl.xy, vel_neg),
        vector.Add(vehcl.xy, vel_orn)
    )
    drw.polygon(pts, fill='yellow', outline='red')



if __name__ == '__main__':
    path_segs = [
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
    ]
    vehcl = vehicle.Vehicle()

    img = PIL.Image.new('RGB', (340, 280))
    drw = PIL.ImageDraw.ImageDraw(img)
    for i in range(NUM_FRAMES):
        ClearBackBuffer(drw)
        DrawPath(drw, path_segs)
        DrawVehicle(vehcl)
        img.save('img{:04d}.png'.format(i + 1))
        vehcl.Update(1.0 / 30.0)

