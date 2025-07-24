import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 2Page_fullp75.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:2Page-fullp75.obj=a7c12839b6aedd8ebead9578139358bc3fd6d9ce8bf919549401537503f4b48e
    +test_classification:System
    +name: test_pcl5_highvalue_2page_fullp75
    +test:
        +title: test_pcl5_highvalue_2page_fullp75
        +guid:4cc95929-6bdc-47d2-93d5-67d85f1fc1f7
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

def test_pcl5_highvalue_2page_fullp75(setup_teardown, printjob, outputsaver, print_emulation, configuration,tray):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        print ("emulator execution")
        # Get list of installed trays
        installed_trays = print_emulation.tray.get_installed_trays()
        selected_tray = None
        
        # Check each tray for Legal/Plain support
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            
            # Check if this tray supports Legal and Plain
            if MediaSize.Legal.name in supported_sizes and MediaType.Plain.name in supported_types:
                selected_tray = tray_id
                break
        
        if selected_tray is None:
            raise ValueError("No tray found supporting Legal size and Plain type paper")
        
        # Open and load the selected tray
        print_emulation.tray.open(selected_tray)
        print_emulation.tray.load(selected_tray, MediaSize.Legal.name, MediaType.Plain.name, 
                                media_orientation=MediaOrientation.Portrait.name)
        print_emulation.tray.close(selected_tray)
    else:
        if tray.is_size_supported('na_legal_8.5x14in', default):
            tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')
    printjob.print_verify('a7c12839b6aedd8ebead9578139358bc3fd6d9ce8bf919549401537503f4b48e', timeout=600)
    outputsaver.save_output()
