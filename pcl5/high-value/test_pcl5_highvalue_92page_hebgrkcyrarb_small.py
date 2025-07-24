import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 92Page_HebGrkCyrArb_small.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1500
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:92Page-HebGrkCyrArb_small.obj=b98eebfa5a3a6a4322cfabdb4133f00ac9d94a4c4584d5b38a07e50c06dbab66
    +test_classification:System
    +name: test_pcl5_highvalue_92page_hebgrkcyrarb_small
    +test:
        +title: test_pcl5_highvalue_92page_hebgrkcyrarb_small
        +guid:7c20510e-3dec-47f6-8d82-940870e6dd4f
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

def test_pcl5_highvalue_92page_hebgrkcyrarb_small(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b98eebfa5a3a6a4322cfabdb4133f00ac9d94a4c4584d5b38a07e50c06dbab66', timeout=1500)
    outputsaver.save_output()
