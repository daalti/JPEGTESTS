import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using cttfontm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:cttfontm.obj=1dbb5eae34a347818c3bad4756e6311fba27dfbe4808afcb46587c1a54a88b1c
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_cttfontm
    +test:
        +title: test_pcl5_pcl_pclcolor_cttfontm
        +guid:8c51ce74-c628-414f-98b1-dddf2531b70b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_cttfontm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1dbb5eae34a347818c3bad4756e6311fba27dfbe4808afcb46587c1a54a88b1c', timeout=900)
    outputsaver.save_output()
