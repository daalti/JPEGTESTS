import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 245Page_macro_gl.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:245Page-macro_gl.obj=64cfbac5616eeaf2c7479acccac37f2bf5ff12bd144f830d1ad4d670fbfdd873
    +test_classification:System
    +name: test_pcl5_basicfunctionality_245page_macro_gl
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_245page_macro_gl
        +guid:d2e56b62-ace9-42b9-b5ee-a1a0ec75d900
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
def test_pcl5_basicfunctionality_245page_macro_gl(setup_teardown, printjob, outputsaver, print_emulation, configuration, tray):
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        # Get list of installed trays
        installed_trays = print_emulation.tray.get_installed_trays()
        selected_tray = None
        
        # Check each tray for supported sizes
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            
            if MediaSize.Letter.name in supported_sizes and MediaType.Plain.name in supported_types:
                selected_tray = tray_id
                break
        
        if selected_tray is None:
            raise ValueError("No tray found supporting Letter size and Plain type paper")
            
        print_emulation.tray.capacity_unlimited(selected_tray)
        print_emulation.tray.open(selected_tray)
        print_emulation.tray.load(selected_tray, MediaSize.Letter.name, MediaType.Plain.name,
                              media_orientation=MediaOrientation.Portrait.name)
        print_emulation.tray.close(selected_tray)

    printjob.print_verify('64cfbac5616eeaf2c7479acccac37f2bf5ff12bd144f830d1ad4d670fbfdd873', timeout=3600)
    outputsaver.save_output()
    tray.reset_trays()
