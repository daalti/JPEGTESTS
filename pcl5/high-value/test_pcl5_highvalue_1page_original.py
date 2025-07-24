import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_Original.prn
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-Original.prn=9b3eab0da0d187f3992d76f387c8e95c7ab2607b7ff5df84bec30ea11c8be90d
    +test_classification:System
    +name: test_pcl5_highvalue_1page_original
    +test:
        +title: test_pcl5_highvalue_1page_original
        +guid:adad0c6e-0439-46e1-807e-8ab06553e3c1
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

def test_pcl5_highvalue_1page_original(setup_teardown, printjob, outputsaver, print_emulation, configuration, tray):

    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        # Get list of installed trays
        installed_trays = print_emulation.tray.get_installed_trays()
        selected_tray = None
        
        # Check each tray for A4/Plain support
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            
            # Check if this tray supports A4 and Plain
            if MediaSize.A4.name in supported_sizes and MediaType.Plain.name in supported_types:
                selected_tray = tray_id
                break
        
        if selected_tray is None:
            raise ValueError("No tray found supporting A4 size and Plain type paper")
        
        # Open and load the selected tray
        print_emulation.tray.open(selected_tray)
        print_emulation.tray.load(selected_tray, MediaSize.A4.name, MediaType.Plain.name, 
                                media_orientation=MediaOrientation.Portrait.name)
        print_emulation.tray.close(selected_tray)
    else:

        # Original code for non-emulator case
        default = tray.get_default_source()
        if tray.is_size_supported('iso_a4_210x297mm', default):
            tray.configure_tray(default, 'iso_a4_210x297mm', 'any')

    printjob.print_verify('9b3eab0da0d187f3992d76f387c8e95c7ab2607b7ff5df84bec30ea11c8be90d', timeout=600)
    outputsaver.save_output()
    tray.reset_trays()
