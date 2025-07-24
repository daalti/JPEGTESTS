import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 57Page_edicras.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1200
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:57Page-edicras.obj=e06b2093af57d251171d7ffda15fc67e9809f5783184b6d8b97a8fe9a4e2e3d3
    +test_classification:System
    +name: test_pcl5_highvalue_57page_edicras
    +test:
        +title: test_pcl5_highvalue_57page_edicras
        +guid:97f6fdd1-6ad6-4b65-acda-b1a072066dc1
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

def test_pcl5_highvalue_57page_edicras(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e06b2093af57d251171d7ffda15fc67e9809f5783184b6d8b97a8fe9a4e2e3d3', timeout=1200)
    outputsaver.save_output()
