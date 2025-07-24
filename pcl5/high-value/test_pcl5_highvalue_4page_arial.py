import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 4Page_arial.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:4Page-arial.obj=c74922027034624c176f82abd10e72e375b8a81ae68fdcdc37af09797d546468
    +test_classification:System
    +name: test_pcl5_highvalue_4page_arial
    +test:
        +title: test_pcl5_highvalue_4page_arial
        +guid:375e3085-b3c5-4871-8659-c820b3390d25
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

def test_pcl5_highvalue_4page_arial(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c74922027034624c176f82abd10e72e375b8a81ae68fdcdc37af09797d546468')
    outputsaver.save_output()
