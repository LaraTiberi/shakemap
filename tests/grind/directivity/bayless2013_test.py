#!/usr/bin/env python 

#stdlib imports
import os.path
import sys
import time as time

# hack the path so that I can debug these functions if I need to
homedir = os.path.dirname(os.path.abspath(__file__))  # where is this script?
shakedir = os.path.abspath(os.path.join(homedir, '..','..','..'))
# put this at the front of the system path, ignoring any installed mapio stuff
sys.path.insert(0, shakedir)

import numpy as np

import openquake.hazardlib.geo as geo
from openquake.hazardlib.geo import point

from shakemap.grind.source import Source
import shakemap.grind.fault as fault
from shakemap.grind.directivity.bayless2013 import Bayless2013
from shakemap.utils.timeutils import ShakeDateTime
from shakemap.utils.vector import Vector
from shakemap.utils.ecef import ecef2latlon

def test_ss3():
    magnitude = 7.2
    dip = np.array([90])
    rake = 180.0
    width = np.array([15])
    fltx = np.array([0, 0])
    flty = np.array([0, 80])
    zp = np.array([0])
    epix = np.array([0])
    epiy = np.array([0.2 * flty[1]])

    # Convert to lat/lon
    proj = geo.utils.get_orthographic_projection(-122, -120, 39, 37)
    tlon, tlat = proj(fltx, flty, reverse=True)
    epilon, epilat = proj(epix, epiy, reverse=True)

    flt = fault.Fault.fromTrace(np.array([tlon[0]]), np.array([tlat[0]]),
                                np.array([tlon[1]]), np.array([tlat[1]]),
                                zp, width, dip, reference='ss3')

    event = {'lat': epilat[0],
             'lon': epilon[0],
             'depth': 10,
             'mag': magnitude,
             'id': 'ss3',
             'locstring': 'test',
             'type': 'SS',
             'timezone': 'UTC'}
    event['time'] = ShakeDateTime.utcfromtimestamp(int(time.time()))
    event['created'] = ShakeDateTime.utcfromtimestamp(int(time.time()))

    x = np.linspace(-60, 60, 21)
    y = np.linspace(-60, 138, 34)
    site_x, site_y = np.meshgrid(x, y)
    slon, slat = proj(site_x, site_y, reverse=True)
    deps = np.zeros_like(slon)
    source = Source(event, flt)
    source.setEventParam('rake', rake)

    test1 = Bayless2013(source, slat, slon, deps, T=1.0)

    # Test fd
    fd = test1.getFd()
    fd_test = np.array(
        [[0.00000000e+00, 0.00000000e+00, 2.14620746e-03,
          6.47899336e-03, 1.23119791e-02, 1.91676140e-02,
          2.64009788e-02, 3.32427846e-02, 3.88863288e-02,
          4.26104002e-02, 4.39120296e-02, 4.26104002e-02,
          3.88863288e-02, 3.32427846e-02, 2.64009788e-02,
          1.91676140e-02, 1.23119791e-02, 6.47899336e-03,
          2.14620746e-03, 0.00000000e+00, 0.00000000e+00],
         [0.00000000e+00, 8.57780996e-04, 3.99405791e-03,
          9.31948105e-03, 1.65406113e-02, 2.51316805e-02,
          3.43205435e-02, 4.31274592e-02, 5.04747209e-02,
          5.53634169e-02, 5.70796092e-02, 5.53634169e-02,
          5.04747209e-02, 4.31274592e-02, 3.43205435e-02,
          2.51316805e-02, 1.65406113e-02, 9.31948105e-03,
          3.99405791e-03, 8.57780996e-04, 0.00000000e+00],
            [-7.32594549e-04, 1.80425497e-04, 3.76908220e-03,
             1.00175179e-02, 1.86854835e-02, 2.92291145e-02,
             4.07487277e-02, 5.20057177e-02, 6.15509770e-02,
             6.79776087e-02, 7.02477931e-02, 6.79776087e-02,
             6.15509770e-02, 5.20057177e-02, 4.07487277e-02,
             2.92291145e-02, 1.86854835e-02, 1.00175179e-02,
             3.76908220e-03, 1.80425497e-04, -7.32594549e-04],
            [-3.29238561e-03, -2.60643191e-03, 1.16635260e-03,
             8.15185259e-03, 1.82290773e-02, 3.08983182e-02,
             4.51608038e-02, 5.94769126e-02, 7.18919113e-02,
             8.03888307e-02, 8.34165399e-02, 8.03888307e-02,
             7.18919113e-02, 5.94769126e-02, 4.51608038e-02,
             3.08983182e-02, 1.82290773e-02, 8.15185259e-03,
             1.16635260e-03, -2.60643191e-03, -3.29238561e-03],
            [-7.68543266e-03, -7.63179286e-03, -4.08866637e-03,
             3.27605236e-03, 1.45558215e-02, 2.94068040e-02,
             4.68176355e-02, 6.49397159e-02, 7.72066272e-02,
             8.50445368e-02, 8.77974692e-02, 8.50445368e-02,
             7.72066272e-02, 6.49397159e-02, 4.68176355e-02,
             2.94068040e-02, 1.45558215e-02, 3.27605236e-03,
             -4.08866637e-03, -7.63179286e-03, -7.68543266e-03],
            [-1.38078234e-02, -1.49011067e-02, -1.21731364e-02,
             -5.02168047e-03, 6.98177526e-03, 2.38268531e-02,
             4.30419205e-02, 6.00041964e-02, 7.44541603e-02,
             8.42939552e-02, 8.77989590e-02, 8.42939552e-02,
             7.44541603e-02, 6.00041964e-02, 4.30419205e-02,
             2.38268531e-02, 6.98177526e-03, -5.02168047e-03,
             -1.21731364e-02, -1.49011067e-02, -1.38078234e-02],
            [-2.13780396e-02, -2.42165379e-02, -2.30613142e-02,
             -1.70011475e-02, -5.15036128e-03, 1.25885635e-02,
             3.24536739e-02, 5.25619351e-02, 7.05100243e-02,
             8.31900906e-02, 8.78003567e-02, 8.31900906e-02,
             7.05100243e-02, 5.25619351e-02, 3.24536739e-02,
             1.25885635e-02, -5.15036128e-03, -1.70011475e-02,
             -2.30613142e-02, -2.42165379e-02, -2.13780396e-02],
            [-2.98882710e-02, -3.50862342e-02, -3.63793490e-02,
             -3.25716319e-02, -2.22546618e-02, -3.59274163e-03,
             1.83064517e-02, 4.20112440e-02, 6.46115966e-02,
             8.14746164e-02, 8.78016623e-02, 8.14746164e-02,
             6.46115966e-02, 4.20112440e-02, 1.83064517e-02,
             -3.59274163e-03, -2.22546618e-02, -3.25716319e-02,
             -3.63793490e-02, -3.50862342e-02, -2.98882710e-02],
            [-3.85810679e-02, -4.66488633e-02, -5.12430987e-02,
             -5.10089462e-02, -4.20856023e-02, -2.36905234e-02,
             -6.33876287e-04, 2.66765430e-02, 5.53289928e-02,
             7.86066125e-02, 8.78028757e-02, 7.86066125e-02,
             5.53289928e-02, 2.66765430e-02, -6.33876287e-04,
             -2.36905234e-02, -4.20856023e-02, -5.10089462e-02,
             -5.12430987e-02, -4.66488633e-02, -3.85810679e-02],
            [-4.64803335e-02, -5.76615888e-02, -6.61458422e-02,
             -7.06512643e-02, -6.38427394e-02, -4.77258398e-02,
             -2.55483969e-02, 4.05840724e-03, 3.98470070e-02,
             7.33053399e-02, 8.78039969e-02, 7.33053399e-02,
             3.98470070e-02, 4.05840724e-03, -2.55483969e-02,
             -4.77258398e-02, -6.38427394e-02, -7.06512643e-02,
             -6.61458422e-02, -5.76615888e-02, -4.64803335e-02],
            [-5.25038299e-02, -6.66129442e-02, -7.90147081e-02,
             -8.87629178e-02, -8.59653118e-02, -7.42828398e-02,
             -5.64316505e-02, -2.87083225e-02, 1.25945312e-02,
             6.19971667e-02, 8.78050260e-02, 6.19971667e-02,
             1.25945312e-02, -2.87083225e-02, -5.64316505e-02,
             -7.42828398e-02, -8.59653118e-02, -8.87629178e-02,
             -7.90147081e-02, -6.66129442e-02, -5.25038299e-02],
            [-5.69779111e-02, -7.36791817e-02, -8.97495345e-02,
             -1.04799583e-01, -1.07737239e-01, -1.02875880e-01,
             -9.46568471e-02, -7.95630162e-02, -4.96285112e-02,
             6.59954795e-03, 5.25569882e-02, 6.59954795e-03,
             -4.96285112e-02, -7.95630162e-02, -9.46568471e-02,
             -1.02875880e-01, -1.07737239e-01, -1.04799583e-01,
             -8.97495345e-02, -7.36791817e-02, -5.69779111e-02],
            [-5.90357675e-02, -7.69727119e-02, -9.48442826e-02,
             -1.12607620e-01, -1.18744885e-01, -1.18201834e-01,
             -1.17217017e-01, -1.15152899e-01, -1.09694433e-01,
             -8.82341332e-02, -1.61624035e-02, -8.82341332e-02,
             -1.09694433e-01, -1.15152899e-01, -1.17217017e-01,
             -1.18201834e-01, -1.18744885e-01, -1.12607620e-01,
             -9.48442826e-02, -7.69727119e-02, -5.90357675e-02],
            [-5.92189452e-02, -7.72680305e-02, -9.53051857e-02,
             -1.13322519e-01, -1.19770917e-01, -1.19670660e-01,
             -1.19486798e-01, -1.19092639e-01, -1.17989113e-01,
             -1.12555820e-01, -4.50009776e-02, -1.12555820e-01,
             -1.17989113e-01, -1.19092639e-01, -1.19486798e-01,
             -1.19670660e-01, -1.19770917e-01, -1.13322519e-01,
             -9.53051857e-02, -7.72680305e-02, -5.92189452e-02],
            [-5.79249958e-02, -7.51927112e-02, -9.20842554e-02,
             -1.08361430e-01, -1.12722790e-01, -1.09732675e-01,
             -1.04531672e-01, -9.44729544e-02, -7.23277773e-02,
             -2.05699911e-02, 3.58249631e-02, -2.05699911e-02,
             -7.23277773e-02, -9.44729544e-02, -1.04531672e-01,
             -1.09732675e-01, -1.12722790e-01, -1.08361430e-01,
             -9.20842554e-02, -7.51927112e-02, -5.79249958e-02],
            [-5.42527703e-02, -6.93641123e-02, -8.31684773e-02,
             -9.49114165e-02, -9.41989454e-02, -8.48645354e-02,
             -7.00894708e-02, -4.58286259e-02, -6.37563061e-03,
             4.68887998e-02, 7.77968419e-02, 4.68887998e-02,
             -6.37563061e-03, -4.58286259e-02, -7.00894708e-02,
             -8.48645354e-02, -9.41989454e-02, -9.49114165e-02,
             -8.31684773e-02, -6.93641123e-02, -5.42527703e-02],
            [-4.82490057e-02, -5.99997941e-02, -6.91786120e-02,
             -7.44891242e-02, -6.73705808e-02, -5.13001284e-02,
             -2.84188057e-02, 3.60143816e-03, 4.47470123e-02,
             8.58663851e-02, 1.04548354e-01, 8.58663851e-02,
             4.47470123e-02, 3.60143816e-03, -2.84188057e-02,
             -5.13001284e-02, -6.73705808e-02, -7.44891242e-02,
             -6.91786120e-02, -5.99997941e-02, -4.82490057e-02],
            [-4.03203010e-02, -4.79063206e-02, -5.16352259e-02,
             -4.98707253e-02, -3.67295509e-02, -1.57342058e-02,
             1.13668830e-02, 4.46551184e-02, 8.10450840e-02,
             1.11780747e-01, 1.24226598e-01, 1.11780747e-01,
             8.10450840e-02, 4.46551184e-02, 1.13668830e-02,
             -1.57342058e-02, -3.67295509e-02, -4.98707253e-02,
             -5.16352259e-02, -4.79063206e-02, -4.03203010e-02],
            [-3.10250239e-02, -3.40796094e-02, -3.22089254e-02,
             -2.37094100e-02, -5.85463114e-03, 1.77402761e-02,
             4.57786845e-02, 7.69637052e-02, 1.07537652e-01,
             1.30906328e-01, 1.39800436e-01, 1.30906328e-01,
             1.07537652e-01, 7.69637052e-02, 4.57786845e-02,
             1.77402761e-02, -5.85463114e-03, -2.37094100e-02,
             -3.22089254e-02, -3.40796094e-02, -3.10250239e-02],
            [-2.09301700e-02, -1.94475962e-02, -1.22970199e-02,
             2.07296407e-03, 2.31516868e-02, 4.74574033e-02,
             7.44743481e-02, 1.02380049e-01, 1.27776301e-01,
             1.46003379e-01, 1.52690015e-01, 1.46003379e-01,
             1.27776301e-01, 1.02380049e-01, 7.44743481e-02,
             4.74574033e-02, 2.31516868e-02, 2.07296407e-03,
             -1.22970199e-02, -1.94475962e-02, -2.09301700e-02],
            [-1.05257992e-02, -4.74329696e-03, 7.12107274e-03,
             2.63431361e-02, 4.93709790e-02, 7.31527220e-02,
             9.82233938e-02, 1.22728059e-01, 1.43894925e-01,
             1.58465026e-01, 1.63685984e-01, 1.58465026e-01,
             1.43894925e-01, 1.22728059e-01, 9.82233938e-02,
             7.31527220e-02, 4.93709790e-02, 2.63431361e-02,
             7.12107274e-03, -4.74329696e-03, -1.05257992e-02],
            [-1.89098657e-04, 9.52392382e-03, 2.54577716e-02,
             4.85730869e-02, 7.26048516e-02, 9.51726659e-02,
             1.17988523e-01, 1.39380421e-01, 1.57176612e-01,
             1.69076915e-01, 1.73274075e-01, 1.69076915e-01,
             1.57176612e-01, 1.39380421e-01, 1.17988523e-01,
             9.51726659e-02, 7.26048516e-02, 4.85730869e-02,
             2.54577716e-02, 9.52392382e-03, -1.89098657e-04],
            [9.81732797e-03, 2.30419581e-02, 4.24234701e-02,
             6.86213308e-02, 9.30164618e-02, 1.14050063e-01,
             1.34620894e-01, 1.53304069e-01, 1.68420867e-01,
             1.78321253e-01, 1.81774183e-01, 1.78321253e-01,
             1.68420867e-01, 1.53304069e-01, 1.34620894e-01,
             1.14050063e-01, 9.30164618e-02, 6.86213308e-02,
             4.24234701e-02, 2.30419581e-02, 9.81732797e-03],
            [1.93290725e-02, 3.56493099e-02, 5.79271157e-02,
             8.65611122e-02, 1.10914315e-01, 1.30317702e-01,
             1.48798006e-01, 1.65173224e-01, 1.78147031e-01,
             1.86513895e-01, 1.89408199e-01, 1.86513895e-01,
             1.78147031e-01, 1.65173224e-01, 1.48798006e-01,
             1.30317702e-01, 1.10914315e-01, 8.65611122e-02,
             5.79271157e-02, 3.56493099e-02, 1.93290725e-02],
            [2.68168937e-02, 4.52356810e-02, 6.92261217e-02,
             9.89630241e-02, 1.23093435e-01, 1.40640067e-01,
             1.56998943e-01, 1.71215219e-01, 1.82297185e-01,
             1.89360704e-01, 1.91789146e-01, 1.89360704e-01,
             1.82297185e-01, 1.71215219e-01, 1.56998943e-01,
             1.40640067e-01, 1.23093435e-01, 9.89630241e-02,
             6.92261217e-02, 4.52356810e-02, 2.68168937e-02],
            [3.19403269e-02, 5.15051953e-02, 7.61032066e-02,
             1.05705197e-01, 1.31722206e-01, 1.47466588e-01,
             1.61892450e-01, 1.74235616e-01, 1.83735386e-01,
             1.89735533e-01, 1.91788616e-01, 1.89735533e-01,
             1.83735386e-01, 1.74235616e-01, 1.61892450e-01,
             1.47466588e-01, 1.31722206e-01, 1.05705197e-01,
             7.61032066e-02, 5.15051953e-02, 3.19403269e-02],
            [3.48604070e-02, 5.49292382e-02, 7.94274234e-02,
             1.08149011e-01, 1.38923419e-01, 1.53070440e-01,
             1.65849067e-01, 1.76646162e-01, 1.84871647e-01,
             1.90029617e-01, 1.91787948e-01, 1.90029617e-01,
             1.84871647e-01, 1.76646162e-01, 1.65849067e-01,
             1.53070440e-01, 1.38923419e-01, 1.08149011e-01,
             7.94274234e-02, 5.49292382e-02, 3.48604070e-02],
            [3.53402022e-02, 5.53653759e-02, 7.91965502e-02,
             1.06486934e-01, 1.36563003e-01, 1.57713955e-01,
             1.69087164e-01, 1.78598269e-01, 1.85784340e-01,
             1.90264452e-01, 1.91787141e-01, 1.90264452e-01,
             1.85784340e-01, 1.78598269e-01, 1.69087164e-01,
             1.57713955e-01, 1.36563003e-01, 1.06486934e-01,
             7.91965502e-02, 5.53653759e-02, 3.53402022e-02],
            [3.32889822e-02, 5.28319225e-02, 7.55769079e-02,
             1.01077605e-01, 1.28592068e-01, 1.57023616e-01,
             1.71766715e-01, 1.80199729e-01, 1.86528091e-01,
             1.90454829e-01, 1.91786196e-01, 1.90454829e-01,
             1.86528091e-01, 1.80199729e-01, 1.71766715e-01,
             1.57023616e-01, 1.28592068e-01, 1.01077605e-01,
             7.55769079e-02, 5.28319225e-02, 3.32889822e-02],
            [2.87295370e-02, 4.74613283e-02, 6.88388861e-02,
             9.23568989e-02, 1.17254645e-01, 1.42483223e-01,
             1.66695764e-01, 1.81528776e-01, 1.87141877e-01,
             1.90611190e-01, 1.91785112e-01, 1.90611190e-01,
             1.87141877e-01, 1.81528776e-01, 1.66695764e-01,
             1.42483223e-01, 1.17254645e-01, 9.23568989e-02,
             6.88388861e-02, 4.74613283e-02, 2.87295370e-02],
            [2.17650266e-02, 3.94568191e-02, 5.93023344e-02,
             8.07720575e-02, 1.03124482e-01, 1.25394282e-01,
             1.46405870e-01, 1.64828303e-01, 1.79288925e-01,
             1.88553222e-01, 1.91747252e-01, 1.88553222e-01,
             1.79288925e-01, 1.64828303e-01, 1.46405870e-01,
             1.25394282e-01, 1.03124482e-01, 8.07720575e-02,
             5.93023344e-02, 3.94568191e-02, 2.17650266e-02],
            [1.25495284e-02, 2.90572166e-02, 4.72972116e-02,
             6.67423656e-02, 8.66951873e-02, 1.06290296e-01,
             1.24520131e-01, 1.40293247e-01, 1.52531693e-01,
             1.60303860e-01, 1.62970689e-01, 1.60303860e-01,
             1.52531693e-01, 1.40293247e-01, 1.24520131e-01,
             1.06290296e-01, 8.66951873e-02, 6.67423656e-02,
             4.72972116e-02, 2.90572166e-02, 1.25495284e-02],
            [1.26441934e-03, 1.65114811e-02, 3.31390978e-02,
             5.06407706e-02, 6.83765492e-02, 8.55839448e-02,
             1.01408074e-01, 1.14955639e-01, 1.25373662e-01,
             1.31946425e-01, 1.34193829e-01, 1.31946425e-01,
             1.25373662e-01, 1.14955639e-01, 1.01408074e-01,
             8.55839448e-02, 6.83765492e-02, 5.06407706e-02,
             3.31390978e-02, 1.65114811e-02, 1.26441934e-03],
            [0.00000000e+00, 2.06213867e-03, 1.71162845e-02,
             3.27888240e-02, 4.85026462e-02, 6.35932476e-02,
             7.73387997e-02, 8.90069217e-02, 9.79166934e-02,
             1.03509489e-01, 1.05416736e-01, 1.03509489e-01,
             9.79166934e-02, 8.90069217e-02, 7.73387997e-02,
             6.35932476e-02, 4.85026462e-02, 3.27888240e-02,
             1.71162845e-02, 2.06213867e-03, 0.00000000e+00]]
    )
    np.testing.assert_allclose(
        fd, fd_test, rtol=1e-4)

def test_ss3_m6():
    magnitude = 6.0
    dip = np.array([90])
    rake = 180.0
    width = np.array([15])
    fltx = np.array([0, 0])
    flty = np.array([0, 80])
    zp = np.array([0])
    epix = np.array([0])
    epiy = np.array([0.2 * flty[1]])

    # Convert to lat/lon
    proj = geo.utils.get_orthographic_projection(-122, -120, 39, 37)
    tlon, tlat = proj(fltx, flty, reverse=True)
    epilon, epilat = proj(epix, epiy, reverse=True)

    flt = fault.Fault.fromTrace(np.array([tlon[0]]), np.array([tlat[0]]),
                                np.array([tlon[1]]), np.array([tlat[1]]),
                                zp, width, dip, reference='ss3')

    event = {'lat': epilat[0],
             'lon': epilon[0],
             'depth': 10,
             'mag': magnitude,
             'id': 'ss3',
             'locstring': 'test',
             'type': 'SS',
             'timezone': 'UTC'}
    event['time'] = ShakeDateTime.utcfromtimestamp(int(time.time()))
    event['created'] = ShakeDateTime.utcfromtimestamp(int(time.time()))

    x = np.linspace(0, 20, 6)
    y = np.linspace(0, 90, 11)
    site_x, site_y = np.meshgrid(x, y)
    slon, slat = proj(site_x, site_y, reverse=True)
    deps = np.zeros_like(slon)
    source = Source(event, flt)
    source.setEventParam('rake', rake)

    test1 = Bayless2013(source, slat, slon, deps, T=1.0)

    # Test fd
    fd = test1.getFd()
    fd_test = np.array(
      [[ 0.05853668,  0.05032323,  0.0306438 ,  0.00839635, -0.01102162,
        -0.02621319],
       [ 0.01720501, -0.00687296, -0.03804823, -0.05547473, -0.0644932 ,
        -0.06947135],
       [-0.03000065, -0.07006634, -0.07708165, -0.07865941, -0.0792369 ,
        -0.07950887],
       [ 0.0398062 ,  0.02571145, -0.0018651 , -0.0255418 , -0.04176278,
        -0.05235095],
       [ 0.0696989 ,  0.06389524,  0.04890304,  0.02983134,  0.01098535,
        -0.00545921],
       [ 0.088278  ,  0.08511069,  0.07628596,  0.06350294,  0.04875897,
         0.03373495],
       [ 0.10179334,  0.09978475,  0.09401676,  0.0851842 ,  0.07422509,
         0.06210369],
       [ 0.11242209,  0.11102701,  0.10696056,  0.10055471,  0.09229027,
         0.08271454],
       [ 0.12118279,  0.12015315,  0.11712653,  0.11228058,  0.10588323,
         0.09825795],
       [ 0.12785957,  0.12706892,  0.12473264,  0.12095384,  0.11589197,
         0.10974684],
       [ 0.12785908,  0.12724852,  0.12543819,  0.12249026,  0.11850249,
         0.11360047]])
    np.testing.assert_allclose(
        fd, fd_test, rtol=1e-4)

#def test_ss3_move_hypo1():
#    magnitude = 7.2
#    dip = np.array([90])
#    rake = 180.0
#    width = np.array([15])
#    fltx = np.array([0, 0])
#    flty = np.array([0, 80])
#    zp = np.array([-1.0]) # positive down
#    epix = np.array([3.0])
#    epiy = np.array([0.2 * flty[1]])

#    # Convert to lat/lon
#    proj = geo.utils.get_orthographic_projection(-122, -120, 39, 37)
#    tlon, tlat = proj(fltx, flty, reverse=True)
#    epilon, epilat = proj(epix, epiy, reverse=True)

#    flt = fault.Fault.fromTrace(np.array([tlon[0]]), np.array([tlat[0]]),
#                                np.array([tlon[1]]), np.array([tlat[1]]),
#                                zp, width, dip, reference='ss3')

#    event = {'lat': epilat[0],
#             'lon': epilon[0],
#             'depth': 10,
#             'mag': magnitude,
#             'id': 'ss3',
#             'locstring': 'test',
#             'type': 'SS',
#             'timezone': 'UTC'}
#    event['time'] = ShakeDateTime.utcfromtimestamp(int(time.time()))
#    event['created'] = ShakeDateTime.utcfromtimestamp(int(time.time()))

#    x = np.linspace(0, 20, 6)
#    y = np.linspace(0, 90, 11)
#    site_x, site_y = np.meshgrid(x, y)
#    slon, slat = proj(site_x, site_y, reverse=True)
#    deps = np.zeros_like(slon)
#    source = Source(event, flt)
#    source.setEventParam('rake', rake)

#    test1 = Bayless2013(source, slat, slon, deps, T=1.0)

#    # Test fd
#    fd = test1.getFd()
#    fd_test = np.array(
#    np.testing.assert_allclose(
#        fd, fd_test, rtol=1e-4)


def test_ss3_m4p5():
    magnitude = 4.5
    dip = np.array([90])
    rake = 180.0
    width = np.array([15])
    fltx = np.array([0, 0])
    flty = np.array([0, 80])
    zp = np.array([0])
    epix = np.array([0])
    epiy = np.array([0.2 * flty[1]])

    # Convert to lat/lon
    proj = geo.utils.get_orthographic_projection(-122, -120, 39, 37)
    tlon, tlat = proj(fltx, flty, reverse=True)
    epilon, epilat = proj(epix, epiy, reverse=True)

    flt = fault.Fault.fromTrace(np.array([tlon[0]]), np.array([tlat[0]]),
                                np.array([tlon[1]]), np.array([tlat[1]]),
                                zp, width, dip, reference='ss3')

    event = {'lat': epilat[0],
             'lon': epilon[0],
             'depth': 10,
             'mag': magnitude,
             'id': 'ss3',
             'locstring': 'test',
             'type': 'SS',
             'timezone': 'UTC'}
    event['time'] = ShakeDateTime.utcfromtimestamp(int(time.time()))
    event['created'] = ShakeDateTime.utcfromtimestamp(int(time.time()))

    x = np.linspace(0, 20, 6)
    y = np.linspace(0, 90, 11)
    site_x, site_y = np.meshgrid(x, y)
    slon, slat = proj(site_x, site_y, reverse=True)
    deps = np.zeros_like(slon)
    source = Source(event, flt)
    source.setEventParam('rake', rake)

    test1 = Bayless2013(source, slat, slon, deps, T=1.0)

    # Test fd
    fd = test1.getFd()
    fd_test = np.array(
      [[ 0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.]])
    np.testing.assert_allclose(
        fd, fd_test, rtol=1e-4)



def test_rv4():
    magnitude = 7.0
    rake = 90.0
    width = np.array([28])
    fltx = np.array([0, 0])
    flty = np.array([0, 32])
    zp = np.array([0])
    dip = np.array([30])

    # Convert to lat/lon
    proj = geo.utils.get_orthographic_projection(-122, -120, 39, 37)
    tlon, tlat = proj(fltx, flty, reverse=True)

    flt = fault.Fault.fromTrace(np.array([tlon[0]]), np.array([tlat[0]]),
                                np.array([tlon[1]]), np.array([tlat[1]]),
                                zp, width, dip, reference='')
    L = flt.getFaultLength()

    # Try to figure out epicenter
    tmp = flt.getQuadrilaterals()[0]
    pp0 = Vector.fromPoint(point.Point(tmp[0].longitude, tmp[0].latitude,
                                       tmp[0].depth))
    pp1 = Vector.fromPoint(point.Point(tmp[1].longitude, tmp[1].latitude,
                                       tmp[1].depth))
    pp2 = Vector.fromPoint(point.Point(tmp[2].longitude, tmp[2].latitude,
                                       tmp[2].depth))
    pp3 = Vector.fromPoint(point.Point(tmp[3].longitude, tmp[3].latitude,
                                       tmp[3].depth))
    dxp = 6/L
    dyp = (width-8)/width
    mp0 = pp0 + (pp1 - pp0)*dxp
    mp1 = pp3 + (pp2 - pp3)*dxp
    rp = mp0 + (mp1 - mp0)*dyp
    epilat,epilon,epidepth = ecef2latlon(rp.x, rp.y, rp.z)

    event = {'lat': epilat,
             'lon': epilon,
             'depth': epidepth,
             'mag': magnitude,
             'id': 'test',
             'locstring': 'rv4',
             'type': 'DS',
             'timezone': 'UTC'}
    event['time'] = ShakeDateTime.utcfromtimestamp(int(time.time()))
    event['created'] = ShakeDateTime.utcfromtimestamp(int(time.time()))

    x = np.linspace(-50, 50, 11)
    y = np.linspace(-50, 50, 11)
    site_x, site_y = np.meshgrid(x, y)
    slon, slat = proj(site_x, site_y, reverse=True)
    deps = np.zeros_like(slon)
    source = Source(event, flt)
    source.setEventParam('rake', rake)

    test1 = Bayless2013(source, slat, slon, deps, T=2.0)

    # Test fd
    fd = test1.getFd()
    fd_test = np.array(
      [[  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          1.72143257e-03,   1.34977260e-03,   4.33616224e-15,
          1.24446253e-03,   1.16142357e-03,   2.25464716e-03,
          7.05281751e-04,   0.00000000e+00],
       [  0.00000000e+00,   0.00000000e+00,   7.62610242e-03,
          1.25133844e-02,   5.61896104e-03,   7.63126014e-15,
          4.52266194e-03,   4.67970900e-03,   1.02820316e-02,
          5.13160096e-03,  -6.13926251e-03],
       [  0.00000000e+00,   4.00495234e-03,   2.37608386e-02,
          2.37139333e-02,   9.55224050e-03,   5.66364910e-15,
          7.70344813e-03,   7.36466362e-03,   1.48239704e-02,
          8.40388145e-03,  -1.58592485e-02],
       [  8.08385547e-19,   9.38150101e-03,   3.38610620e-02,
          3.85351492e-02,   1.91044918e-02,   3.98697802e-15,
          1.54321666e-02,   1.21913760e-02,   2.04435166e-02,
          1.04931859e-02,  -1.85935894e-02],
       [  2.12025421e-18,   1.37316085e-02,   4.40193799e-02,
          6.16562477e-02,   4.77612496e-02,   2.60257085e-15,
          3.86322888e-02,   1.97965887e-02,   2.64882038e-02,
          1.23335908e-02,  -2.07389932e-02],
       [  2.64338576e-18,   1.45898292e-02,   4.89104213e-02,
          7.70703166e-02,   9.55225258e-02,   1.01875104e-01,
          7.73459329e-02,   2.50275508e-02,   2.93537540e-02,
          1.30949577e-02,  -2.15685454e-02],
       [  2.64330042e-18,   1.45898262e-02,   4.89104186e-02,
          7.70703146e-02,   9.55225248e-02,   1.01910945e-01,
          7.74050835e-02,   2.52307946e-02,   2.92970736e-02,
          1.30880504e-02,  -2.15685424e-02],
       [  2.64318867e-18,   1.45898259e-02,   4.89104184e-02,
          7.70703144e-02,   9.55225247e-02,   1.01933432e-01,
          7.74421258e-02,   2.53572923e-02,   2.92615130e-02,
          1.30837284e-02,  -2.15685422e-02],
       [  2.64305117e-18,   1.45898284e-02,   4.89104206e-02,
          7.70703161e-02,   9.55225256e-02,   1.01942593e-01,
          7.74571359e-02,   2.54081640e-02,   2.92472117e-02,
          1.30819985e-02,  -2.15685446e-02],
       [  2.30141673e-18,   1.40210825e-02,   4.56205547e-02,
          6.63109661e-02,   5.79266964e-02,   2.33044622e-15,
          4.69672564e-02,   2.18401553e-02,   2.72864925e-02,
          1.25728575e-02,  -2.10227772e-02],
       [  1.10672535e-18,   1.04777076e-02,   3.59041065e-02,
          4.24614318e-02,   2.24217216e-02,   3.66914762e-15,
          1.81728517e-02,   1.39301504e-02,   2.14956836e-02,
          1.08711460e-02,  -1.90802849e-02]]
    )
    np.testing.assert_allclose(fd, fd_test, rtol=2e-4)
    
def test_so6():
    event_name = 'so6'
    magnitude = 7.2
    dip = np.array([70])
    rake = 135
    width = np.array([15])
    L = 80
    fltx = np.array([0, 0])
    flty = np.array([0, L])
    zp = np.array([0])
    # Convert to lat/lon
    proj = geo.utils.get_orthographic_projection(-122, -120, 39, 37)
    tlon,tlat = proj(fltx, flty, reverse = True)
    flt = fault.Fault.fromTrace(np.array([tlon[0]]), np.array([tlat[0]]), 
                                np.array([tlon[1]]), np.array([tlat[1]]),
                                zp, width, dip, reference = 'rv4')
    x = np.linspace(-80, 80, 21)
    y = np.linspace(-50, 130, 21)
    site_x,site_y = np.meshgrid(x, y)
    slon,slat = proj(site_x, site_y, reverse = True)
    sdepth = np.zeros_like(slon)
    tmp = flt.getQuadrilaterals()[0]
    pp0 = Vector.fromPoint(point.Point(tmp[0].longitude, tmp[0].latitude, tmp[0].depth))
    pp1 = Vector.fromPoint(point.Point(tmp[1].longitude, tmp[1].latitude, tmp[1].depth))
    pp2 = Vector.fromPoint(point.Point(tmp[2].longitude, tmp[2].latitude, tmp[2].depth))
    pp3 = Vector.fromPoint(point.Point(tmp[3].longitude, tmp[3].latitude, tmp[3].depth))
    dxp = 10/L
    dyp = (width-5)/width
    mp0 = pp0 + (pp1 - pp0)*dxp
    mp1 = pp3 + (pp2 - pp3)*dxp
    rp = mp0 + (mp1 - mp0)*dyp
    epilat,epilon,epidepth = ecef2latlon(rp.x, rp.y, rp.z)
    epix,epiy = proj(epilon, epilat, reverse = False)
    event = {'lat': epilat, 
             'lon': epilon, 
             'depth':epidepth, 
             'mag': magnitude, 
             'id':'so6',
             'locstring':'so6',
             'type':'RV',
             'timezone':'UTC'}
    event['time'] = ShakeDateTime.utcfromtimestamp(int(time.time()))
    event['created'] = ShakeDateTime.utcfromtimestamp(int(time.time()))
    fltlat = [a.latitude for a in flt.getQuadrilaterals()[0]]
    fltlon = [a.longitude for a in flt.getQuadrilaterals()[0]]
    fltlat = np.append(fltlat, fltlat[0])
    fltlon = np.append(fltlon, fltlon[0])
    fltx,flty = proj(fltlon, fltlat, reverse = False)
    source = Source(event, flt)
    source.setEventParam('rake', rake)
    test1 = Bayless2013(source, slat, slon, sdepth, T = 5)
    fd = test1.getFd()
    fd_test = np.array(
      [[  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         -8.92879772e-03,  -1.74526918e-02,  -2.22981746e-02,
         -2.34350450e-02,  -2.13620062e-02,  -1.72712346e-02,
         -1.29509613e-02,  -1.02545064e-02,  -1.03010185e-02,
         -1.28847597e-02,  -1.66274727e-02,  -1.96984070e-02,
         -2.05377743e-02,  -1.81831337e-02,  -1.21881814e-02,
         -2.64862879e-03,   0.00000000e+00,   0.00000000e+00],
       [  0.00000000e+00,   0.00000000e+00,  -8.73221519e-03,
         -2.21421374e-02,  -3.18438939e-02,  -3.71488270e-02,
         -3.76239913e-02,  -3.35015951e-02,  -2.61748968e-02,
         -1.83864728e-02,  -1.34793002e-02,  -1.36687799e-02,
         -1.85727143e-02,  -2.55527671e-02,  -3.14227568e-02,
         -3.38933995e-02,  -3.19289607e-02,  -2.53396980e-02,
         -1.45943649e-02,  -3.71405488e-04,   0.00000000e+00],
       [  0.00000000e+00,  -2.54621422e-03,  -2.11428566e-02,
         -3.68609103e-02,  -4.87464747e-02,  -5.56539037e-02,
         -5.64419387e-02,  -5.05331157e-02,  -3.52919381e-02,
         -2.18782050e-02,  -1.40858125e-02,  -1.47354546e-02,
         -2.35727189e-02,  -3.74838465e-02,  -4.75915414e-02,
         -5.13000399e-02,  -4.87882409e-02,  -4.05716321e-02,
         -2.77368254e-02,  -1.13542729e-02,   0.00000000e+00],
       [  0.00000000e+00,  -1.21642958e-02,  -3.33747360e-02,
         -5.21661817e-02,  -6.74724509e-02,  -7.77628842e-02,
         -8.00243748e-02,  -6.42496853e-02,  -4.38124530e-02,
         -1.97027426e-02,  -1.45897731e-02,  -1.07427056e-02,
         -3.08235222e-02,  -4.82656988e-02,  -6.67692677e-02,
         -7.35152908e-02,  -6.85574283e-02,  -5.71811573e-02,
         -4.12138780e-02,  -2.20396726e-02,  -6.24121310e-04],
       [  0.00000000e+00,  -2.00643401e-02,  -4.39827328e-02,
         -6.62722434e-02,  -8.60268414e-02,  -1.01730306e-01,
         -9.86277741e-02,  -9.82914922e-02,  -5.22335876e-02,
         -1.54622435e-02,  -1.57487554e-02,  -3.06190808e-03,
         -4.81481586e-02,  -8.92480491e-02,  -8.63776477e-02,
         -9.98130440e-02,  -8.95491230e-02,  -7.33553695e-02,
         -5.34401725e-02,  -3.11601812e-02,  -7.33715103e-03],
       [  0.00000000e+00,  -2.50053614e-02,  -5.11695772e-02,
         -7.65997026e-02,  -1.00809054e-01,  -1.22877573e-01,
         -1.18738178e-01,  -1.55236782e-01,  -7.45388001e-02,
          1.92779182e-03,  -1.94380016e-02,   1.94922939e-02,
         -7.66669920e-02,  -1.53909722e-01,  -1.10846875e-01,
         -1.19746768e-01,  -1.07680300e-01,  -8.59905101e-02,
         -6.22042294e-02,  -3.71802472e-02,  -1.13867485e-02],
       [  0.00000000e+00,  -2.63645827e-02,  -5.37984901e-02,
         -8.11337022e-02,  -1.08298371e-01,  -1.35146441e-01,
         -1.34825430e-01,  -1.85836050e-01,  -1.10730875e-01,
         -3.18861095e-02,   4.14395701e-02,  -1.52711946e-02,
         -1.31840763e-01,  -1.96794707e-01,  -1.33453212e-01,
         -1.34989129e-01,  -1.17922385e-01,  -9.21637323e-02,
         -6.58369237e-02,  -3.91646838e-02,  -1.22685698e-02],
       [  0.00000000e+00,  -2.64622244e-02,  -5.40483999e-02,
         -8.16190336e-02,  -1.09162854e-01,  -1.36656677e-01,
         -1.37081504e-01,  -1.89522811e-01,  -1.17723634e-01,
         -4.88765748e-02,  -5.04529015e-03,  -5.76414497e-02,
         -1.45712183e-01,  -2.03062804e-01,  -1.36859828e-01,
         -1.37107390e-01,  -1.19124650e-01,  -9.28263279e-02,
         -6.61800709e-02,  -3.93088682e-02,  -1.22842049e-02],
       [  0.00000000e+00,  -2.58466495e-02,  -5.24858827e-02,
         -7.86086164e-02,  -1.03856343e-01,  -1.27529509e-01,
         -1.23794779e-01,  -1.68810613e-01,  -8.22602627e-02,
          1.74236964e-02,   9.38708725e-02,   4.23208284e-02,
         -8.46343723e-02,  -1.70476759e-01,  -1.17547884e-01,
         -1.24569752e-01,  -1.11518670e-01,  -8.84736806e-02,
         -6.38037151e-02,  -3.81874381e-02,  -1.19867610e-02],
       [  0.00000000e+00,  -2.42186547e-02,  -4.84175525e-02,
         -7.09428614e-02,  -9.07754575e-02,  -1.06117824e-01,
         -9.50228292e-02,  -1.29781980e-01,  -3.08573454e-02,
          7.39058739e-02,   1.30478117e-01,   8.28181149e-02,
         -2.70389535e-02,  -1.20837502e-01,  -8.02081725e-02,
         -9.70274506e-02,  -9.35853383e-02,  -7.77422806e-02,
         -5.77817530e-02,  -3.53067886e-02,  -1.12414659e-02],
       [  0.00000000e+00,  -2.16818717e-02,  -4.22363856e-02,
         -5.96909893e-02,  -7.24805224e-02,  -7.81867829e-02,
         -6.11838569e-02,  -9.05679744e-02,   9.95934969e-03,
          1.07503875e-01,   1.52073917e-01,   1.05894634e-01,
          8.68652263e-03,  -7.98571818e-02,  -4.16548658e-02,
         -6.40511838e-02,  -6.99337160e-02,  -6.26305633e-02,
         -4.89098800e-02,  -3.09284566e-02,  -1.00919381e-02],
       [  0.00000000e+00,  -1.84940182e-02,  -3.47054606e-02,
         -4.65278129e-02,  -5.22037664e-02,  -4.93977115e-02,
         -2.95395230e-02,  -5.82421092e-02,   3.91025654e-02,
          1.29337956e-01,   1.67436703e-01,   1.21969296e-01,
          3.20823547e-02,  -5.00287386e-02,  -9.22993907e-03,
         -3.27186625e-02,  -4.52706958e-02,  -4.57409325e-02,
         -3.84701291e-02,  -2.55751405e-02,  -8.64950254e-03],
       [  0.00000000e+00,  -1.49431380e-02,  -2.65887341e-02,
         -3.29162158e-02,  -3.22994323e-02,  -2.29081781e-02,
         -2.60259636e-03,  -3.29856530e-02,   6.02631314e-02,
          1.45003704e-01,   1.79361264e-01,   1.34292814e-01,
          4.88007115e-02,  -2.82328554e-02,   1.64212421e-02,
         -5.72391847e-03,  -2.23438861e-02,  -2.90246794e-02,
         -2.76054402e-02,  -1.97779758e-02,  -7.03945406e-03],
       [  0.00000000e+00,  -1.12771143e-02,  -1.84737590e-02,
         -1.98228664e-02,  -1.40092305e-02,   1.84580818e-04,
          1.95817303e-02,  -1.32608487e-02,   7.62783168e-02,
          1.57076433e-01,   1.89083905e-01,   1.44259188e-01,
          6.15722813e-02,  -1.17505212e-02,   3.65938109e-02,
          1.66937711e-02,  -2.18970818e-03,  -1.35507683e-02,
         -1.70890527e-02,  -1.39519424e-02,  -5.37036892e-03],
       [  0.00000000e+00,  -7.67615215e-03,  -1.07348257e-02,
         -7.75276739e-03,   2.22351695e-03,   1.98662250e-02,
          3.77611177e-02,   2.42018661e-03,   8.89036172e-02,
          1.66855206e-01,   1.97260700e-01,   1.52590263e-01,
          7.17981256e-02,   1.18005972e-03,   5.26852303e-02,
          3.51638855e-02,   1.51012176e-02,   2.69654076e-04,
         -7.33815554e-03,  -8.36639665e-03,  -3.72176313e-03],
       [  0.00000000e+00,  -4.50552324e-03,  -4.32262850e-03,
          1.73559158e-03,   1.42670366e-02,   3.35040699e-02,
          4.97279358e-02,   1.85410528e-02,   9.39950666e-02,
          1.46646579e-01,   9.13474746e-02,   1.37004651e-01,
          7.74648339e-02,   1.59777072e-02,   6.25334939e-02,
          4.74577418e-02,   2.72155518e-02,   1.06174952e-02,
          3.94103899e-04,  -3.68465400e-03,  -2.19830733e-03],
       [  0.00000000e+00,  -1.74629916e-03,   5.44471813e-04,
          8.22933499e-03,   2.15699287e-02,   4.04232250e-02,
          5.69678048e-02,   5.52408259e-02,   9.04381272e-02,
          1.08204635e-01,   9.14439984e-02,   1.06884511e-01,
          8.17241884e-02,   5.55282924e-02,   6.78528399e-02,
          5.47188925e-02,   3.35251483e-02,   1.69615982e-02,
          5.72048628e-03,  -8.81437278e-05,  -7.36518436e-04],
       [  0.00000000e+00,   4.07838765e-05,   3.63933766e-03,
          1.20080876e-02,   2.51274691e-02,   4.25687176e-02,
          6.25685606e-02,   7.33480475e-02,   8.37515545e-02,
          9.52500287e-02,   9.15135660e-02,   9.66442834e-02,
          8.66659913e-02,   8.10325633e-02,   7.18836713e-02,
          5.45548434e-02,   3.55884875e-02,   2.00142359e-02,
          8.71200201e-03,   2.04407846e-03,  -6.53680674e-06],
       [  0.00000000e+00,   2.40054729e-04,   4.44975227e-03,
          1.27572519e-02,   2.49362989e-02,   4.03831326e-02,
          5.80039988e-02,   7.61280192e-02,   8.37404162e-02,
          8.89634569e-02,   9.15651607e-02,   9.13586235e-02,
          8.83589144e-02,   8.27804032e-02,   6.75666471e-02,
          5.00483249e-02,   3.36733366e-02,   1.96758691e-02,
          9.00603204e-03,   2.18370401e-03,   0.00000000e+00],
       [  0.00000000e+00,   0.00000000e+00,   2.78776980e-03,
          1.05086036e-02,   2.13238822e-02,   3.45577738e-02,
          4.91570145e-02,   6.36787133e-02,   7.63710088e-02,
          8.54072310e-02,   8.92960200e-02,   8.75702197e-02,
          8.07095447e-02,   6.97999389e-02,   5.63787286e-02,
          4.20734776e-02,   2.83073312e-02,   1.61614525e-02,
          6.56194125e-03,   1.00721924e-04,   0.00000000e+00],
       [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          5.49667845e-03,   1.47563319e-02,   2.57955743e-02,
          3.76689418e-02,   4.91861917e-02,   5.90108907e-02,
          6.58478416e-02,   6.87018515e-02,   6.73174642e-02,
          6.20270643e-02,   5.35456385e-02,   4.29400416e-02,
          3.14129728e-02,   2.00795162e-02,   9.84001885e-03,
          1.53992995e-03,   0.00000000e+00,   0.00000000e+00]]
    )
    np.testing.assert_allclose(fd, fd_test, rtol=1e-4)

if __name__ == '__main__':
    test_ss3()
    test_rv4()
    test_so6()
