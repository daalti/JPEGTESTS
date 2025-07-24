import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 167Page_hzpltsz2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:167Page-hzpltsz2.obj=9ab7ae90da6c2bea5ee71cdb908640593c38c9f65a857b2e1b24166670281115
    +test_classification:System
    +name: test_pcl5_highvalue_167page_hzpltsz2
    +test:
        +title: test_pcl5_highvalue_167page_hzpltsz2
        +guid:82316dc7-05b0-4bc3-8b56-f8dcc008d686
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

def test_pcl5_highvalue_167page_hzpltsz2(setup_teardown, printjob, outputsaver, print_emulation, configuration, tray):
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        print("Running on enterprise emulator")
        # Get list of installed trays
        installed_trays = print_emulation.tray.get_installed_trays()
        print(f"Installed trays: {installed_trays}")
        selected_tray = None
        
        # Check each tray for Letter/Plain support
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            print(f"Tray {tray_id} - Supported sizes: {supported_sizes}, Supported types: {supported_types}")
            
            if MediaSize.Letter.name in supported_sizes and MediaType.Plain.name in supported_types:
                selected_tray = tray_id
                print(f"Selected tray {selected_tray} for Letter/Plain")
                break
                
        if selected_tray is None:
            raise ValueError("No tray found supporting Letter size and Plain type paper")
            
        # Set unlimited capacity for selected tray
        print(f"Setting {selected_tray} to unlimited capacity")
        print_emulation.tray.capacity_unlimited(selected_tray)
        
        # Open and load the tray directly since we know it's available and supported
        print(f"Opening {selected_tray}")
        print_emulation.tray.open(selected_tray)
        
        # Load with Letter/Plain paper
        print(f"Loading {selected_tray} with Letter/Plain paper")
        print_emulation.tray.load(selected_tray, MediaSize.Letter.name, MediaType.Plain.name,
                              media_orientation=MediaOrientation.Portrait.name)
        
        print(f"Closing {selected_tray}")
        print_emulation.tray.close(selected_tray)

    printjob.print_verify('9ab7ae90da6c2bea5ee71cdb908640593c38c9f65a857b2e1b24166670281115', timeout=3600)
    outputsaver.save_output()
