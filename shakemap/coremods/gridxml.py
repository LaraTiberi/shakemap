# stdlib imports
import os.path
import json
import logging
from datetime import datetime
import re
from collections import OrderedDict

# third party imports
import numpy as np
from shakelib.utils.containers import ShakeMapOutputContainer
from mapio.shake import ShakeGrid

# local imports
from .base import CoreModule
from shakemap.utils.config import get_config_paths
import shakemap

# historically, we only had the component we are now calling
# 'GREATER_OF_TWO_HORIZONTAL'.
# As we do not intend grid.xml files to be forward compatible with
# additional layers of information and different components (RotD50, etc.)
# we'll hard code this here until grid.xml files experience their heat death.
COMPONENT = 'GREATER_OF_TWO_HORIZONTAL'

TIMEFMT = '%Y-%m-%dT%H:%M:%SZ'


def _oq_to_gridxml(oqimt):
    """
    Convert openquake IMT nomenclature to grid.xml friendly form.

    Note: The grid.xml form only handles periods up to 9.9, after
    that there is no way to tell the difference between 10.0 and 1.0.

    Examples:
    SA(1.0) (Spectral Acceleration at 1 second) -> PSA10
    SA(0.3) (Spectral Acceleration at 0.3 second) -> PSA03
    SA(15.0) (Spectral Acceleration at 15 seconds) -> NOT SUPPORTED
    SA(3) (Spectral Acceleration at 3 seconds) -> PSA30
    SA(.5) (Spectral Acceleration at 0.5 seconds) -> PSA05


    Args:
        oqimt (str): Openquake IMT nomenclature string.
    Returns:
        str: grid.xml friendly IMT string.
    Raises:
        ValueError: when there is no corresponding filename-friendly
            IMT representation, or when frequency exceeds 9.9.
    """
    if oqimt in ['PGA', 'PGV', 'MMI','IA','PGD','IH']:
        return oqimt
    float_pattern = r"[-+]?\d*\.\d+|\d+"
    periods = re.findall(float_pattern, oqimt)
    if not len(periods):
        fmt = 'IMT string "%s" has no file-name friendly representation.'
        raise ValueError(fmt % oqimt)
    period = periods[0]
    if period.find('.') < 0:
        integer = period
        fraction = '0'
    else:
        integer, fraction = period.split('.')
        if not len(integer):
            integer = '0'
    if int(integer) >= 10:
        raise ValueError('Periods >= than 10 seconds not supported.')
    fileimt = 'PSA%s%s' % (integer, fraction)
    return fileimt


class GridXMLModule(CoreModule):
    """
    gridxml -- Create grid.xml and uncertainty.xml files from shake_result.hdf.
    """

    command_name = 'gridxml'

    contents = {'xmlGrids': {'title': 'XML Grid',
                             'caption': 'XML grid of ground motions',
                             'formats': [{'filename': 'grid.xml',
                                          'type': 'text/xml'}
                                         ]
                             },
                'uncertaintyGrid': {'title': 'Uncertainty Grid',
                                    'caption': 'XML grid of uncertainties',
                                    'formats': [{'filename': 'uncertainty.xml',
                                                 'type': 'text/xml'}
                                                ]
                                    }
                }

    def execute(self):
        """Create grid.xml and uncertainty.xml files.

        Raises:
            NotADirectoryError: When the event data directory does not exist.
            FileNotFoundError: When the the shake_result HDF file does not
                exist.
        """
        logger = logging.getLogger(__name__)
        install_path, data_path = get_config_paths()
        datadir = os.path.join(data_path, self._eventid, 'current', 'products')
        if not os.path.isdir(datadir):
            raise NotADirectoryError('%s is not a valid directory.' % datadir)
        datafile = os.path.join(datadir, 'shake_result.hdf')
        if not os.path.isfile(datafile):
            raise FileNotFoundError('%s does not exist.' % datafile)

        # Open the ShakeMapOutputContainer and extract the data
        container = ShakeMapOutputContainer.load(datafile)

        # get all of the grid layers and the geodict
        if container.getDataType() != 'grid':
            raise NotImplementedError('gridxml module can only function on '
                                      'gridded data, not sets of points')
        gridnames = container.getIMTs(COMPONENT)
        xml_types = ['grid', 'uncertainty']
        for xml_type in xml_types:
            layers = OrderedDict()
            field_keys = OrderedDict()
            for gridname in gridnames:
                imt_field = _oq_to_gridxml(gridname)
                imtdict = container.getIMTGrids(gridname, COMPONENT)
                if xml_type == 'grid':
                    grid = imtdict['mean']
                    metadata = imtdict['mean_metadata']
                elif xml_type == 'uncertainty':
                    grid = imtdict['std']
                    metadata = imtdict['std_metadata']

                units = metadata['units']
                digits = metadata['digits']
                grid_data = grid.getData()
                # convert from HDF units to legacy grid.xml units
                if xml_type == 'grid':
                    if units == 'ln(cm/s)':
                        grid_data = np.exp(grid_data)
                        units = 'cm/s'
                    elif units == 'ln(g)':
                        grid_data = np.exp(grid_data) * 100
                        units = '%g'
                    else:
                        pass

                if xml_type == 'grid':
                    layers[imt_field] = grid_data
                    field_keys[imt_field] = (units, digits)
                else:
                    layers['STD' + imt_field] = grid_data
                    field_keys['STD' + imt_field] = (units, digits)

            geodict = grid.getGeoDict()

            config = container.getConfig()

            # event dictionary
            info = container.getMetadata()
            event_info = info['input']['event_information']
            event_dict = {}
            event_dict['event_id'] = event_info['event_id']
            event_dict['magnitude'] = float(event_info['magnitude'])
            event_dict['depth'] = float(event_info['depth'])
            event_dict['lat'] = float(event_info['latitude'])
            event_dict['lon'] = float(event_info['longitude'])
            event_dict['event_timestamp'] = datetime.strptime(
                event_info['origin_time'], TIMEFMT)
            event_dict['event_description'] = event_info['location']
            event_dict['event_network'] = \
                info['input']['event_information']['eventsource']

            # shake dictionary
            shake_dict = {}
            shake_dict['event_id'] = event_dict['event_id']
            shake_dict['shakemap_id'] = event_dict['event_id']
            shake_dict['shakemap_version'] = \
                info['processing']['shakemap_versions']['map_version']
            shake_dict['code_version'] = shakemap.__version__
            ptime = info['processing']['shakemap_versions']['process_time']
            shake_dict['process_timestamp'] = datetime.strptime(ptime, TIMEFMT)
            shake_dict['shakemap_originator'] = \
                config['system']['source_network']
            shake_dict['map_status'] = config['system']['map_status']
            shake_dict['shakemap_event_type'] = 'ACTUAL'
            if event_dict['event_id'].endswith('_se'):
                shake_dict['shakemap_event_type'] = 'SCENARIO'

            shake_grid = ShakeGrid(
                layers, geodict, event_dict,
                shake_dict, {}, field_keys=field_keys)
            fname = os.path.join(datadir, '%s.xml' % xml_type)
            logger.debug('Saving IMT grids to %s' % fname)
            shake_grid.save(fname)  # TODO - set grid version number
