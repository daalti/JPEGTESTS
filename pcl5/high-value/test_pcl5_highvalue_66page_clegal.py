import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 66Page_clegal.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:66Page-clegal.obj=6bd52cbabaf17018c6532f32e854e6bd60559c3777d66c94bc00eee25fc785d4
    +test_classification:System
    +name: test_pcl5_highvalue_66page_clegal
    +test:
        +title: test_pcl5_highvalue_66page_clegal
        +guid:5185a8d8-712e-45fa-a42a-b6a0e539bf29
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:900
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_66page_clegal(setup_teardown, printjob, outputsaver,tray, print_emulation, configuration):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        installed_trays = print_emulation.tray.get_installed_trays()
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            if MediaSize.Legal.name in supported_sizes and MediaType.Plain.name in supported_types:
                print_emulation.tray.capacity_unlimited(tray_id)
                print_emulation.tray.load(tray_id, MediaSize.Legal.name, MediaType.Plain.name)
    
    elif tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in','stationery')
    printjob.print_verify('6bd52cbabaf17018c6532f32e854e6bd60559c3777d66c94bc00eee25fc785d4', timeout=900)
    outputsaver.save_output()
