# stdlib imports
from abc import ABC, abstractmethod

# local imports
from openquake.hazardlib.imt import PGA, PGV, SA,IA,PGD,IH


class GMICE(ABC):
    """
    Base class called to implement ground motion intensity conversion equations (GMICE).

    Inherited by AK07, Wald99, WGRW12.
    """
    def __init__(self):
        self._pga = PGA()
        self._pgv = PGV()
        self._pgd = PGD()
        self._ia = IA()
        self._ih = IH()
        self._sa03 = SA(0.3)
        self._sa10 = SA(1.0)
        self._sa30 = SA(3.0)

    @staticmethod
    def getDistanceType():
        return 'rrup'

    def getMinMax(self):
        """
        Get the minimum and maximum MMI values produced by this GMICE.

        Returns:
            Tuple of min and max values of GMICE.
        """
        return self.min_max

    def getName(self):
        """
        Get the name of this GMICE.

        Returns:
            String containing name of GMICE.
        """
        return self.name

    def getScale(self):
        """
        Get the name of the PostScript file containing this GMICE's
        scale.

        Returns:
            Name of GMICE scale file.
        """
        return self.scale

    @abstractmethod
    def getMIfromGM(cls, amps, imt, dists=None, mag=None):
        """
        Function to compute macroseismic intensity from ground-motion
        intensity. Supported ground-motion IMTs are PGA, PGV and PSA
        at 0.3, 1.0, and 2.0 sec periods.

        Args:
            amps (ndarray):
                Ground motion amplitude; natural log units; g for PGA and
                PSA, cm/s for PGV.
            imt (OpenQuake IMT):
                Type the input amps (must be one of PGA, PGV, or SA).
                Supported SA periods are 0.3, 1.0, and 3.0 sec.
                `[link] <http://docs.openquake.org/oq-hazardlib/master/imt.html>`
            dists (ndarray):
                Numpy array of distances from rupture (km).
            mag (float):
                Earthquake magnitude.

        Returns:
            ndarray of Modified Mercalli Intensity and ndarray of
            dMMI / dln(amp) (i.e., the slope of the relationship at the
            point in question).
        """
        pass

    @abstractmethod
    def getGMfromMI(cls, mmi, imt, dists=None, mag=None):
        """
        Function to tcompute ground-motion intensity from macroseismic
        intensity. Supported IMTs are PGA, PGV and PSA for 0.3, 1.0, and
        3.0 sec periods.

        Args:
            mmi (ndarray):
                Macroseismic intensity.
            imt (OpenQuake IMT):
                IMT of the requested ground-motions intensities (must be
                one of PGA, PGV, or SA).
                `[link] <http://docs.openquake.org/oq-hazardlib/master/imt.html>`
            dists (ndarray):
                Rupture distances (km) to the corresponding MMIs.
            mag (float):
                Earthquake magnitude.

        Returns:
            Ndarray of ground motion intensity in natural log of g for PGA
            and PSA, and natural log cm/s for PGV; ndarray of dln(amp) / dMMI
            (i.e., the slope of the relationship at the point in question).
        """
        pass

    @abstractmethod
    def getGM2MIsd(cls):
        """
        Return a dictionary of standard deviations for the ground-motion
        to MMI conversion. The keys are the ground motion types.

        Returns:
            Dictionary of GM to MI sigmas (in MMI units).
        """
        pass

    @abstractmethod
    def getMI2GMsd(cls):
        """
        Return a dictionary of standard deviations for the MMI
        to ground-motion conversion. The keys are the ground motion
        types.

        Returns:
            Dictionary of MI to GM sigmas (ln(PGM) units).
        """
        pass

    @abstractmethod
    def _getConsts(cls, imt):
        """
        Helper function to get the constants.
        """
        pass
