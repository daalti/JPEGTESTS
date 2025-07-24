import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 300Page_ctmtrics.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:300Page-ctmtrics.obj=79a18fd6bf4915c6d0c35be07e0d2f274b27b1dfecdee71962b1bde3d62cc48e
    +test_classification:System
    +name: test_pcl5_highvalue_300page_ctmtrics
    +test:
        +title: test_pcl5_highvalue_300page_ctmtrics
        +guid:78c22e54-02d7-4265-802e-6ab7053f756a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:4000
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_300page_ctmtrics(setup_teardown, printjob, outputsaver, print_emulation, tray, configuration):
    if print_emulation.print_engine_platform == 'emulator':
        installed_trays = print_emulation.tray.get_installed_trays()

        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)

            if MediaSize.Letter.name in supported_sizes and MediaType.Plain.name in supported_types:
                print_emulation.tray.capacity_unlimited(tray_id)
                print_emulation.tray.open(tray_id)
                print_emulation.tray.load(tray_id, MediaSize.Letter.name, MediaType.Plain.name,
                                    media_orientation=MediaOrientation.Portrait.name)
                print_emulation.tray.close(tray_id)
                break

    printjob.print_verify('79a18fd6bf4915c6d0c35be07e0d2f274b27b1dfecdee71962b1bde3d62cc48e', timeout=4000)
    outputsaver.save_output()
