import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 17Page_kerning.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:17Page-kerning.obj=74af3eb476370ce3161faa68227a1a2495f98fc504a3746f28db65971c4dceba
    +test_classification:System
    +name: test_pcl5_highvalue_17page_kerning
    +test:
        +title: test_pcl5_highvalue_17page_kerning
        +guid:487bf5c5-1f91-47b5-acab-9f027982d9a4
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

def test_pcl5_highvalue_17page_kerning(setup_teardown, printjob, outputsaver, print_emulation, configuration, tray):
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':

        # Get list of installed trays
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

    printjob.print_verify('74af3eb476370ce3161faa68227a1a2495f98fc504a3746f28db65971c4dceba', timeout=300)
    outputsaver.save_output()
    tray.reset_trays()
