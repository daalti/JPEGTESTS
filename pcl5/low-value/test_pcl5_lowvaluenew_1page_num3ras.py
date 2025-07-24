import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 1Page_num3ras.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-num3ras.obj=24c9221157c11139ea8c24aecc4acbd7a7c14597545361399002242bae93a053
    +test_classification:System
    +name: test_pcl5_lowvaluenew_1page_num3ras
    +test:
        +title: test_pcl5_lowvaluenew_1page_num3ras
        +guid:1bb1bae6-be1f-470b-8607-d3d7183647e4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_1page_num3ras(setup_teardown, printjob, outputsaver):
    printjob.print_verify('24c9221157c11139ea8c24aecc4acbd7a7c14597545361399002242bae93a053', timeout=600)
    outputsaver.save_output()
