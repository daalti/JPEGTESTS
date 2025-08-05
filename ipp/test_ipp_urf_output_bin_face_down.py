import pytest
import logging

from dunetuf.network.ipp.ipp_utils import IppTool
from dunetuf.utility.systemtestpath import get_system_test_binaries_path
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation, TrayLevel

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value output-bin_face-down
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Letter_Color_600.urf=6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f
    +name:test_ipp_urf_output_bin_face_down
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_output_bin_face_down
        +guid:472b2d00-d53d-4ed9-adf2-58b7f26d0a08
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaPath=FaceDown

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_output_bin_face_down(setup_teardown, printjob, outputsaver, tray, net, print_emulation):

    ipptool = IppTool(net.ip_address)
    attribute = 'output-bin-supported'  
    response = ipptool.get(attribute)
    if attribute not in response:
        assert False, "{} attribute is missing!".format(attribute)

    values = response[attribute]
   
    if 'face-down' not in values:
        logging.info("face-down attribute value is not present for this configuration.  this product configuration contain = " + str(values))

    else:
        outputsaver.operation_mode('TIFF')
        default = tray.get_default_source()
        if print_emulation.print_engine_platform == 'emulator':
            print_emulation.tray.setup_tray(
            trayid="all",
            media_size=MediaSize.Letter.name,
            media_type=MediaType.Plain.name,
            orientation=MediaOrientation.Default.name,
            level=TrayLevel.Full.name
        )
        elif tray.is_size_supported('na_letter_8.5x11in', default):
            tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

        ipp_test_attribs = {'document-format': 'image/urf', 'output-bin': 'face-down'}
        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

        printjob.ipp_print(ipp_test_file, '6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f')
        outputsaver.save_output()
        outputsaver.operation_mode('NONE')