import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation, TrayLevel

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_lsg67924.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-lsg67924.obj=abe7c9a37056f9845f0537ca74e3c8fa73c3990be1e02de4fe2446487c1d7dd6
    +test_classification:System
    +name: test_pcl5_highvalue_1page_lsg67924
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_1page_lsg67924
        +guid:6d608a12-38a9-4e40-b69f-0d3577caf3af
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

def test_pcl5_highvalue_1page_lsg67924(setup_teardown, printjob, outputsaver,tray, print_emulation):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
        print_emulation.tray.setup_tray(trayid="all",media_size=MediaSize.A4.name,media_type=MediaType.Plain.name,orientation=MediaOrientation.Default.name,level=TrayLevel.Full.name)
    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'any')
    printjob.print_verify('abe7c9a37056f9845f0537ca74e3c8fa73c3990be1e02de4fe2446487c1d7dd6', timeout=600)
    outputsaver.save_output()
    tray.reset_trays() 