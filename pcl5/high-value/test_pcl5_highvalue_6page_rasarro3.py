import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 6Page_rasarro3.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:6Page-rasarro3.obj=0ec97836048ae4555fe0279e538d6b3d179ceda7c7085d181d450b2c4fa00d6d
    +test_classification:System
    +name: test_pcl5_highvalue_6page_rasarro3
    +test:
        +title: test_pcl5_highvalue_6page_rasarro3
        +guid:6b2fb6e8-f12c-4b45-ad1f-c8b4dd8359f4
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

def test_pcl5_highvalue_6page_rasarro3(setup_teardown, printjob, outputsaver,tray, print_emulation):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
        print_emulation.tray.setup_tray(trayid="all", media_size=MediaSize.Legal.name, media_type=MediaType.Plain.name,
                                    orientation=MediaOrientation.Default.name, level=TrayLevel.Full.name)
    
    elif    tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in','stationery')
    printjob.print_verify_multi('0ec97836048ae4555fe0279e538d6b3d179ceda7c7085d181d450b2c4fa00d6d',expected_jobs=6,timeout=900)
    outputsaver.save_output()
