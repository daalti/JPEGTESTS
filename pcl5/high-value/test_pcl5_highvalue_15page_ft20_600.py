import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 15Page_ft20_600.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:180
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:15Page-ft20_600.obj=38bdec6309e1212232f010ee8b51437da763f3641e1b0116af3ade12defc6842
    +test_classification:System
    +name: test_pcl5_highvalue_15page_ft20_600
    +test:
        +title: test_pcl5_highvalue_15page_ft20_600
        +guid:a6ff43c4-4664-4c3d-a7ee-31d3852a198b
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

def test_pcl5_highvalue_15page_ft20_600(setup_teardown, printjob, outputsaver, print_emulation, configuration, tray):
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        installed_trays = print_emulation.tray.get_installed_trays()
        selected_tray = None
        
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            
            if MediaSize.Letter.name in supported_sizes and MediaType.Plain.name in supported_types:
                selected_tray = tray_id
                break
        
        if selected_tray is None:
            raise ValueError("No tray found supporting Letter size and Plain type paper")
        
        print_emulation.tray.open(selected_tray)
        print_emulation.tray.load(selected_tray, MediaSize.Letter.name, MediaType.Plain.name,
                                media_orientation=MediaOrientation.Portrait.name)
        print_emulation.tray.close(selected_tray)

    printjob.print_verify('38bdec6309e1212232f010ee8b51437da763f3641e1b0116af3ade12defc6842', timeout=300)
    outputsaver.save_output()
    tray.reset_trays()
