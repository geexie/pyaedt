# Import exception handling here due to:
# https://github.com/pyansys/PyAEDT/pull/243
import os
os.environ["SF6694_NON_GRAPHICAL_COMMAND_EXECUTION"] = "1"
os.environ["SF159726_SCRIPTOBJECT"] = "1"
from pyaedt.generic.general_methods import aedt_exception_handler, generate_unique_name, retry_ntimes
from pyaedt.generic.general_methods import is_ironpython, _pythonver, inside_desktop, convert_remote_object
from pyaedt.aedt_logger import AedtLogger
from pyaedt.generic.design_types import (Hfss3dLayout,
                                         Hfss,
                                         Circuit,
                                         Q2d,
                                         Q3d,
                                         Siwave,
                                         Icepak,
                                         Edb,
                                         Maxwell3d,
                                         Maxwell2d,
                                         Mechanical,
                                         Rmxprt,
                                         Simplorer,
                                         Emit,
                                         get_pyaedt_app,
                                         Desktop)




