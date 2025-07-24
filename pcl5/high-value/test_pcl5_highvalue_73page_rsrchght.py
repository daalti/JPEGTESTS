import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 73Page_rsrchght.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1200
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:73Page-rsrchght.obj=40e968255cbfb3dae9cfcf1eb4bbd69afb66d75805070436c5aec12e06ee6ebd
    +test_classification:System
    +name: test_pcl5_highvalue_73page_rsrchght
    +test:
        +title: test_pcl5_highvalue_73page_rsrchght
        +guid:e52d12ed-b850-4baa-b039-2ff3d2f20d5e
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

def test_pcl5_highvalue_73page_rsrchght(setup_teardown, printjob, outputsaver):
    printjob.print_verify('40e968255cbfb3dae9cfcf1eb4bbd69afb66d75805070436c5aec12e06ee6ebd', timeout=1200)
    outputsaver.save_output()
