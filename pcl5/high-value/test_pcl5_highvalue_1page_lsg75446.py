import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_lsg75446.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-lsg75446.obj=5204ace0373a691e6fe20204ec0d089d8385b8f4b4b22d9fc39a9ec2bd6af1b3
    +test_classification:System
    +name: test_pcl5_highvalue_1page_lsg75446
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_1page_lsg75446
        +guid:fd9e487a-0865-4507-a176-dbadbe2c8020
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

def test_pcl5_highvalue_1page_lsg75446(setup_teardown, printjob, outputsaver,tray, print_emulation):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
        print_emulation.tray.setup_tray(trayid="all", media_size=MediaSize.A4.name, media_type=MediaType.Plain.name,
                                    orientation=MediaOrientation.Default.name, level=TrayLevel.Full.name)


    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm','stationery')
    
    printjob.print_verify('5204ace0373a691e6fe20204ec0d089d8385b8f4b4b22d9fc39a9ec2bd6af1b3', timeout=600)
    outputsaver.save_output()
