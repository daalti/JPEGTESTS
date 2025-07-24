import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ctmtrics.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1400
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ctmtrics.obj=7c35934ba633020b31dde86080734b61606c322a87354fb54e94f85f5ea1444a
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_ctmtrics
    +test:
        +title: test_pcl5_pcl_pclcolor_ctmtrics
        +guid:c655e0db-4925-404c-990e-9164b44224c2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_ctmtrics(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7c35934ba633020b31dde86080734b61606c322a87354fb54e94f85f5ea1444a', timeout=1400)
    outputsaver.save_output()
