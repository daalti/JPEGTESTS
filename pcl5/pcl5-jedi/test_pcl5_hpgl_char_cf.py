import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using cf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:cf.obj=e141712a17bf1a30b939466567c976e63655bf8f00fb2629df17071510c2e309
    +test_classification:System
    +name: test_pcl5_hpgl_char_cf
    +test:
        +title: test_pcl5_hpgl_char_cf
        +guid:e3be56ee-a61c-48fe-a193-fcbb9b7e7b7b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_cf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e141712a17bf1a30b939466567c976e63655bf8f00fb2629df17071510c2e309', timeout=600)
    outputsaver.save_output()
