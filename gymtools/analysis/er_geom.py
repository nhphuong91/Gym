# Used in the catalogue's revision 8 check of vertical-pull grips (T12, 2026-10-06): how far a long humerus
# turns the shoulder out at the bottom of a front pulldown, for two grip widths, two humerus lengths and four elbow planes.
# Run: python3 er_geom.py (needs numpy). Lengths in cm; the output is rough geometry, not a measurement.
# Rough geometry: shoulder ER (forearm-pointer convention) at the bottom of a front pulldown.
# Coordinates: x lateral, y cranial, z anterior; shoulder joint centre at origin.
import numpy as np
def er(hum, fore, hand, elbow_plane_deg):
    # elbow on the circle where |E|=hum and |E-H|=fore; pick the point whose azimuth (angle of E
    # projected on x-z plane, from +x toward +z) is closest to elbow_plane_deg (0 = frontal plane, + = forward)
    H=np.array(hand,float)
    best=None
    for az in np.radians(np.linspace(-60,90,1501)):
        for el in np.radians(np.linspace(-89,0,891)):   # elevation below horizontal
            E=hum*np.array([np.cos(el)*np.cos(az), np.sin(el), np.cos(el)*np.sin(az)])
            d=abs(np.linalg.norm(E-H)-fore)
            if d<0.3:
                score=abs(np.degrees(az)-elbow_plane_deg)
                if best is None or score<best[0]: best=(score,E)
    if best is None: return None
    E=best[1]; h=E/np.linalg.norm(E); f=(H-E)/np.linalg.norm(H-E)
    elev=np.degrees(np.arccos(-h[1]))   # humeral elevation from the side
    # rotation reference: 0 = forearm in the plane of elevation pointing 'forward' of that plane,
    # computed as the forearm-pointer angle about the humerus from the anterior-most direction
    A=np.array([0,0,1.0]); A=A-(A@h)*h; A/=np.linalg.norm(A)
    P=np.cross(h,A)                     # candidate outward direction
    if P[1]<0: P=-P                      # ER moves the forearm cranially when the arm is abducted
    fp=f-(f@h)*h
    phi=np.degrees(np.arctan2(fp@P, fp@A))
    flex=np.degrees(np.arccos(np.clip(f@h,-1,1)))
    return round(elev), round(np.degrees(np.arctan2(E[2],E[0]))), round(flex), round(phi)
for half in (20,27):
    for hum in (33,36):
        for plane in (-15,0,20,35):
            r=er(hum,30,(half,-3,8),plane)
            print(f"grip half-width {half} cm, humerus {hum} cm, elbow plane {plane:+}°: elevation, plane, elbow flexion, ER =", r)
