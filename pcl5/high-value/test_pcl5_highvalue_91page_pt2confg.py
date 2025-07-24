import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 91Page_pt2confg.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:91Page-pt2confg.obj=d6defe7576252bdb91df0cfa335db0d3ba3c5e2ef64bb037c9585b0cc913aef9
    +test_classification:System
    +name: test_pcl5_highvalue_91page_pt2confg
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_91page_pt2confg
        +guid:61ee0b1f-3e62-492b-978b-d8110dfe5024
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:1000
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_91page_pt2confg(setup_teardown, printjob, outputsaver, print_emulation):
    if print_emulation.print_engine_platform == 'emulator':
        print_emulation.tray.setup_tray(
            trayid="all",
            media_size=MediaSize.Letter.name,
            media_type=MediaType.Plain.name,
            orientation=MediaOrientation.Default.name,
            level=TrayLevel.Full.name
        )
    printjob.print_verify_multi('d6defe7576252bdb91df0cfa335db0d3ba3c5e2ef64bb037c9585b0cc913aef9', expected_jobs=3,timeout=1000)
    outputsaver.save_output()
