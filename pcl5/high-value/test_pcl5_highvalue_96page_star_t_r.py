import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 96Page_star_t_r.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1620
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:96Page-star_t_r.obj=f7ecb9d81f45bb5ce189d471233c2993e373216ad584dd155fad7ee0d7d8c7c3
    +test_classification:System
    +name: test_pcl5_highvalue_96page_star_t_r
    +test:
        +title: test_pcl5_highvalue_96page_star_t_r
        +guid:136c8ca8-585c-45d7-bf56-049001f5d5f3
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

def test_pcl5_highvalue_96page_star_t_r(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f7ecb9d81f45bb5ce189d471233c2993e373216ad584dd155fad7ee0d7d8c7c3', timeout=1500)
    outputsaver.save_output()
