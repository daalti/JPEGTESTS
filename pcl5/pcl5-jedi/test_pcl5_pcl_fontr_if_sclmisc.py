import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using sclmisc.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sclmisc.obj=0e8737114e69386b4f84261901c2a518d3c9ea06113b1bfad8d48953e7532728
    +test_classification:System
    +name: test_pcl5_pcl_fontr_if_sclmisc
    +test:
        +title: test_pcl5_pcl_fontr_if_sclmisc
        +guid:bf3c43ec-1ae8-4523-844b-28a890befc6d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontr_if_sclmisc(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0e8737114e69386b4f84261901c2a518d3c9ea06113b1bfad8d48953e7532728', timeout=600)
    outputsaver.save_output()
