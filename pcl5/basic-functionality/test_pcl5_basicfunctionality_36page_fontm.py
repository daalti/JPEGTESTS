import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 36Page_fontm.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:36Page-fontm.obj=2a6caaac98023d5747cdad4ef443e46e42b453c97841e6a90cf8d69e114551b5
    +test_classification:System
    +name: test_pcl5_basicfunctionality_36page_fontm
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_36page_fontm
        +guid:37a560a8-5ce4-48cc-afec-bfd427aadcfe
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:800
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_36page_fontm(setup_teardown, printjob, outputsaver,udw, print_emulation):
    if print_emulation.print_engine_platform == 'emulator':
        print_emulation.tray.setup_tray(
            trayid="all",
            media_size=MediaSize.Letter.name,
            media_type=MediaType.Plain.name,
            orientation=MediaOrientation.Default.name,
            level=TrayLevel.Full.name
        )
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('2a6caaac98023d5747cdad4ef443e46e42b453c97841e6a90cf8d69e114551b5',timeout=800)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
