import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 28Page_lanscape.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:28Page-lanscape.obj=e19a0bbcfce7f2105739efe487bf56b1d4bb51b43095112704553f18f94f0b89
    +test_classification:System
    +name: test_pcl5_basicfunctionality_28page_lanscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_28page_lanscape
        +guid:688203c3-d802-4b55-a3d3-e462e5826b09
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
def test_pcl5_basicfunctionality_28page_lanscape(setup_teardown, printjob, outputsaver, print_emulation, configuration, tray):
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        # Get list of installed trays
        installed_trays = print_emulation.tray.get_installed_trays()
        selected_tray = None
        
        # Check each tray for Letter/Plain support
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

    printjob.print_verify('e19a0bbcfce7f2105739efe487bf56b1d4bb51b43095112704553f18f94f0b89', timeout=600)
    outputsaver.save_output()
    tray.reset_trays()
