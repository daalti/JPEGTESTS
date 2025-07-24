import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 10Page_halflf.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:10Page-halflf.obj=de108406e4a6b545ba61ecf23344c69a5feaae92b7eb590a0ec15fd9e8ae5424
    +test_classification:System
    +name: test_pcl5_highvalue_10page_halflf
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_10page_halflf
        +guid:63a31062-0485-454a-bc6c-753746b42080
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_10page_halflf(setup_teardown, printjob,udw,outputsaver, print_emulation):
    outputsaver.validate_crc_tiff(udw)
    if print_emulation.print_engine_platform == 'emulator':
        installed_trays = print_emulation.tray.get_installed_trays()
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            if MediaSize.Letter.name in supported_sizes and MediaType.Plain.name in supported_types:
                print_emulation.tray.load(tray_id, MediaSize.Letter.name, MediaType.Plain.name)
    printjob.print_verify('de108406e4a6b545ba61ecf23344c69a5feaae92b7eb590a0ec15fd9e8ae5424', timeout=300)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
