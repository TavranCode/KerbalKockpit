# Adapted from original work by github user marioferpa --> https://github.com/marioferpa/krpcscripts

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, proj3d
import numpy as np
from math import radians

from Utilities import si_val


# Plot setup

class Launchplot:
    def __init__(self):

        self.fig = plt.figure(figsize=(7, 7), facecolor="black")
        self.ax1 = self.fig.add_subplot(111)

        self.xar, self.yar = 0, 0
        self.xlim = 10
        self.ylim = 10

        # Gradient

        self.colormap = ListedColormap(np.loadtxt("kerbin_colormap.txt") / 255, N=256)  # made with http://jdherman.github.io/colormap/
        gradient = np.linspace(0, 10, 256)
        self.Z = np.zeros(shape=(256, 2))
        n = 255

        for item in gradient:
            self.Z[n] = np.array([item, item])
            n -= 1

        self.data_x = np.array(0)
        self.data_y = np.array(0)

        self.rts = False
        self.run_plot = False
        self.h_distance = 0

        self.start_coord = np.array((0,0))

        plt.xlim(-2, self.xlim)
        plt.ylim(0, self.ylim)

        self.ax1.imshow(self.Z, cmap=self.colormap, interpolation="bicubic", extent=[-2, self.xlim, 0, self.ylim])
        self.ax1.set_title("Launch Trajectory", fontsize=24, color="blue", fontweight="bold")
        self.ax1.set_xlabel("Horizontal distance (km)", fontsize=20, color="blue", fontweight="bold")
        self.ax1.set_ylabel("Altitude (km)", fontsize=20, color="blue", fontweight="bold")
        self.ax1.tick_params(color="blue", labelcolor="blue", labelsize=16)

        for spine in self.ax1.spines.values():
            spine.set_edgecolor("blue")

        self.fig.canvas.draw()

    def animate(self, vessel, position, altitude):

        # self.ax1.set_visible(False)

        if str(vessel.situation) == "VesselSituation.pre_launch" or str(vessel.situation) == "VesselSituation.landed":
            self.xar, self.yar = 0, 0
            self.start_coord = np.array(position)
            self.h_distance = 0
            self.xlim = 10
            self.ylim = 10
            self.rts = True

        elif self.rts:
            self.run_plot = True
            self.rts = False

        if self.run_plot:
            if altitude >= vessel.orbit.body.atmosphere_depth:
                self.run_plot = False

            self.h_distance = (np.linalg.norm(position - self.start_coord) * (2. * np.pi * vessel.orbit.body.equatorial_radius) / 360.) / 1000  # km
            self.xar = np.append(self.xar, self.h_distance)
            self.yar = np.append(self.yar, (altitude / 1000))

            # PLOT
            if self.xlim - self.h_distance < 5:
                self.xlim += 20
                self.ylim += 10

            if self.ylim - altitude / 1000 < 5:
                self.ylim += 10
                self.xlim += 10

            self.ax1.clear()  # can I move this to the start of the loop?
            self.ax1.plot(self.xar, self.yar, color="white", linewidth="5")

            plt.xlim(-2, self.xlim)
            plt.ylim(0, self.ylim)

            self.ax1.imshow(self.Z, cmap=self.colormap, interpolation="bicubic", extent=[-2, self.xlim, 0, self.ylim])
            self.ax1.set_title("Launch Trajectory", fontsize=24, color="blue", fontweight="bold")
            self.ax1.set_xlabel("Horizontal distance (km)", fontsize=20, color="blue", fontweight="bold")
            self.ax1.set_ylabel("Altitude (km)", fontsize=20, color="blue", fontweight="bold")
            self.ax1.tick_params(color="blue", labelcolor="blue", labelsize=16)

            for spine in self.ax1.spines.values():
                spine.set_edgecolor("blue")

            self.fig.canvas.draw()


class Orbitplot:
    def __init__(self):
        self.fig = plt.figure(figsize=(7, 9), facecolor="black")
        self.ax1 = self.fig.add_subplot(211, polar=True, axisbg="black")
        self.ax2 = self.fig.add_subplot(212, projection='3d', axisbg="black")

    def animate(self, vessel, periapsis, eccentricity, ecc_anom, inclination, LAN):
        # clear the plot and reset its properties
        self.ax1.clear()
        self.ax1.set_theta_offset(np.pi)
        self.ax1.axis("off")

        # plot 1
        #  plot the planet
        pr = vessel.orbit.body.equatorial_radius
        circle = plt.Circle((0, 0), pr, transform=self.ax1.transData._b, color="grey", alpha=1)
        self.ax1.add_artist(circle)
        self.ax1.annotate(vessel.orbit.body.name,
                          xy=(.5, .5),
                          xycoords='axes fraction',
                          horizontalalignment='center',
                          verticalalignment='center',
                          color="white",
                          size=24
                          )

        # calculate the orbit path
        q = periapsis + pr  # periapsis radius
        a = q / (1 - eccentricity)  # semi major axis
        ap = 2 * a - q  # aperiapsis radius

        theta = np.linspace(0, 2 * np.pi, 181)
        r = (a * (1 - eccentricity ** 2)) / (1 + eccentricity * np.cos(theta))

        # set the plot axis limits
        self.ax1.set_rlim(ap * 1.25)

        # plot the orbit
        self.ax1.plot(theta, r, color="blue", lw=3)

        # plot PE and AP
        self.ax1.plot([0], [q], "D", color="white", markersize=7)
        self.ax1.annotate("Pe = " + si_val(periapsis, 2) + "m",
                          xy=(0, q),  # theta, radius
                          xytext=(-5, -5),  # fraction, fraction
                          textcoords='offset points',
                          horizontalalignment='right',
                          verticalalignment='bottom',
                          color="white"
                          )

        self.ax1.plot([np.pi], [ap], "D", color="white", markersize=7)
        self.ax1.annotate("Ap = " + si_val(ap - pr, 2) + "m",
                          xy=(np.pi, ap),  # theta, radius
                          xytext=(5, 5),  # fraction, fraction
                          textcoords='offset points',
                          horizontalalignment='left',
                          verticalalignment='bottom',
                          color="white"
                          )

        # plot the current position
        true_anom = 2 * np.arctan2(np.sqrt(1 + eccentricity) * np.sin(ecc_anom / 2), np.sqrt(1 - eccentricity) * np.cos(ecc_anom / 2))
        r_vess = (a * (1 - eccentricity ** 2)) / (1 + eccentricity * np.cos(true_anom))

        self.ax1.plot([true_anom], [r_vess], ".", color="red", markersize=20)

        # plot 2
        self.ax2.clear()
        self.ax2.axis("off")

        # convert the orbit to cartesian coordinates and rotate for inclination and LAN
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = np.zeros(181)

        inclination = radians(inclination * np.pi / 180) #todo temp hack due to inclination bug

        x2 = x * np.cos(inclination) + z * np.sin(inclination)
        y2 = y
        z2 = -x * np.sin(inclination) + z * np.cos(inclination)

        x3 = x2 * np.cos(LAN) - y2 * np.sin(LAN)
        y3 = x2 * np.sin(LAN) + y2 * np.cos(LAN)
        z3 = z2

        #set up marker colours and sizes
        c = [[1,1,1,1]]  # this is our PE point
        s = [100]
        node_coord = [[x3[0],y3[0],z3[0]]]
        for i in range(1,181):
            if i == 90:  #this is our AP point
                c.append(c[0])
                s.append(s[0])
                node_coord.append([x3[90],y3[90],z3[90]])
            elif abs(z3[i]) < 1:   #These are our An and Dn points
                c.append([0,1,0, 1])
                s.append(100)
                node_coord.append([x3[i], y3[i], z3[i]])
            else:
                c.append([0,0,1,1])
                s.append(10)

        #plot the resulting orbit
        self.ax2.scatter(x3, y3, z3, c=c, s=s, marker = "D", edgecolors = "none")


        #Annotate the nodes
        if z3[0] < 0:  #90 degree point is the ascending node as periapsis is south of the equator
            node_labels = ["Pe", "An", "Ap", "Dn"]
        else:
            node_labels = ["Pe", "Dn", "Ap", "An"]

        for i in range(4):
            xl, yl, _ = proj3d.proj_transform(node_coord[i][0],node_coord[i][1], node_coord[i][2], self.ax2.get_proj())
            self.ax2.annotate(node_labels[i],
                              xy=(xl, yl),
                              xytext=(5, 5),  # fraction, fraction
                              textcoords='offset points',
                              horizontalalignment='left',
                              verticalalignment='bottom',
                              color="white"
                              )

        #plot the vessel position
        x = r_vess  * np.cos(true_anom)
        y = r_vess * np.sin(true_anom)
        z = 0

        x2 = x * np.cos(inclination) + z * np.sin(inclination)
        y2 = y
        z2 = -x * np.sin(inclination) + z * np.cos(inclination)

        x3 = x2 * np.cos(LAN) - y2 * np.sin(LAN)
        y3 = x2 * np.sin(LAN) + y2 * np.cos(LAN)
        z3 = z2

        self.ax2.plot([x3],[y3],[z3], ".", color="red", markersize=20)

        # add the planet
        t1, t2 = np.mgrid[0.0:np.pi:200j, 0.0:2.0 * np.pi:200j]
        xp = pr * np.sin(t1) * np.cos(t2)
        yp = pr * np.sin(t1) * np.sin(t2)
        zp = pr * np.cos(t1)
        self.ax2.plot_surface(xp, yp, zp, color="grey")

        # Adjustment of the axes, so that they all have the same span:
        for axis in 'xyz':
            getattr(self.ax2, 'set_{}lim'.format(axis))((-a, a))

        self.fig.canvas.draw()
